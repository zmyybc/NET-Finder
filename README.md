# NET-Finder: Automated Systematic Reaction Network Exploration

NET-Finder is an advanced computational tool designed for the automated and systematic search of reaction networks. It utilizes transition state theory and the dimer method to explore potential energy surfaces, starting from initial reactant structures.

## Features

- Automated transition state search using the dimer method
- Efficient reaction path optimization
- Filtering of duplicate and high-energy reaction paths
- Construction of comprehensive reaction networks
- Support for both local and SLURM-based computations
- Real-time monitoring of job progress
- Flexible integration with various atomic simulation environments

## Installation

### Prerequisites

- Python >= 3.8
- ASE (Atomic Simulation Environment)
- NumPy
- SciPy
- matplotlib
- psutil

### Installation Steps

1. Clone the NET-Finder repository:
   ```
   git clone https://github.com/your-username/NET-Finder.git
   cd NET-Finder
   ```
2. put net_finder to your python path.



## Documentation

For detailed documentation, please refer to the `docs` directory in this repository or visit our [Read the Docs page](https://net-finder.readthedocs.io/en/latest/).

## Usage Examples

You can find more detailed usage examples in the `tutorial` directory of this repository. 

## Contributing

We welcome contributions to NET-Finder! You can submit pull requests, report issues, or request features.

## License

NET-Finder is released under the GNU License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

This project builds upon the work of many in the computational chemistry and materials science communities. We are particularly grateful to:

- The developers of the Atomic Simulation Environment (ASE) [1]
- The Henkelman group at the University of Texas at Austin for their work on transition state theory methods [2,3]


## Contact

For questions, suggestions, or collaborations, please open an issue on this GitHub repository or contact the maintainers directly at [573683148@qq.com].

## References

[1] Ask, M., Larsen, A. H., Mortensen, J. J., et al. (2015). The Atomic Simulation Environment—A Python library for working with atoms. Journal of Physics: Condensed Matter, 29(27), 273002. https://doi.org/10.1088/1361-648X/aa680e

[2] Henkelman, G., Uberuaga, B. P., & Jónsson, H. (2000). A climbing image nudged elastic band method for finding saddle points and minimum energy paths. The Journal of Chemical Physics, 113(22), 9901-9904. https://doi.org/10.1063/1.1329672

[3] Henkelman, G., & Jónsson, H. (2000). Improved tangent estimate in the nudged elastic band method for finding minimum energy paths and saddle points. The Journal of Chemical Physics, 113(22), 9978-9985. https://doi.org/10.1063/1.1323224
