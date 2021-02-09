#/bin/bash
myInvocation="$(printf %q "$BASH_SOURCE")$((($#)) && printf ' %q' "$@")"
export PATH_RESULTS=$1'/repro_friends-s01/'
export PATH_DATA=$1
export XP_TYPE=$2

echo Experiment type: $XP_TYPE
echo Input data located in $PATH_DATA
echo Results will be saved in $PATH_RESULTS

mkdir $PATH_RESULTS
echo $myInvocation > $PATH_RESULTS"script.log"

python repro_summary.py --fwhm 5 --cluster 20  --state 60  --xp_type $XP_TYPE $PATH_DATA $PATH_RESULTS &
python repro_summary.py --fwhm 5 --cluster 20  --state 120 --xp_type $XP_TYPE $PATH_DATA $PATH_RESULTS &
python repro_summary.py --fwhm 5 --cluster 50  --state 150 --xp_type $XP_TYPE $PATH_DATA $PATH_RESULTS &
python repro_summary.py --fwhm 5 --cluster 50  --state 300 --xp_type $XP_TYPE $PATH_DATA $PATH_RESULTS &
python repro_summary.py --fwhm 5 --cluster 300 --state 900 --xp_type $XP_TYPE $PATH_DATA $PATH_RESULTS &
if [[ "$XP_TYPE" != "friends-s01_clean_multi_fwhm" ]]; then
    python repro_summary.py --fwhm 8 --cluster 20  --state 60  --xp_type $XP_TYPE $PATH_DATA $PATH_RESULTS &
    python repro_summary.py --fwhm 8 --cluster 20  --state 120 --xp_type $XP_TYPE $PATH_DATA $PATH_RESULTS &
    python repro_summary.py --fwhm 8 --cluster 50  --state 150 --xp_type $XP_TYPE $PATH_DATA $PATH_RESULTS &
    python repro_summary.py --fwhm 8 --cluster 50  --state 300 --xp_type $XP_TYPE $PATH_DATA $PATH_RESULTS &
    python repro_summary.py --fwhm 8 --cluster 300 --state 900 --xp_type $XP_TYPE $PATH_DATA $PATH_RESULTS &
fi
