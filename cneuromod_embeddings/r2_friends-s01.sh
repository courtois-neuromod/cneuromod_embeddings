#/bin/bash

myInvocation="$(printf %q "$BASH_SOURCE")$((($#)) && printf ' %q' "$@")"
export TYPE_MASK=$2
export PATH_RESULTS=$1'/r2_friends-s01_'$TYPE_MASK'/'
export PATH_DATA=$1

echo Input data located in $PATH_DATA
echo Results will be saved in $PATH_RESULTS

mkdir $PATH_RESULTS
echo $myInvocation > $PATH_RESULTS"script.log"

python r2_summary.py --type_mask $TYPE_MASK --atlas intra --fwhm 5 --cluster 20  --state 60  $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas intra --fwhm 5 --cluster 20  --state 120 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas intra --fwhm 5 --cluster 50  --state 150 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas intra --fwhm 5 --cluster 50  --state 300 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas intra --fwhm 5 --cluster 300 --state 900 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas intra --fwhm 8 --cluster 20  --state 60  $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas intra --fwhm 8 --cluster 20  --state 120 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas intra --fwhm 8 --cluster 50  --state 150 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas intra --fwhm 8 --cluster 50  --state 300 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas intra --fwhm 8 --cluster 300 --state 900 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas inter --fwhm 5 --cluster 20  --state 60  $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas inter --fwhm 5 --cluster 20  --state 120 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas inter --fwhm 5 --cluster 50  --state 150 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas inter --fwhm 5 --cluster 50  --state 300 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas inter --fwhm 5 --cluster 300 --state 900 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas inter --fwhm 8 --cluster 20  --state 60  $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas inter --fwhm 8 --cluster 20  --state 120 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas inter --fwhm 8 --cluster 50  --state 150 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas inter --fwhm 8 --cluster 50  --state 300 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas inter --fwhm 8 --cluster 300 --state 900 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas difumo1024 --fwhm 5 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas difumo512  --fwhm 5 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas difumo256  --fwhm 5 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas mist197    --fwhm 5 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas mist444    --fwhm 5 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas schaefer   --fwhm 5 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas smith      --fwhm 5 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas difumo1024 --fwhm 8 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas difumo512  --fwhm 8 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas difumo256  --fwhm 8 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas mist197    --fwhm 8 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas mist444    --fwhm 8 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas schaefer   --fwhm 8 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --atlas smith      --fwhm 8 $PATH_DATA $PATH_RESULTS &

