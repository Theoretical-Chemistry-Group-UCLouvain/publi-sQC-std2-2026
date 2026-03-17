import sys

import numpy
import numpy as np
import pandas
from pyscf import gto, scf, ao2mo

import argparse


def mae(m: np.ndarray, ref: np.ndarray):
    """MAE"""
    return np.abs(m - ref).mean()


def MAEs_mo_ERIs(mol: gto.Mole):
    """Get MAEs for 0th, 1st, 2nd, and full CNDO approximation"""
    # Do HF
    mf = scf.RHF(mol)
    mf.kernel()

    C = mf.mo_coeff
    nao = C.shape[0]

    # AO integrals
    S = mol.intor("int1e_ovlp")
    eri_ao = mol.intor("int2e")

    # Exact MO ERIs
    eri_mo_exact = ao2mo.restore(1, ao2mo.kernel(mol, C), C.shape[1])

    # Löwdin orthogonalization
    eigval, eigvec = np.linalg.eigh(S)

    eigv = np.linalg.eigh(S - numpy.eye(S.shape[0]))

    S_inv_sqrt = eigvec @ np.diag(eigval**(-0.5)) @ eigvec.T
    S_sqrt = eigvec @ np.diag(eigval**0.5) @ eigvec.T

    # orthogonalized AO integrals
    eri_orth_ao = np.einsum(
        "pa,qb,rc,sd,abcd->pqrs",
        S_inv_sqrt,
        S_inv_sqrt,
        S_inv_sqrt,
        S_inv_sqrt,
        eri_ao,
        optimize=True
    )

    # orthogonalized MO coefficients
    C_orth = S_sqrt @ C

    # MO ERIs in orthogonalized basis
    eri_mo_limit = np.einsum(
        "pi,pj,qk,ql,ppqq->ijkl",
        C_orth,
        C_orth,
        C_orth,
        C_orth,
        eri_orth_ao,
        optimize=True
    )

    # CNDO approximation
    eri_cndo = np.zeros_like(eri_ao)

    for mu in range(nao):
        for nu in range(nao):
            eri_cndo[mu,mu,nu,nu] = eri_ao[mu,mu,nu,nu]

    eri_mo_cndo_0th = np.einsum(
        "pi,pj,qk,ql,ppqq->ijkl",
        C_orth,
        C_orth,
        C_orth,
        C_orth,
        eri_cndo,
        optimize=True
    )

    # 1st order correction
    for mu in range(nao):
        for nu in range(nao):
            for alpha in range(nao):
                if alpha != mu:
                    eri_cndo[mu,mu,nu,nu] -= S[mu, alpha] * eri_ao[alpha, mu, nu, nu]
                if alpha != nu:
                    eri_cndo[mu,mu,nu,nu] -= S[nu, alpha] * eri_ao[mu, mu, alpha, nu]

    eri_mo_cndo_1st = np.einsum(
        "pi,pj,qk,ql,ppqq->ijkl",
        C_orth,
        C_orth,
        C_orth,
        C_orth,
        eri_cndo,
        optimize=True
    )

    # second order correction
    for mu in range(nao):
        for nu in range(nao):
            for alpha in range(nao):
                for beta in range(nao):
                    if alpha != mu and beta != mu:
                        eri_cndo[mu,mu,nu,nu] += 1/4 * S[mu, alpha] * S[mu, beta] * eri_ao[alpha, beta, nu, nu]
                        eri_cndo[mu,mu,nu,nu] += 3/4 * S[mu, alpha] * S[alpha, beta] * eri_ao[beta, mu, nu, nu]
                    if alpha != nu and beta != nu:
                        eri_cndo[mu,mu,nu,nu] += 1/4 * S[nu, alpha] * S[nu, beta] * eri_ao[mu, mu, alpha, beta]
                        eri_cndo[mu,mu,nu,nu] += 3/4 * S[nu, alpha] * S[alpha, beta] * eri_ao[mu, mu, beta, nu]
                    if alpha != mu and beta != nu:
                        eri_cndo[mu,mu,nu,nu] += S[mu, alpha] * S[nu, beta] * eri_ao[alpha, mu, beta, nu]

    eri_mo_cndo_2nd = np.einsum(
        "pi,pj,qk,ql,ppqq->ijkl",
        C_orth,
        C_orth,
        C_orth,
        C_orth,
        eri_cndo,
        optimize=True
    )

    # Compare tensors
    return (
        eigv[0].max(),
        mae(eri_mo_cndo_0th, eri_mo_exact),
        mae(eri_mo_cndo_1st, eri_mo_exact),
        mae(eri_mo_cndo_2nd, eri_mo_exact),
        mae(eri_mo_limit, eri_mo_exact),
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--basis', default='STO-3G')
    parser.add_argument('-m', '--molecule', choices=['LiH', 'H2O', 'C2H4'], default='LiH')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout)

    args = parser.parse_args()

    data = []
    for r in np.linspace(.5, 5, 46):
        print('r={} for {} at the HF/{} level'.format(r, args.molecule, args.basis))
        if args.molecule == 'LiH':
            # r_eq = 1.619022000
            molecule = gto.M(
                atom="""
                    Li        0.000000000      0.000000000      0.000000000
                    H        0.000000000      0.000000000       {}
                """.format(r),
                basis=args.basis,
                verbose=0
            )
        elif args.molecule == 'H2O':
            # r_eq = 0.946222800
            molecule = gto.M(
                atom='''
                    O        0.000000000      0.000000000      0.000000000
                    H       -0.000002798      0.000000000      {}
                    H        0.915409140      0.000000000     -0.239507189
                '''.format(r),
                basis=args.basis,
                verbose=0
            )
        else:
            # r_eq = 1.320891000
            molecule = gto.M(
                atom=f'''
                    C        0.000000000      0.000000000      0.000000000
                    H        0.000000000      0.922596000     -0.568865000
                    H        0.000000000     -0.922596000     -0.568865000
                    C        0.000000000      0.000000000      {r}
                    H        0.000000000      0.922596000      {r + 1.889756000 - 1.320891000}
                    H        0.000000000     -0.922596000      {r + 1.889756000 - 1.320891000}
                ''',
                basis=args.basis,
                verbose=0
            )

        data.append([r, *MAEs_mo_ERIs(molecule)])

    dset = pandas.DataFrame(
        data, columns=['r', 'max_eigv_delta', 'MAE_0th_order', 'MAE_1st_order', 'MAE_2nd_order', 'MAE_cndo_exact'])

    dset.to_csv(args.output)


if __name__ == '__main__':
    main()
