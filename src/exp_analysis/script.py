import pandas as pd
import anndata as ad
import sys
import json

## VIASH START
par = {
  "perturbation_data": "resources/grn-benchmark/perturbation_data.h5ad",
  "prediction": "output/scenic_default/scenic.csv",
  # "peak_gene_net": "resources/grn-benchmark/peak_gene_models/figr.csv",
  "annot_peak_database": "resources/supplementary/annot_peak_database.csv",
  "annot_gene_database": "resources/supplementary/annot_gene_database.csv",
  "stats": "output/stats.json",
  "reg_weight_distribution": "output/reg_weight_distribution.png",
  "tf_gene_indegee_fig": "output/tf_gene_indegee_fig.png",
  "tf_gene_outdegee_fig": "output/tf_gene_outdegee_fig.png"
}
## VIASH END


perturbation_data = ad.read_h5ad(par["perturbation_data"])
prediction = pd.read_csv(par["prediction"])
# peak_gene_net = pd.read_csv(par["peak_gene_net"])
# annot_peak_database = pd.read_csv(par["annot_peak_database"])
# hvgs = pd.read_csv(par["hvgs"])

meta = {
  "resources_dir":'src/exp_analysis/'
}
sys.path.append(meta["resources_dir"])
from helper import Explanatory_analysis, plot_cumulative_density

print('Plotting CMD of weight: ',par['reg_weight_distribution'], flush=True)
fig, ax = plot_cumulative_density(prediction.weight, title='CMD of reg. weight')
fig.savefig(par['reg_weight_distribution'])

print('Reading input files', flush=True)
# peak_gene_net['source'] = peak_gene_net['peak']
info_obj = Explanatory_analysis(net=prediction)
print("Calculate basic stats")
stats = info_obj.calculate_basic_stats()
print(stats)
print("Outputting stats to :", par['stats'])
with open(par['stats'], 'w') as ff:
  json.dump(stats, ff)
# print("Annotation of peaks")
# peak_annot = info_obj.annotate_peaks(annot_peak_database)
# print("Annotation of genes")
# gene_annot = info_obj.annotate_genes(annot_gene_database)
print("Topological analysis")
info_obj.calculate_centrality_stats()

tf_gene_in = info_obj.tf_gene.in_deg
tf_gene_out = info_obj.tf_gene.out_deg

print("Plotting tf-gene in degree, dir: ", par['tf_gene_indegee_fig'])
print("Plotting tf-gene out degree, dir: ", par['tf_gene_outdegee_fig'])
fig, ax = info_obj.plot_cdf(tf_gene_in, title='In degree TF-gene')
fig.savefig(par['tf_gene_indegee_fig'], dpi=300, bbox_inches='tight', format='png')
fig, ax = info_obj.plot_cdf(tf_gene_out, title='Out degree TF-gene')
fig.savefig(par['tf_gene_outdegee_fig'], dpi=300, bbox_inches='tight', format='png')

