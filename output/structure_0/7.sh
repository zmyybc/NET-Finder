#!/bin/bash
#SBATCH --job-name=7
#SBATCH --output=output/structure_0/7.out
#SBATCH --error=output/structure_0/7.err
#SBATCH #SBATCH --nodes=1
#SBATCH --account=che190010
#SBATCH --ntasks=128
#SBATCH --time=12:00:00
#SBATCH --partition=shared
module load intel
python job.py config.json ./ 7
