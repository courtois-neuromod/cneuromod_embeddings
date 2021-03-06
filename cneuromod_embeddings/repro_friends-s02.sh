#/bin/bash
myInvocation="$(printf %q "$BASH_SOURCE")$((($#)) && printf ' %q' "$@")"
export PATH_RESULTS=$1'/repro_friends-s02/'
export PATH_DATA=$1
export XP_TYPE=$2

echo Experiment type: $XP_TYPE
echo Input data located in $PATH_DATA
echo Results will be saved in $PATH_RESULTS

mkdir $PATH_RESULTS
echo $myInvocation > $PATH_RESULTS"script.log"

python repro_summary.py --fwhm 5 --cluster 64  --state 256  --xp_type $XP_TYPE $PATH_DATA $PATH_RESULTS &
python repro_summary.py --fwhm 5 --cluster 64  --state 512 --xp_type $XP_TYPE $PATH_DATA $PATH_RESULTS &
python repro_summary.py --fwhm 5 --cluster 256  --state 512 --xp_type $XP_TYPE $PATH_DATA $PATH_RESULTS &
python repro_summary.py --fwhm 5 --cluster 256  --state 1024 --xp_type $XP_TYPE $PATH_DATA $PATH_RESULTS &
