# PlasFlowSolver
Version 2.0.0

Written by Domenico Lanza

PlasFlowSolver is a Python-based data reduction code designed to determine free-stream flow conditions—such as enthalpy—in inductively coupled plasma (ICP) wind tunnel experiments. By integrating experimental measurements (static pressure, stagnation pressure, heat flux) with theoretical models, it solves the equilibrium boundary layer equations at the stagnation point of an axisymmetric body. The solver leverages [Mutation++](https://github.com/mutationpp/Mutationpp) as its thermodynamics library. The result is a characterization of the flow’s thermophysical properties, including temperature, density, Mach number, and species composition.

For any doubt or suggestion, please contact me at lanza3@illinois.edu

## Requirements

- **Python:** Version 3.10+ recommended
- **Dependencies:**
  - `numpy`
  - `scipy`
  - `mutationpp`
  - `h5py`
  - `openpyxl`
  - `pandas`
