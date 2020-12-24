#!/bin/bash
#SBATCH --account=rrg-pbellec
#SBATCH --mail-user=l1g5o4b4c8u9i6v6@simexp.slack.com
#SBATCH --mail-type=END,FAIL
#SBATCH --time=00:30:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=6G
#SBATCH --output "output/slurm/fuse_%A.out"

python tools/fuse_r2_files.py