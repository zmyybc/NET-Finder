#!/bin/bash
#SBATCH --job-name=5
#SBATCH --output=output/structure_3/5.out
#SBATCH --error=output/structure_3/5.err
#SBATCH #SBATCH --nodes=1
#SBATCH --account=che190010
#SBATCH --ntasks=128
#SBATCH --time=12:00:00
#SBATCH --partition=shared
module load intel
python job.py config.json ./ 5
