import pandas
import matplotlib.pyplot as plt
import numpy
import argparse

def prepare_data(data: pandas.DataFrame):
    return data

def plot_XC(ax, data, k, name, val: str = 'E0n', ref: str = 'RI-CC2', gmax: float = 0.6):
    data_ref = data[data['Method'] == ref]
    
    for i, a in enumerate(['', 's', 'Xs']):
        data_XC = data[data['Method'] == a + name]
        if len(data_XC) == 0:
            print('no', a, name)
            continue
        
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
parser.add_argument('inputs', nargs='*')
parser.add_argument('-n', '--names', nargs='*')
parser.add_argument('-o', '--output', default='Data_1PA.pdf')
parser.add_argument('-r', '--req', default=1.0, type=float)
parser.add_argument('-l', '--label', default='X-Y')

args = parser.parse_args()

if len(args.inputs) != len(args.names):
    raise Exception('length of `names` must match `inputs`')

figure = plt.figure(figsize=(len(args.inputs) * 3, 4))
axes = figure.subplots(1, len(args.inputs), sharex=True, sharey=True)

absmax = 0
absmin = 1

for i, (inp, name) in enumerate(zip(args.inputs, args.names)):
        data = prepare_data(pandas.read_csv(inp))
        axes[i].semilogy(data['r'], data['MAE_cndo_exact'], label='Exact' if i==0 else None)
        axes[i].semilogy(data['r'], data['MAE_0th_order'], label='0$^{th}$ order' if i==0 else None)
        axes[i].semilogy(data['r'], data['MAE_1st_order'], label='1$^{st}$ order' if i==0 else None)
        axes[i].semilogy(data['r'], data['MAE_2nd_order'], label='2$^{nd}$ order' if i==0 else None)
        
        absmax = max(absmax, data['MAE_1st_order'].max())
        absmin = min(absmin, data['MAE_cndo_exact'].min())
        
        axes[i].set_title(name)
        axes[i].set_xlabel('$r_{{{}}}$ (Å)'.format(args.label))

axes[0].set_ylim(absmin, absmax)
axes[0].set_xlim(.5, 5)
axes[0].legend()

for i in range(len(args.inputs)):
    axes[i].vlines(args.req, absmin, absmax, ls='--', color='grey')
    
axes[0].set_ylabel('MAE on $(pq|rs)$ (a.u.)')

plt.tight_layout()
figure.savefig(args.output, dpi=300)
