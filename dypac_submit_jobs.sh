#!/bin/bash
#SBATCH --account=rrg-pbellec
#SBATCH --job-name=dypac_job
#SBATCH --mail-type=END,FAIL
#SBATCH --time=30:00:00
#SBATCH --cpus-per-task=25
#SBATCH --mem=60G
#SBATCH --output=dypac_output.out

module load python/3.6
source ~/hanad_env/bin/activate
bash dypac_jobs.sh
