import pandas as pd
import anndata as ad
import sys
import numpy as np


## VIASH START
par = {
    'perturbation_data': 'resources/grn-benchmark/perturbation_data.h5ad',
    'layer': 'scgen_pearson',
    "prediction": "resources/grn_models/donor_0_celltype/grnboost2.csv",
    'tf_all': 'resources/prior/tf_all.csv',
    "max_n_links": 50000,
    'consensus': 'resources/prior/consensus-num-regulators.json',
    'score': 'output/score_regression2.csv',
    'reg_type': 'ridge',
    'static_only': True,
    'layer': 'scgen_pearson',
    'subsample': -2,
    'max_workers': 4,
    'apply_tf': True,
    'clip_scores': True,
    'method_id': 'grnboost'
    
}
## VIASH END
# meta = {
#   "resources_dir":'src/metrics/regression_1/'
# }
print(par)
sys.path.append(meta['resources_dir'])
from main import main

if isinstance(par['reg_type'], list) and (len(par['reg_type']) == 1):
    par['reg_type'] = par['reg_type'][0]
assert isinstance(par['reg_type'], str)

print('Reading input data')

output = main(par)

print('Write output to file', flush=True)
print(output)
metric_ids = output.columns.to_numpy()
metric_values = output.values[0]

output = ad.AnnData(
    X=np.empty((0, 0)),
    uns={
        "dataset_id": str(par["layer"]),
        "method_id": f"reg2-{par['method_id']}",
        "metric_ids": metric_ids,
        "metric_values": metric_values
    }
)
output.write_h5ad(par['score'], compression='gzip')
print('Completed', flush=True)
