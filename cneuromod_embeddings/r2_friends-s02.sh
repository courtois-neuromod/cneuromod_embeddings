#/bin/bash

myInvocation="$(printf %q "$BASH_SOURCE")$((($#)) && printf ' %q' "$@")"
export TYPE_MASK=$3
export PATH_RESULTS=$2"/r2_"$TYPE_MASK
export PATH_DATA=$1
export XP_TYPE="friends-s02"

echo Experiment type: $XP_TYPE
echo Input data located in $PATH_DATA
echo Results will be saved in $PATH_RESULTS

mkdir $PATH_RESULTS
echo $myInvocation > $PATH_RESULTS"/r2_friends-s02.log"

python r2_summary.py --type_mask $TYPE_MASK --xp_type $XP_TYPE --atlas training --fwhm 5 --cluster 64   --state 256  $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --xp_type $XP_TYPE --atlas training --fwhm 5 --cluster 64   --state 512  $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --xp_type $XP_TYPE --atlas training --fwhm 5 --cluster 256  --state 1024 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --xp_type $XP_TYPE --atlas intra --fwhm 5 --cluster 64   --state 256  $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --xp_type $XP_TYPE --atlas intra --fwhm 5 --cluster 64   --state 512  $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --xp_type $XP_TYPE --atlas intra --fwhm 5 --cluster 256  --state 1024 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --xp_type $XP_TYPE --atlas inter --fwhm 5 --cluster 64   --state 256  $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --xp_type $XP_TYPE --atlas inter --fwhm 5 --cluster 64   --state 512  $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --xp_type $XP_TYPE --atlas inter --fwhm 5 --cluster 256  --state 1024 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --xp_type $XP_TYPE --atlas difumo1024 --fwhm 5 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --xp_type $XP_TYPE --atlas difumo512  --fwhm 5 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --xp_type $XP_TYPE --atlas difumo256  --fwhm 5 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --xp_type $XP_TYPE --atlas mist197    --fwhm 5 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --xp_type $XP_TYPE --atlas mist444    --fwhm 5 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --xp_type $XP_TYPE --atlas schaefer   --fwhm 5 $PATH_DATA $PATH_RESULTS &
python r2_summary.py --type_mask $TYPE_MASK --xp_type $XP_TYPE --atlas smith      --fwhm 5 $PATH_DATA $PATH_RESULTS &

