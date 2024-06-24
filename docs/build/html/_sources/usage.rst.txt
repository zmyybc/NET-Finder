Usage
=====

This guide provides instructions on how to use NET-Finder for your reaction network exploration tasks. We'll cover basic usage, configuration, and some advanced features.

Quick Start
-----------

To quickly familiarize yourself with NET-Finder, you can use the provided `main.py` script:

.. code-block:: bash

   python main.py

This will run a simple example using default parameters.

Basic Usage
-----------

1. Prepare Your Input Structures
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Prepare your initial structures in VASP format (.vasp files) and place them in an `initial` directory.

2. Create a Configuration File
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a configuration file (e.g., `config.json`) with your desired parameters:

.. code-block:: json

   {
     "calculator_imports": "from ase.calculators.vasp import Vasp",
     "calculator_setup": "calc = Vasp(xc='pbe', encut=400, icharg=1, ncore=32, kpts=(1, 1, 1), ismear=0, sigma=0.01, isym=0, ispin=2, nupdown=4, algo='fast', gamma=True, nsw=0, lwave=True, lcharg=True, nelm=200, ediff=0.0001)",
     "dimer_params": {
       "displacement_method": "gauss",
       "displacement_radius": 2.0,
       "dimer_separation": 0.01
     },
     "slurm_params": {
       "nodes": 1,
       "account": "your_account",
       "ntasks": 128,
       "time": "12:00:00",
       "partition": "shared"
     }
   }

3. Run NET-Finder
^^^^^^^^^^^^^^^^^

Create a Python script to run NET-Finder:

.. code-block:: python

   from ase.io import read
   from net_finder.paths import TransitionStateSearch
   from net_finder.net import ReactionNetwork

   # Load initial structures
   initial_structures = [read(f'initial/structure_{i}.vasp') for i in range(3)]

   # Set up calculator and parameters
   calc = {
       "calculator_imports": "from ase.calculators.vasp import Vasp",
       "calculator_setup": "calc = Vasp(xc='pbe', encut=400, icharg=1, ncore=32, kpts=(1, 1, 1), ismear=0, sigma=0.01, isym=0, ispin=2, nupdown=4, algo='fast', gamma=True, nsw=0, lwave=True, lcharg=True, nelm=200, ediff=0.0001)"
   }

   dimer_params = {
       'displacement_method': 'gauss',
       'displacement_radius': 2.0,
       'dimer_separation': 0.01,
   }

   slurm_params = {
       'nodes': 1,
       'account': 'your_account',
       'ntasks': 128,
       'time': '12:00:00',
       'partition': 'shared',
   }

   # Run transition state search
   ts_search = TransitionStateSearch(initial_structures, calc, dimer_params, output_dir='ts_search_output', run_mode='slurm', slurm_params=slurm_params)
   ts_search.run(fmax=0.05, steps=100)

   # Collect reaction paths and generate network
   reaction_paths = ts_search.collect_reaction_paths()
   network = ReactionNetwork(reaction_paths, energy_cutoff=-22.5)
   network.generate_graph(output_dir='reaction_network_output')

Run this script to start the NET-Finder calculation:

.. code-block:: bash

   python run_net_finder.py

Advanced Usage
--------------

Customizing Dimer Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can customize the dimer method parameters to fine-tune the transition state search:

.. code-block:: python

   dimer_params = {
       'displacement_method': 'gauss',
       'displacement_radius': 2.5,
       'dimer_separation': 0.005,
       'fix_index': 10  # Fix atoms with index less than 10
   }

Using Different Calculators
^^^^^^^^^^^^^^^^^^^^^^^^^^^

NET-Finder supports various ASE calculators. Here's an example using EMT:

.. code-block:: python

   from ase.calculators.emt import EMT

   calc = {
       "calculator_imports": "from ase.calculators.emt import EMT",
       "calculator_setup": "calc = EMT()"
   }

Analyzing Results
-----------------

After running NET-Finder, you can analyze the results:

1. Check the `ts_search_output` directory for individual transition state searches.
2. Examine the `reaction_network_output` directory for the generated reaction network graph and related files.
3. Use the `ReactionNetwork` class methods to further analyze the network:

   .. code-block:: python

      # Get all unique species in the network
      unique_species = network.get_unique_species()

      # Get all reaction paths
      all_paths = network.get_reaction_paths()

      # Get the lowest energy path between two species
      lowest_path = network.get_lowest_energy_path(start_species, end_species)

Visualizing the Network
^^^^^^^^^^^^^^^^^^^^^^^

NET-Finder generates a network graph in the `reaction_network_output` directory. You can visualize this graph using various tools:

1. Open the generated PNG file directly.
2. Use network visualization libraries like NetworkX with matplotlib for more advanced visualizations:

   .. code-block:: python

      import networkx as nx
      import matplotlib.pyplot as plt

      G = network.graph
      pos = nx.spring_layout(G)
      nx.draw(G, pos, with_labels=True)
      plt.show()

Troubleshooting
---------------

If you encounter issues while using NET-Finder:

1. Check the log files in the output directories for error messages.
2. Verify that your input structures are correctly formatted.
3. Ensure that the calculator is properly set up and all required files (e.g., POTCAR for VASP) are present.
4. If using SLURM, check the SLURM output files for any job-related issues.

For persistent problems, please open an issue on the NET-Finder GitHub repository with a detailed description of the problem and relevant log files.