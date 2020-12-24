#!/bin/bash
#SBATCH --account=rrg-pbellec
#SBATCH --mail-user=l1g5o4b4c8u9i6v6@simexp.slack.com
#SBATCH --mail-type=END,FAIL
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=25
#SBATCH --mem=60G
#SBATCH --array=1-12
#SBATCH --output "output/slurm/dypac_output_%A_%a.out"

sed -n "$SLURM_ARRAY_TASK_ID p" < dypac_jobs.sh | bash
