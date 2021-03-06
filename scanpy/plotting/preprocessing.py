import numpy as np
from matplotlib import pyplot as pl
from matplotlib import rcParams
from . import utils

# --------------------------------------------------------------------------------
# Plot result of preprocessing functions
# --------------------------------------------------------------------------------


def filter_genes_dispersion(result, log=False, save=None, show=None):
    """Plot dispersions vs. means for genes.

    Produces Supp. Fig. 5c of Zheng et al. (2017) and MeanVarPlot() of Seurat.

    Parameters
    ----------
    result: np.recarray
        Result of sc.pp.filter_genes_dispersion.
    log : bool
        Plot on logarithmic axes.
    """
    gene_subset = result.gene_subset
    means = result.means
    dispersions = result.dispersions
    dispersions_norm = result.dispersions_norm
    for id, d in enumerate([dispersions_norm, dispersions]):
        pl.figure(figsize=rcParams['figure.figsize'])
        for label, color, mask in zip(['highly variable genes', 'other genes'],
                                      ['black', 'grey'],
                                      [gene_subset, ~gene_subset]):
            if False: means_, disps_ = np.log10(means[mask]), np.log10(d[mask])
            else: means_, disps_ = means[mask], d[mask]
            pl.scatter(means_, disps_, label=label, c=color, s=1)
        if log:  # there's a bug in autoscale
            pl.xscale('log')
            pl.yscale('log')
            min_dispersion = np.min(dispersions)
            y_min = 0.95*min_dispersion if min_dispersion > 0 else 1e-1
            pl.xlim(0.95*np.min(means), 1.05*np.max(means))
            pl.ylim(y_min, 1.05*np.max(dispersions))
        pl.legend()
        pl.xlabel(('$log_{10}$ ' if False else '') + 'mean expression of gene')

        file_name = 'filter_genes_dispersion{}'.format('_normalized' if id == 0 else '')
        pl.ylabel(('$log_{10}$ ' if False else '') + 'dispersion of gene'
                  + (' (normalized)' if id == 0 else ' (not normalized)'))
        utils.savefig_or_show(file_name, show=show, save=save)
        
