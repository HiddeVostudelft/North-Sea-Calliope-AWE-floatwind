#!/bin/sh

#SBATCH --partition=compute
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=64G
#SBATCH --mail-type=END
#SBATCH --account=research-tpm-ess

srun 2050_6_9_2015.py