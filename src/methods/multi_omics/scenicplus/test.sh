#viash build src/methods/multi_omics/scenicplus/config.novsh.yaml --platform docker -o bin/scenicplus && bin/scenicplus/scenicplus --multiomics_atac resources/resources_test/grn-benchmark/multiomics_atac.h5ad --multiomics_rna resources/resources_test/grn-benchmark/multiomics_rna.h5ad --temp_dir output/scenicplus --prediction output/scenicplus/prediction.csv --pycistopic_object output/scenicplus/pycistopic.pkl
docker run -v /mnt/c/Users/antoi/git/task_grn_inference/:/base apassemi/scenicplus python /base/src/methods/multi_omics/scenicplus/script.py
