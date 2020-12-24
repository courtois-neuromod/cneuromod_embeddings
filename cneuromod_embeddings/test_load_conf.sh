#!/bin/bash
#SBATCH --account=rrg-pbellec
#SBATCH --mail-user=l1g5o4b4c8u9i6v6@simexp.slack.com
#SBATCH --mail-type=END,FAIL
#SBATCH --time=00:30:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=20G
#SBATCH --output "output/slurm/test_%A.out"

python test_conf_load.py
