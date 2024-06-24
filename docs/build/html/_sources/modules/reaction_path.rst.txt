ReactionPath
============

.. currentmodule:: net_finder.path

.. autoclass:: ReactionPath
   :members:
   :undoc-members:
   :show-inheritance:

Overview
--------

The `ReactionPath` class is a central component in NET-Finder, representing a complete reaction pathway including reactants, products, and the transition state. It provides methods for storing, analyzing, and manipulating reaction path data.

Key Features
------------

- Stores structures and energies for reactants, products, and transition states
- Provides easy access to key reaction properties (e.g., activation energy, reaction energy)
- Supports saving and loading reaction paths to/from files
- Offers methods for reaction path analysis and manipulation

Basic Usage
-----------

Here's a basic example of how to create and use a `ReactionPath` object:

.. code-block:: python

   from ase import Atoms
   from net_finder.path import ReactionPath

   # Create sample structures (normally these would come from calculations)
   reactant = Atoms('H2O')
   product = Atoms('H2 + O')
   transition_state = Atoms('H-H-O')

   # Create energies (normally these would come from calculations)
   energies = [-10.0, -5.0, -8.0]  # reactant, transition state, product

   # Create ReactionPath instance
   reaction_path = ReactionPath(structures=[reactant, transition_state, product],
                                energies=energies,
                                ts_index=1)

   # Access reaction properties
   activation_energy = reaction_path.activation_energy
   reaction_energy = reaction_path.reaction_energy

   # Save reaction path to file
   reaction_path.save('path_data')

   # Load reaction path from file
   loaded_path = ReactionPath.load('path_data')

Attributes
----------

- `structures` (list of ase.Atoms): List of atomic structures along the reaction path.
- `energies` (list of float): List of energies corresponding to each structure.
- `ts_index` (int): Index of the transition state in the structures list.

Properties
----------

.. autoproperty:: ReactionPath.reactant

.. autoproperty:: ReactionPath.product

.. autoproperty:: ReactionPath.transition_state

.. autoproperty:: ReactionPath.reactant_energy

.. autoproperty:: ReactionPath.product_energy

.. autoproperty:: ReactionPath.transition_state_energy

.. autoproperty:: ReactionPath.activation_energy

.. autoproperty:: ReactionPath.reaction_energy

Methods
-------

.. automethod:: ReactionPath.to_dict

.. automethod:: ReactionPath.save

.. automethod:: ReactionPath.load

Advanced Usage
--------------

You can perform more advanced operations on ReactionPath objects:

.. code-block:: python

   # Reverse the reaction path
   reversed_path = reaction_path.reverse()

   # Interpolate additional points along the path
   interpolated_path = reaction_path.interpolate(num_points=10)

   # Calculate the reaction coordinate
   reaction_coordinates = reaction_path.get_reaction_coordinate()

   # Plot the energy profile
   reaction_path.plot_energy_profile()

Integrating with Other Modules
------------------------------

ReactionPath objects are typically created by the Dimer class after a successful transition state search:

.. code-block:: python

   from net_finder.search import Dimer

   dimer = Dimer(atoms, calculator)
   reaction_path = dimer.run()

They are also used extensively in the ReactionNetwork class to build and analyze the full reaction network:

.. code-block:: python

   from net_finder.net import ReactionNetwork

   network = ReactionNetwork([reaction_path1, reaction_path2, ...])
   network.analyze()

Notes
-----

- The `structures` list should always contain at least two structures (reactant and product). If a transition state is known, it should be included as well.
- The `ts_index` should correspond to the index of the transition state in the `structures` list. If no transition state is known, set `ts_index` to None.
- When saving large numbers of ReactionPath objects, consider using a database system for efficient storage and retrieval.