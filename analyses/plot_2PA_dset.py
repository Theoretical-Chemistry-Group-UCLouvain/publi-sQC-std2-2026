import pandas
import matplotlib.pyplot as plt
import numpy
import argparse
import itertools

def mad(data, axis=None):
    return numpy.mean(numpy.abs(data - numpy.mean(data, axis)), axis)

def prepare_data(data: pandas.DataFrame):
    return data

def plot_XC(ax, data, k, name, val: str = 'E0n', ref: str = 'RI-CC2', gmax: float = 0.6, add_label=False):
    data_ref = data[data['Method'] == ref]
    
    for i, a in enumerate(['', 's', 'Xs']):
        data_XC = data[data['Method'] == a + name]
        if len(data_XC) == 0:
            print('no', a, name)
            continue
        
        if '2PA' in val:
            diff = numpy.log10(data_XC[val].values) - numpy.log10(data_ref[val].values)
        else:
            diff = data_XC[val].values - data_ref[val].values
        
        vp = ax.violinplot(diff, positions=[k  + i / 4 - .25], widths=0.25, showmeans=True, showextrema=True, orientation='horizontal')
        vp['bodies'][0].set_facecolor('C{}'.format(i))
        for p in ['cbars', 'cmins', 'cmaxes', 'cmeans']:
            vp[p].set_edgecolors('C{}'.format(i))
        
        ax.text(
            diff.max() if diff.max() < .75 * gmax else diff.min(), 
            k + i / 4 - .25, ' {:.2f} ({:.2f}) '.format(numpy.mean(diff), mad(diff)), 
            va='center', 
            ha='left' if diff.max() < .75 * gmax else 'right')

parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('-o', '--output', default='Data_2PA.pdf')
parser.add_argument('-g', '--gmax', default=0.5, type=float)

args = parser.parse_args()

data = prepare_data(pandas.read_csv(args.input))

figure = plt.figure(figsize=(10, 9))
axes = figure.subplots(1, 2, sharey=True)
    
axes[0].vlines(0, -1, 9, linestyle='--', color='gray', linewidth=0.7)
axes[1].vlines(0, -1, 9, linestyle='--', color='gray', linewidth=0.7)

XCFs = ['TPSSH', 'B3LYP', 'PBE0', 'M06', 'BHHLYP', 'M06-2X', 'CAM-B3LYP', 'ωB97X-D3', 'ωB97M-V']

axes[0].set_ylim(-.5, 8.5)
axes[0].set_yticks(numpy.ravel([(j -.25, j, j + .25) for j in range(len(XCFs))]), ['TD', 'sTD', 'XsTD'] * len(XCFs))

axes[0].set_xlabel('$\\Delta\\Delta E_{0\\rightarrow n}$ (eV)')
axes[1].set_xlabel('$\\Delta \\log_{10}(\\delta^{2PA})$')

for i, n in enumerate(XCFs):
    axes[0].text(-.15, i / len(XCFs) + .055, n, transform=axes[0].transAxes, ha='center', va='center', rotation=90, fontsize=11, color='gray')
    plot_XC(axes[0], data, i, n, val='E0n', gmax=args.gmax)
    plot_XC(axes[1], data, i, n, val='δ2PA', gmax=args.gmax)

plt.tight_layout()

figure.savefig(args.output, dpi=300)
