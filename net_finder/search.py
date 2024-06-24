import os
import numpy as np
from ase import Atoms
from ase.optimize import BFGS
from ase.dimer import DimerControl, MinModeAtoms, MinModeTranslate
from ase.io import read, write
from ase.io.trajectory import Trajectory
from .path import ReactionPath
from ase.constraints import FixAtoms
class Dimer:
    def __init__(self, atoms, calc, output_dir='dimer', dimer_params=None):
        self.atoms = atoms
        self.calc = calc
        self.output_dir = output_dir
        self.dimer_params = dimer_params or {}

    def run(self, fmax=0.05, steps=100):
        mask = [atom.index < self.dimer_params.get('fix_index', -1) for atom in self.atoms]
        self.atoms.set_constraint(FixAtoms(mask=mask))
        self.atoms.calc = self.calc
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        

        with DimerControl(
            initial_eigenmode_method='displacement',
            displacement_method=self.dimer_params.get('displacement_method', 'gauss'),
            displacement_center=self.dimer_params.get('displacement_center', 0),
            displacement_radius=self.dimer_params.get('displacement_radius', 5.0),
            dimer_separation=self.dimer_params.get('dimer_separation', 0.01),
            logfile=os.path.join(self.output_dir, 'dimer_control.log')
        ) as d_control:
          d_atoms = MinModeAtoms(self.atoms, d_control)
          d_atoms.displace()
          dimer_traj_file = os.path.join(self.output_dir, 'dimer_method.traj')
          dimer_log_file = os.path.join(self.output_dir, 'dimer_log')
          with MinModeTranslate(d_atoms, trajectory=dimer_traj_file, logfile= dimer_log_file) as dim_rlx:
              dim_rlx.run(fmax=fmax, steps=steps)
              poscar_file = os.path.join(self.output_dir, 'POSCAR')
              d_atoms.write(poscar_file)
              IS = read(poscar_file)
              FS = read(poscar_file)
      
              IS.calc = self.calc
              FS.calc = self.calc
              IS.positions += d_atoms.eigenmodes[0]
              FS.positions -= d_atoms.eigenmodes[0]
      
              is_traj_file = os.path.join(self.output_dir, 'IS.traj')
              fs_traj_file = os.path.join(self.output_dir, 'FS.traj')
              dyn1 = BFGS(IS, trajectory=is_traj_file)
              dyn2 = BFGS(FS, trajectory=fs_traj_file)
              dyn1.run(fmax=fmax, steps=steps)
              dyn2.run(fmax=fmax, steps=steps)
      
              traj = [IS, d_atoms, FS]
              directory = os.path.join(self.output_dir, 'traj')
              self._write_trajectories(traj, directory)
              ts_index = self._find_ts_index(traj)
              energies = self._get_energies(traj)
              reaction_path = ReactionPath(traj, energies, ts_index)
              reaction_path.save(self.output_dir)
              return reaction_path
    def _combine_trajectories(self, traj1, traj2):
        traj = []
        for i, atoms in enumerate(traj1):
            #if i % 4 == 0:
                traj.append(atoms)
        for i, atoms in enumerate(traj2):
            #if i % 4 == 0:
                traj.append(atoms)
        return traj
    def _get_energies(self, traj):
        energies = [atoms.get_potential_energy() for atoms in traj]
        return energies
    def _write_trajectories(self, traj, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

        for i, atoms in enumerate(traj):
            filename = f'{directory}/structure_{i}.vasp'
            atoms.write(filename)
            #write(filename, atoms)
    def _calculate_energy_barrier(self, traj, ts_index):
        if ts_index is not None:
            ts_energy = traj[ts_index].get_potential_energy()
            reactant_energy = traj[0].get_potential_energy()
            energy_barrier = ts_energy - reactant_energy
        else:
            energy_barrier = None
        return energy_barrier
    def _get_reaction_path(self, traj):
        ts_index = 1#self._find_ts_index(traj)
        reaction_path = ReactionPath(traj, ts_index)
        reaction_path.calculate_energy_barrier()
        return reaction_path

    def _find_ts_index(self, traj):
       # energies = [atoms.get_potential_energy() for atoms in traj]
       # ts_index = energies.index(max(energies))
        return 1
