Introduction
============

NET-Finder (Network Explorer for Transition states and Intermediates) is an advanced computational tool designed for the automated and systematic search of reaction networks. It utilizes transition state theory and the dimer method to explore potential energy surfaces, starting from initial reactant structures.

Key Features
------------

- Automated transition state search using the dimer method
- Reaction path optimization
- Filtering of duplicate and high-energy reaction paths
- Construction of comprehensive reaction networks
- Optional network expansion for extensive exploration

Theory
------

NET-Finder's core functionality is based on transition state theory and employs the dimer method for transition state searches. The program follows these key steps:

1. **Initial Structure Input**: The program accepts a set of initial structures as input. These structures serve as the starting points for the reaction network exploration.

2. **Transition State Search**: For each input structure, NET-Finder performs multiple transition state searches using the dimer method. The dimer method is an efficient algorithm for finding saddle points on the potential energy surface without requiring an initial guess for the transition state geometry.

3. **Reaction Path Optimization**: From each identified transition state, the program optimizes along the eigenvector in both directions to obtain complete reaction paths. This step connects the transition state to its corresponding reactant and product states.

4. **Path Filtering**: Duplicate and high-energy reaction paths are filtered out to focus on the most relevant chemical transformations. This step helps to reduce computational overhead and simplify the resulting reaction network.

5. **Network Construction**: The remaining paths are connected to form a comprehensive reaction network. This network represents the possible reaction pathways and intermediates in the chemical system under study.

6. **Network Expansion**: Optionally, all nodes in the generated network can be used as inputs for further searches, allowing for the exploration of more extensive reaction networks. This iterative process can reveal complex reaction mechanisms and unexpected intermediates.

By automating these steps, NET-Finder enables researchers to efficiently explore complex reaction landscapes and discover new reaction pathways that might be challenging to predict or identify manually.