import os
import subprocess
from .path import ReactionPath
from .search import Dimer
from .searchjob import TransitionStateJob
import pickle
import json
import time
import logging
import signal
import psutil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TransitionStateSearch:
    def __init__(self, initial_structures, calc, dimer_params=None, output_dir='./ts_search', run_mode='shell', trys=10, slurm_params=None):
        self.initial_structures = initial_structures
        self.calc = calc
        self.dimer_params = dimer_params or {}
        self.output_dir = output_dir
        self.run_mode = run_mode
        self.slurm_params = slurm_params or {}
        self.reaction_paths = []
        self.trys = trys

        logger.info(f'Initializing TransitionStateSearch with {len(initial_structures)} initial structures, output directory: {output_dir}, run mode: {run_mode}, number of tries: {trys}')

    def run(self, fmax=0.05, steps=100):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f'Created output directory: {self.output_dir}')

        jobs = []
        for i, initial_structure in enumerate(self.initial_structures):
            structure_dir = os.path.join(self.output_dir, f'structure_{i}')
            if not os.path.exists(structure_dir):
                os.makedirs(structure_dir)
                logger.info(f'Created directory for structure {i}: {structure_dir}')

            initial_structure.write(os.path.join(structure_dir, 'initial.vasp'))
            logger.info(f'Wrote initial structure {i} to {os.path.join(structure_dir, "initial.vasp")}')

            config = {
                'calculator_imports': self.calc['calculator_imports'],
                'calculator_setup': self.calc['calculator_setup'],
                'dimer_params': self.dimer_params,
                'fmax': fmax,
                'steps': steps,
            }
            config_file = os.path.join(structure_dir, 'config.json')
            with open(config_file, 'w') as f:
                json.dump(config, f)
            logger.info(f'Wrote configuration for structure {i} to {config_file}')

            for j in range(self.trys):
                job = TransitionStateJob(j, structure_dir, config_file, self.slurm_params if self.run_mode == 'slurm' else None)
                process_info = job.submit(str(j))
                if process_info is not None:
                    if self.run_mode == 'slurm':
                        job_id = process_info
                      #  print(job_id,"here!!!!!!!!!!")
                        jobs.append((job_id, f'structure_{i}_try_{j}'))
                    else:
                        pid = process_info
                        jobs.append((pid, f'structure_{i}_try_{j}'))
                logger.info(f'Submitted job for structure {i}, try {j}, PID: {pid if self.run_mode != "slurm" else "N/A"}')

        if self.run_mode == 'slurm':
            self._monitor_slurm_jobs(jobs)
        else:
            self._run_shell_jobs(jobs)
            
    def _monitor_slurm_jobs(self, jobs):
        completed_jobs = set()
        while len(completed_jobs) < len(jobs):
            for job_id, job_name in jobs:
                if job_name not in completed_jobs:
                    status = self.get_slurm_job_status(job_id)
                    if status == 'COMPLETED':
                        completed_jobs.add(job_name)
                        logger.info(f'Job {job_name} completed')
                    elif status == 'FAILED':
                        completed_jobs.add(job_name)
                        logger.warning(f'Job {job_name} failed')
                    else:
                        logger.info(f'Job {job_name} is {status}')
            time.sleep(3)  # 每3秒更新一次状态
    def _run_shell_jobs(self, jobs):
        completed_jobs = set()
        while len(completed_jobs) < len(jobs):
            for pid, job_name in jobs:
                if job_name in completed_jobs:
                    continue

                try:
                    process = psutil.Process(pid)
                    if process.is_running():
                        # 检查进程是否真的在运行，而不是僵尸进程
                        status = process.status()
                        if status == psutil.STATUS_ZOMBIE:
                            raise psutil.NoSuchProcess(pid)
                        logger.info(f'Job {job_name} (PID: {pid}) is still running')
                    else:
                        # 进程已结束，但我们需要获取退出代码
                        raise psutil.NoSuchProcess(pid)
                
                except psutil.NoSuchProcess:
                    completed_jobs.add(job_name)
                    try:
                        exit_code = process.wait(timeout=1)
                    except psutil.TimeoutExpired:
                        logger.warning(f'Could not get exit code for job {job_name} (PID: {pid})')
                        exit_code = None
                    
                    if exit_code == 0:
                        logger.info(f'Job {job_name} (PID: {pid}) completed successfully')
                    else:
                        logger.warning(f'Job {job_name} (PID: {pid}) failed with exit code {exit_code}')
                    
                    # 直接处理输出文件
                    stdout_file = f"{job_name}_stdout.log"
                    stderr_file = f"{job_name}_stderr.log"
                    
                    if os.path.exists(stdout_file):
                        with open(stdout_file, "r") as f:
                            stdout = f.read()
                        logger.debug(f'Stdout for {job_name}: {stdout}')
                    
                    if os.path.exists(stderr_file):
                        with open(stderr_file, "r") as f:
                            stderr = f.read()
                        logger.debug(f'Stderr for {job_name}: {stderr}')
                    
                    if not os.path.exists(stdout_file) and not os.path.exists(stderr_file):
                        logger.debug(f'Output logs not found for {job_name}')
                
                except Exception as e:
                    logger.error(f'Error monitoring job {job_name} (PID: {pid}): {str(e)}')
                    completed_jobs.add(job_name)
            
            time.sleep(3)  # 每3秒检查一次状态
    def get_slurm_job_status(self, job_id):
        try:
            output = subprocess.check_output(['squeue', '-j', str(job_id), '-h', '-o', '%T']).decode().strip()
            if output == '':
                return 'COMPLETED'
            else:
                return output
        except subprocess.CalledProcessError as e:
            if e.returncode == 1:
                return 'COMPLETED'
            else:
                return 'FAILED'

    def collect_reaction_paths(self):
        self.reaction_paths = []
        for i in range(len(self.initial_structures)):
            for j in range(self.trys):
                structure_dir = os.path.join(self.output_dir, f'structure_{i}')
                traj_file = os.path.join(structure_dir, str(j))
                if os.path.exists(traj_file):
                    traj_file_path = os.path.join(traj_file, 'reaction_path.json')
                    if os.path.exists(traj_file_path):
                        reaction_path = ReactionPath().load(traj_file)
                        self.reaction_paths.append(reaction_path)
                        logger.info(f'Loaded reaction path from {traj_file}')
                    else:
                        logger.warning(f'No reaction path found in {traj_file}. Skipping...')
                    
        logger.info(f'Collected {len(self.reaction_paths)} reaction paths')
        return self.reaction_paths

    def get_reaction_paths(self):
        return self.reaction_paths

    def save_reaction_paths(self, output_dir=None):
        output_dir = output_dir or self.output_dir
        for i, reaction_path in enumerate(self.reaction_paths):
            reaction_path.save(os.path.join(output_dir, f'path_{i}'))
            logger.info(f'Saved reaction path {i} to {os.path.join(output_dir, f"path_{i}")}')

    @staticmethod
    def load_reaction_paths(directory):
        reaction_paths = []
        for i in range(len(os.listdir(directory)) // 2):
            reaction_path = ReactionPath.load(os.path.join(directory, f'path_{i}'))
            reaction_paths.append(reaction_path)
            logger.info(f'Loaded reaction path from {os.path.join(directory, f"path_{i}")}')
        logger.info(f'Loaded {len(reaction_paths)} reaction paths from {directory}')
        return reaction_paths
