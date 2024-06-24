import os
import subprocess

class SlurmJob:
    def __init__(self, script, job_name, output_dir, slurm_params=None, command_line_args=None):
        self.script = script
        self.job_name = job_name
        self.output_dir = output_dir
        self.slurm_params = slurm_params or {}
        self.command_line_args = command_line_args

    def submit(self):
        script_path = self._write_script()
        job_id = self._submit_script(script_path)
      #  print(job_id)
        return job_id

    def _write_script(self):
        script_path = os.path.join(self.output_dir, f'{self.job_name}.sh')
        with open(script_path, 'w') as f:
            f.write(self._generate_script())
        return script_path

    def _generate_script(self):
        return f"""#!/bin/bash
#SBATCH --job-name={self.job_name}
#SBATCH --output={self.output_dir}/{self.job_name}.out
#SBATCH --error={self.output_dir}/{self.job_name}.err
#SBATCH {self._get_slurm_params_str()}
module load intel
python job.py {self.command_line_args[0]} {self.command_line_args[1]} {self.command_line_args[2]}
"""

    def _get_slurm_params_str(self):
        return '\n'.join(f'#SBATCH --{k}={v}' for k, v in self.slurm_params.items())

    def _submit_script(self, script_path):
        result = subprocess.run(['sbatch', f'{self.job_name}.sh'], cwd=self.output_dir, capture_output=True, text=True)
        if result.returncode == 0:
            
            output_lines = result.stdout.strip().split('\n')
           # print(output_lines)
            job_id_line = output_lines[-1]
            job_id = job_id_line.split()[-1]
            return job_id
        else:
            print(f"Error submitting job: {result.stderr}")
            return None