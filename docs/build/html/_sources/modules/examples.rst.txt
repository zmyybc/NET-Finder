Examples
========

This section provides comprehensive examples of using NET-Finder for various reaction network exploration tasks. These examples demonstrate how to set up and run calculations, analyze results, and interpret the output.

Basic Reaction Network Exploration
----------------------------------

This example shows how to set up a basic reaction network exploration for a simple system.

.. code-block:: python

   from ase.build import molecule
   from ase.calculators.emt import EMT
   from net_finder.paths import TransitionStateSearch
   from net_finder.net import ReactionNetwork

   # Create initial structures
   initial_structures = [
       molecule('H2O'),
       molecule('H2'),
       molecule('O2')
   ]

   # Set up calculator
   calc = {
       "calculator_imports": "from ase.calculators.emt import EMT",
       "calculator_setup": "calc = EMT()"
   }

   # Set up dimer parameters
   dimer_params = {
       'displacement_method': 'gauss',
       'displacement_radius': 0.5,
       'dimer_separation': 0.01
   }

   # Create TransitionStateSearch instance
   ts_search = TransitionStateSearch(initial_structures, calc, dimer_params,
                                     output_dir='water_formation', run_mode='local')

   # Run transition state searches
   ts_search.run(fmax=0.05, steps=100)

   # Collect reaction paths
   reaction_paths = ts_search.collect_reaction_paths()

   # Create and analyze reaction network
   network = ReactionNetwork(reaction_paths, energy_cutoff=-5.0)
   network.generate_graph(output_dir='water_formation_network')

   # Analyze results
   unique_species = network.get_unique_species()
   print(f"Number of unique species: {len(unique_species)}")

   for i, species in enumerate(unique_species):
       print(f"Species {i}: {species.get_chemical_formula()}")

   # Find lowest energy path between H2 + O2 and H2O
   start = molecule('H2') + molecule('O2')
   end = molecule('H2O')
   lowest_path = network.get_lowest_energy_path(start, end)

   if lowest_path:
       print("Lowest energy path:")
       for step in lowest_path:
           print(f"  {step.reactant.get_chemical_formula()} -> {step.product.get_chemical_formula()}")
           print(f"  Activation energy: {step.activation_energy:.2f} eV")
   else:
       print("No path found between specified species.")

Surface Reaction Network
------------------------

This example demonstrates how to explore a reaction network on a catalyst surface.

.. code-block:: python

   from ase.build import fcc111, add_adsorbate
   from ase.calculators.vasp import Vasp
   from net_finder.paths import TransitionStateSearch
   from net_finder.net import ReactionNetwork

   # Create initial structures
   slab = fcc111('Pt', size=(3,3,4), vacuum=10.0)
   
   structures = []
   # CO adsorbed
   co_ads = slab.copy()
   add_adsorbate(co_ads, 'CO', 2.0, 'ontop')
   structures.append(co_ads)
   
   # O adsorbed
   o_ads = slab.copy()
   add_adsorbate(o_ads, 'O', 1.5, 'fcc')
   structures.append(o_ads)
   
   # CO and O co-adsorbed
   co_o_ads = slab.copy()
   add_adsorbate(co_o_ads, 'CO', 2.0, 'ontop')
   add_adsorbate(co_o_ads, 'O', 1.5, 'fcc')
   structures.append(co_o_ads)

   # Set up VASP calculator
   calc = {
       "calculator_imports": "from ase.calculators.vasp import Vasp",
       "calculator_setup": """calc = Vasp(xc='PBE', encut=400, kpts=(3,3,1),
                              ismear=0, sigma=0.1, ibrion=-1, nsw=0,
                              ldau=True, ldautype=2, ldauu={'Pt':2}, ldaul={'Pt':2},
                              luse_vdw=True, aggac=0.0)"""
   }

   # Set up dimer parameters
   dimer_params = {
       'displacement_method': 'gauss',
       'displacement_radius': 0.5,
       'dimer_separation': 0.01,
       'fix_index': len(slab)  # Fix slab atoms
   }

   # Create TransitionStateSearch instance
   ts_search = TransitionStateSearch(structures, calc, dimer_params,
                                     output_dir='co_oxidation', run_mode='slurm',
                                     slurm_params={'nodes': 1, 'ntasks': 24, 'time': '24:00:00'})

   # Run transition state searches
   ts_search.run(fmax=0.05, steps=200)

   # Collect reaction paths
   reaction_paths = ts_search.collect_reaction_paths()

   # Create and analyze reaction network
   network = ReactionNetwork(reaction_paths, energy_cutoff=-7.0)
   network.generate_graph(output_dir='co_oxidation_network')

   # Analyze results
   print("Unique intermediates:")
   for species in network.get_unique_species():
       print(f"  {species.get_chemical_formula(mode='metal')}")

   # Find all paths for CO oxidation
   co_o_start = co_o_ads
   co2_end = slab.copy()
   add_adsorbate(co2_end, 'CO2', 3.0, 'ontop')

   all_paths = network.find_all_paths(co_o_start, co2_end)
   print(f"\nFound {len(all_paths)} paths for CO oxidation")

   # Print details of the shortest path
   if all_paths:
       shortest_path = min(all_paths, key=len)
       print("\nShortest path for CO oxidation:")
       for step in shortest_path:
           print(f"  {step.reactant.get_chemical_formula(mode='metal')} -> "
                 f"{step.product.get_chemical_formula(mode='metal')}")
           print(f"  Activation energy: {step.activation_energy:.2f} eV")
   else:
       print("No paths found for CO oxidation")

Notes on Examples
-----------------

- The first example uses the EMT calculator for demonstration purposes. For real systems, more accurate calculators like VASP, GPAW, or Quantum ESPRESSO should be used.
- The surface reaction example uses VASP and includes some advanced settings like U-J corrections and van der Waals interactions. Adjust these settings according to your specific system and computational resources.
- When using SLURM for job submission, make sure to adjust the SLURM parameters according to your cluster's configuration and the computational demands of your system.
- The energy cutoff values used in these examples (-5.0 eV and -7.0 eV) are arbitrary. You should choose appropriate values based on the energy scale of your specific system.
- These examples demonstrate basic usage. For more complex systems or detailed analyses, you may need to use additional features of NET-Finder or combine it with other computational tools.