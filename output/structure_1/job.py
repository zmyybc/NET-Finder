
import os
import sys
import json
from ase.io import read, write
from net_finder.search import Dimer
from ase.calculators.emt import EMT

if len(sys.argv) != 4:
    print("Usage: python job.py <config_file> <structure_dir> <i>")
    sys.exit(1)

config_file = sys.argv[1]
structure_dir = sys.argv[2]
i = sys.argv[3]

with open(config_file, 'r') as f:
    config = json.load(f)

if not os.path.exists(i):
    os.makedirs(i)

atoms = read(os.path.join(structure_dir, 'initial.vasp'))

calc = EMT()

calc.set(directory=i)
dimer = Dimer(atoms, calc, output_dir=i, dimer_params=config['dimer_params'])
traj = dimer.run(fmax=config['fmax'], steps=config['steps'])
