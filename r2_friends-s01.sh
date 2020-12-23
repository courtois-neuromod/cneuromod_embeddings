#/bin/bash

export PATH_RESULTS='/data/cisl/pbellec/cneuromod_embeddings/xp_202012/r2_friends-s01'
export PATH_DATA='/data/cisl/pbellec/cneuromod_embeddings/xp_202012'

echo Input data located in $PATH_DATA
echo Results will be saved in $PATH_RESULTS

python r2_summary.py --atlas intra --fwhm 5 --cluster 20  --state 60  $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas intra --fwhm 5 --cluster 20  --state 120 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas intra --fwhm 5 --cluster 50  --state 150 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas intra --fwhm 5 --cluster 50  --state 300 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas intra --fwhm 5 --cluster 300 --state 900 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas intra --fwhm 8 --cluster 20  --state 60  $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas intra --fwhm 8 --cluster 20  --state 120 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas intra --fwhm 8 --cluster 50  --state 150 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas intra --fwhm 8 --cluster 50  --state 300 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas intra --fwhm 8 --cluster 300 --state 900 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas inter --fwhm 5 --cluster 20  --state 60  $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas inter --fwhm 5 --cluster 20  --state 120 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas inter --fwhm 5 --cluster 50  --state 150 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas inter --fwhm 5 --cluster 50  --state 300 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas inter --fwhm 5 --cluster 300 --state 900 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas inter --fwhm 8 --cluster 20  --state 60  $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas inter --fwhm 8 --cluster 20  --state 120 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas inter --fwhm 8 --cluster 50  --state 150 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas inter --fwhm 8 --cluster 50  --state 300 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas inter --fwhm 8 --cluster 300 --state 900 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas difumo1024 --fwhm 5 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas difumo512  --fwhm 5 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas difumo256  --fwhm 5 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas mist197    --fwhm 5 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas mist444    --fwhm 5 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas schaefer   --fwhm 5 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas smith      --fwhm 5 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas difumo1024 --fwhm 8 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas difumo512  --fwhm 8 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas difumo256  --fwhm 8 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas mist197    --fwhm 8 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas mist444    --fwhm 8 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas schaefer   --fwhm 8 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --atlas smith      --fwhm 8 $PATH_DATA $PATH_RESULTS &

