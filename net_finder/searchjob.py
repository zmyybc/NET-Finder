import os
import sys
import json
import subprocess
import threading
from ase.io import read, write

class TransitionStateJob:
    def __init__(self, i, structure_dir, config_file, slurm_params=None):
        self.structure_dir = structure_dir
        self.config_file = config_file
        self.slurm_params = slurm_params or {}
        self.i = i

    def submit(self, name):
        with open(self.config_file, 'r') as f:
            config = json.load(f)
        
        script = f"""
import os
import sys
import json
from ase.io import read, write
from net_finder.search import Dimer
{config['calculator_imports']}

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

{config['calculator_setup']}

calc.set(directory=i)
dimer = Dimer(atoms, calc, output_dir=i, dimer_params=config['dimer_params'])
traj = dimer.run(fmax=config['fmax'], steps=config['steps'])
"""

        if self.slurm_params:
            return self.submit_slurm_job(name, script)
        else:
            return self.submit_shell_job(script)

    def submit_slurm_job(self, name, script):
        from .jobs import SlurmJob
        script_path = os.path.join(self.structure_dir, 'job.py')
        with open(script_path, 'w') as f:
            f.write(script)
        job = SlurmJob(script, name, self.structure_dir, self.slurm_params, command_line_args=['config.json', './', self.i])
        return job.submit()
            
    def submit_shell_job(self, script):
        
        script_path = os.path.join(self.structure_dir, 'job.py')
        print(script_path)
        with open(script_path, 'w') as f:
            f.write(script)
        cmd = [sys.executable, 'job.py', 'config.json', './', str(self.i)]
        
        process = subprocess.Popen(
            cmd,
            cwd=self.structure_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # 创建线程来异步读取输出
       # stdout_thread = threading.Thread(target=self.read_output, args=(process.stdout, "STDOUT"))
        stderr_thread = threading.Thread(target=self.read_output, args=(process.stderr, "STDERR"))
        
      #  stdout_thread.start()
        stderr_thread.start()
        
        return process.pid

    def read_output(self, pipe, pipe_name):
        for line in pipe:
            print(f"{pipe_name}: {line.strip()}")