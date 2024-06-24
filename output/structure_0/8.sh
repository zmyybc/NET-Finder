#!/bin/bash
#SBATCH --job-name=8
#SBATCH --output=output/structure_0/8.out
#SBATCH --error=output/structure_0/8.err
#SBATCH #SBATCH --nodes=1
#SBATCH --account=che190010
#SBATCH --ntasks=128
#SBATCH --time=12:00:00
#SBATCH --partition=shared
module load intel
python job.py config.json ./ 8
