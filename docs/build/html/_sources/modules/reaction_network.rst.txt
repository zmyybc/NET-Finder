ReactionNetwork
===============

.. currentmodule:: net_finder.net

.. autoclass:: ReactionNetwork
   :members:
   :undoc-members:
   :show-inheritance:

Overview
--------

The `ReactionNetwork` class is a crucial component in NET-Finder that constructs and analyzes reaction networks based on the collected reaction paths. It provides methods for network visualization, path analysis, and identification of key reaction routes.

Key Features
------------

- Constructs a reaction network from a set of reaction paths
- Filters reaction paths based on energy criteria
- Generates network graphs for visualization
- Provides methods for analyzing network properties and finding important paths
- Supports export of network data for further analysis

Basic Usage
-----------

Here's a basic example of how to use the `ReactionNetwork` class:

.. code-block:: python

   from net_finder.net import ReactionNetwork
   from net_finder.path import ReactionPath

   # Assume we have a list of ReactionPath objects
   reaction_paths = [...]  # List of ReactionPath objects

   # Create ReactionNetwork instance
   network = ReactionNetwork(reaction_paths, energy_cutoff=-22.5)

   # Generate and save the network graph
   network.generate_graph(output_dir='reaction_network_output')

   # Analyze the network
   unique_species = network.get_unique_species()
   lowest_energy_path = network.get_lowest_energy_path(start_species, end_species)

Parameters
----------

- `reaction_paths` (list of ReactionPath): List of reaction paths to construct the network.
- `energy_cutoff` (float, optional): Maximum energy threshold for including reactions.
- `structure_diff_threshold` (float, optional): Threshold for considering structures as similar (default: 0.1).

Methods
-------

.. automethod:: ReactionNetwork.generate_graph

Generates and saves the reaction network graph.

Parameters:
  - `output_dir` (str): Directory to save the generated graph and related files.

.. automethod:: ReactionNetwork.get_unique_species

Returns a list of unique species (structures) in the network.

.. automethod:: ReactionNetwork.get_reaction_paths

Returns all reaction paths in the network.

.. automethod:: ReactionNetwork.get_lowest_energy_path

Finds the lowest energy path between two species.

Parameters:
  - `start_species` (ase.Atoms): Starting species structure.
  - `end_species` (ase.Atoms): End species structure.

Returns:
  - List of ReactionPath objects representing the lowest energy path.

Advanced Usage
--------------

For more advanced analysis of the reaction network:

.. code-block:: python

   # Find all paths between two species
   all_paths = network.find_all_paths(start_species, end_species)

   # Identify rate-limiting steps
   rate_limiting_steps = network.identify_rate_limiting_steps()

   # Calculate network properties
   connectivity = network.calculate_connectivity()
   centrality = network.calculate_centrality()

   # Export network data for external analysis
   network.export_to_graphml('network.graphml')

Visualization
-------------

The `generate_graph` method creates a visual representation of the reaction network:

.. code-block:: python

   network.generate_graph(output_dir='network_visualization')

This generates:
- A PNG file of the network graph
- Individual structure files for each unique species
- A detailed log of the network generation process

You can customize the appearance of the graph:

.. code-block:: python

   network.generate_graph(output_dir='custom_network',
                          node_size=1000,
                          edge_width=2,
                          font_size=12)

Integration with Other Modules
------------------------------

The ReactionNetwork class is typically used as the final step in a NET-Finder workflow:

.. code-block:: python

   from net_finder.paths import TransitionStateSearch

   # Run transition state searches
   ts_search = TransitionStateSearch(initial_structures, calc, dimer_params)
   ts_search.run()

   # Collect reaction paths
   reaction_paths = ts_search.collect_reaction_paths()

   # Create and analyze the reaction network
   network = ReactionNetwork(reaction_paths, energy_cutoff=-22.5)
   network.generate_graph()

   # Perform further analysis
   key_intermediates = network.identify_key_intermediates()
   dominant_pathways = network.find_dominant_pathways(start, end)

Notes
-----

- The energy cutoff parameter can significantly affect the complexity of the resulting network. Adjust it carefully to balance between completeness and manageability.
- For large networks, graph generation and some analysis methods may be computationally intensive. Consider using sampling or filtering techniques for very large datasets.
- The structure comparison used to identify unique species is based on RMSD. Adjust the `structure_diff_threshold` if needed for your specific system.
- While the generated graph provides a good overview, consider using specialized network analysis tools for more advanced analyses of large or complex networks.