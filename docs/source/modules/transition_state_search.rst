TransitionStateSearch
=====================

.. currentmodule:: net_finder.paths

.. autoclass:: TransitionStateSearch
   :members:
   :undoc-members:
   :show-inheritance:

Overview
--------

The `TransitionStateSearch` class is a high-level component in NET-Finder that manages multiple transition state searches. It coordinates the execution of Dimer searches, handles job submission (locally or on a cluster), and collects results.

Key Features
------------

- Manages multiple transition state searches from different initial structures
- Supports both local execution and job submission to computing clusters (e.g., using SLURM)
- Provides methods for collecting and analyzing reaction paths from completed searches
- Allows customization of search parameters and computational resources

Basic Usage
-----------

Here's a basic example of how to use the `TransitionStateSearch` class:

.. code-block:: python

   from ase.io import read
   from net_finder.paths import TransitionStateSearch

   # Load initial structures
   initial_structures = [read(f'initial/structure_{i}.vasp') for i in range(3)]

   # Set up calculator configuration
   calc = {
       "calculator_imports": "from ase.calculators.vasp import Vasp",
       "calculator_setup": "calc = Vasp(xc='pbe', encut=400, kpts=(1, 1, 1))"
   }

   # Set up dimer parameters
   dimer_params = {
       'displacement_method': 'gauss',
       'displacement_radius': 2.0,
       'dimer_separation': 0.01
   }

   # Create TransitionStateSearch instance
   ts_search = TransitionStateSearch(initial_structures, calc, dimer_params,
                                     output_dir='ts_search_output', run_mode='local')

   # Run transition state searches
   ts_search.run(fmax=0.05, steps=100)

   # Collect reaction paths
   reaction_paths = ts_search.collect_reaction_paths()

Parameters
----------

- `initial_structures` (list of ase.Atoms): List of initial structures for transition state searches.
- `calc` (dict): Configuration for the calculator to be used in searches.
- `dimer_params` (dict): Parameters for the Dimer method.
- `output_dir` (str): Directory to store output files (default: './ts_search').
- `run_mode` (str): Execution mode, either 'local' or 'slurm' (default: 'local').
- `trys` (int): Number of attempts per initial structure (default: 10).
- `slurm_params` (dict): Parameters for SLURM job submission (if run_mode is 'slurm').

Methods
-------

.. automethod:: TransitionStateSearch.run

This method initiates the transition state searches for all initial structures.

Parameters:
  - `fmax` (float): Maximum force criterion for optimization.
  - `steps` (int): Maximum number of optimization steps.

.. automethod:: TransitionStateSearch.collect_reaction_paths

This method collects and returns the reaction paths from completed searches.

Returns:
  - List of ReactionPath objects.

.. automethod:: TransitionStateSearch.get_reaction_paths

Returns the currently collected reaction paths.

.. automethod:: TransitionStateSearch.save_reaction_paths

Saves the collected reaction paths to the specified directory.

Parameters:
  - `output_dir` (str, optional): Directory to save the reaction paths. If not specified, uses the instance's output_dir.

Advanced Usage
--------------

For more advanced usage, you can customize the search parameters and use cluster resources:

.. code-block:: python

   slurm_params = {
       'nodes': 1,
       'ntasks': 32,
       'time': '12:00:00',
       'partition': 'regular'
   }

   ts_search = TransitionStateSearch(initial_structures, calc, dimer_params,
                                     output_dir='ts_search_output', run_mode='slurm',
                                     trys=20, slurm_params=slurm_params)

   ts_search.run(fmax=0.01, steps=200)

   # Monitor job progress
   while not ts_search.all_jobs_completed():
       ts_search.print_job_status()
       time.sleep(60)  # Wait for 1 minute before checking again

   reaction_paths = ts_search.collect_reaction_paths()

   # Save collected reaction paths
   ts_search.save_reaction_paths('final_paths')

Integration with Other Modules
------------------------------

The TransitionStateSearch class is typically used as part of a larger workflow in NET-Finder:

.. code-block:: python

   from net_finder.net import ReactionNetwork

   # Run transition state searches
   ts_search = TransitionStateSearch(initial_structures, calc, dimer_params)
   ts_search.run()

   # Collect reaction paths and create a reaction network
   reaction_paths = ts_search.collect_reaction_paths()
   network = ReactionNetwork(reaction_paths)

   # Analyze the network
   network.generate_graph()

Notes
-----

- When using the 'slurm' run mode, ensure that your environment is properly configured for SLURM job submission.
- The number of tries (`trys` parameter) can significantly affect the likelihood of finding transition states, but also increases computational cost.
- For large-scale searches, consider implementing a database backend for efficient storage and retrieval of reaction paths.
- Monitor resource usage and adjust `slurm_params` as needed to optimize performance on your specific cluster setup.