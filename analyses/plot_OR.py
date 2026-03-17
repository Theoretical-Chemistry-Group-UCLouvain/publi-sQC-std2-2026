import pandas
import matplotlib.pyplot as plt
import numpy
import argparse

def mad(data, axis=None):
    return numpy.mean(numpy.abs(data - numpy.mean(data, axis)), axis)

def prepare_data(data: pandas.DataFrame):
    return data

def plot_XC(ax, data_n, data_s, k, name, approach: str, ref: str = 'EXP', gmax: float = 0.6):
    data_ref = data_n[data_n['Method'] == ref]
    
    for i, a in enumerate(['', 's', 'Xs']):
        if i == 0 and approach == 'MVG':
            continue

        if i > 0:
            data_XC = data_s[(data_s['Method'] == a + name) & (data_s['Approach'] == approach)]
        else:
            data_XC = data_n[data_n['Method'] == name]
        
        diff = numpy.log10(numpy.abs(data_XC['Phi_D'].values)) - numpy.log10(numpy.abs(data_ref['Phi_D'].values))
        
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
parser.add_argument('input_n')
parser.add_argument('input_simplified')
parser.add_argument('-o', '--output', default='Data_OR.pdf')
parser.add_argument('-g', '--gmax', default=2.25, type=float)

args = parser.parse_args()

data_n = prepare_data(pandas.read_csv(args.input_n))
data_simplified = prepare_data(pandas.read_csv(args.input_simplified))

figure = plt.figure(figsize=(10, 6))
axes = figure.subplots(1, 2, sharey=True)
    
axes[0].vlines(0, -1, 6, linestyle='--', color='gray', linewidth=0.7)
axes[1].vlines(0, -1, 6, linestyle='--', color='gray', linewidth=0.7)

XCFs = ['B3LYP', 'PBE0', 'BHHLYP', 'M06-2X', 'CAM-B3LYP', 'ωB97X-D3']

axes[0].set_ylim(-.5, 5.5)
axes[0].set_yticks(numpy.ravel([(j -.25, j, j + .25) for j in range(len(XCFs))]), ['TD', 'sTD', 'XsTD'] * len(XCFs))

axes[0].set_xlabel('$\\Delta log_{10}(|[\\Phi]_D|)$')
axes[1].set_xlabel('$\\Delta log_{10}(|[\\Phi]_D|)$')

for i, n in enumerate(XCFs):
    axes[0].text(-.15, i / len(XCFs) + .07, n, transform=axes[0].transAxes, ha='center', va='center', rotation=90, fontsize=11, color='gray')
    plot_XC(axes[0], data_n, data_simplified, i, n, 'LG', gmax=args.gmax)
    plot_XC(axes[1], data_n, data_simplified, i, n, 'MVG', gmax=args.gmax)
    
axes[0].set_xlim(-3, 3)
axes[1].set_xlim(-3, 3)

plt.tight_layout()
figure.savefig(args.output, dpi=300)
