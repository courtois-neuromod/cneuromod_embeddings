#!/bin/bash
#SBATCH --account=rrg-pbellec
#SBATCH --mail-user=l1g5o4b4c8u9i6v6@simexp.slack.com
#SBATCH --mail-type=END,FAIL
#SBATCH --time=00:45:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=20G
#SBATCH --output "output/slurm/bids_save_output_%A_%a.out"

python tools/save_bids_layout.py
