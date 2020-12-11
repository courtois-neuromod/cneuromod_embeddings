#/bin/bash

export PATH_RESULTS='/data/cisl/pbellec/cneuromod_embeddings/xp_202012/friends-s01_reproducibility'
export PATH_DATA='/data/cisl/pbellec/cneuromod_embeddings/xp_202012'

echo Input data located in $PATH_DATA
echo Results will be saved in $PATH_RESULTS
python friends-s01_reproducibility.py --fwhm 5 --cluster 300 --state 900 $PATH_DATA $PATH_RESULTS
