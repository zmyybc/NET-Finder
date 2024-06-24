Dimer
=====

.. currentmodule:: net_finder.search

.. autoclass:: Dimer
   :members:
   :undoc-members:
   :show-inheritance:

Overview
--------

The `Dimer` class is a core component of NET-Finder, responsible for performing transition state searches using the dimer method. This method is an efficient algorithm for finding saddle points on potential energy surfaces without requiring an initial guess for the transition state geometry.

Key Features
------------

- Implements the dimer method for transition state search
- Supports various displacement methods for initial dimer orientation
- Allows for customization of dimer parameters
- Performs reaction path optimization from identified transition states

Basic Usage
-----------

Here's a basic example of how to use the `Dimer` class:

.. code-block:: python

   from ase.io import read
   from ase.calculators.emt import EMT
   from net_finder.search import Dimer

   # Load initial structure
   atoms = read('initial_structure.vasp')

   # Set up calculator
   calc = EMT()

   # Set up dimer parameters
   dimer_params = {
       'displacement_method': 'gauss',
       'displacement_radius': 2.0,
       'dimer_separation': 0.01
   }

   # Create Dimer instance
   dimer = Dimer(atoms, calc, output_dir='dimer_output', dimer_params=dimer_params)

   # Run dimer method
   reaction_path = dimer.run(fmax=0.05, steps=100)

Parameters
----------

- `atoms` (ase.Atoms): The initial atomic structure.
- `calc` (ase.calculators.Calculator): The ASE calculator to use for energy and force calculations.
- `output_dir` (str): Directory to store output files.
- `dimer_params` (dict): Dictionary of dimer method parameters.

  - `displacement_method` (str): Method for initial displacement ('gauss', 'random', etc.).
  - `displacement_radius` (float): Radius for the initial displacement.
  - `dimer_separation` (float): Separation distance between dimer images.
  - `fix_index` (int, optional): Fix atoms with index less than this value.

Methods
-------

.. automethod:: Dimer.run

This method performs the dimer search and returns a `ReactionPath` object.

Parameters:
  - `fmax` (float): Maximum force criterion for optimization.
  - `steps` (int): Maximum number of optimization steps.

Returns:
  - `ReactionPath`: Object containing the optimized reaction path.

Advanced Usage
--------------

For more advanced usage, you can customize the dimer parameters to suit your specific system:

.. code-block:: python

   dimer_params = {
       'displacement_method': 'random',
       'displacement_radius': 1.5,
       'dimer_separation': 0.005,
       'fix_index': 10  # Fix the first 10 atoms
   }

   dimer = Dimer(atoms, calc, output_dir='custom_dimer_output', dimer_params=dimer_params)

You can also access intermediate results and trajectories from the `Dimer` instance after running:

.. code-block:: python

   reaction_path = dimer.run(fmax=0.05, steps=100)
   
   # Access transition state structure
   ts_structure = reaction_path.transition_state

   # Access reaction path energies
   energies = reaction_path.energies

   # Access full trajectory
   trajectory = dimer.get_trajectory()

Notes
-----

- The dimer method can be sensitive to initial conditions. If you're not finding the desired transition state, try adjusting the `displacement_radius` or using a different `displacement_method`.
- For systems with rigid parts (e.g., a surface), use the `fix_index` parameter to keep part of the structure fixed during the search.
- The `run` method can be computationally intensive for large systems or accurate calculators. Consider using parallel computing resources when available.