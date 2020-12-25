#/bin/bash
myInvocation="$(printf %q "$BASH_SOURCE")$((($#)) && printf ' %q' "$@")"
export FWHM=$2
export PATH_RESULTS=$1'/repro_friends-s01'
export PATH_DATA=$1

echo Input data located in $PATH_DATA
echo Results will be saved in $PATH_RESULTS

python repro_summary.py --fwhm $FWHM --cluster 20  --state 60  $PATH_DATA $PATH_RESULTS &
python repro_summary.py --fwhm $FWHM --cluster 20  --state 120 $PATH_DATA $PATH_RESULTS &
python repro_summary.py --fwhm $FWHM --cluster 50  --state 150 $PATH_DATA $PATH_RESULTS &
python repro_summary.py --fwhm $FWHM --cluster 50  --state 300 $PATH_DATA $PATH_RESULTS &
python repro_summary.py --fwhm $FWHM --cluster 300 --state 900 $PATH_DATA $PATH_RESULTS &
