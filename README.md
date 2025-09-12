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

## License

This software is open source and free.  
It is distributed under the terms of the **GNU General Public License v3.0** (GPLv3) 
and the **GNU Lesser General Public License v3.0** (LGPLv3).  

- The main application code is released under the [GPLv3](COPYING).  
- The library components are released under the [LGPLv3](COPYING.LESSER).  

© 2023-2025 The Board of Trustees of the University of Illinois. All rights reserved.

## Citing PlasFlowSolver

Please cite the following article when mentioning Mutation++ in your own papers.

* Lanza et al. [PlasFlowSolver: An Aerothermodynamic Data Reduction Model for Inductively Coupled Plasma Wind Tunnel Facilities](https://arc.aiaa.org/doi/abs/10.2514/6.2025-0449) *AIAA SciTech 2025 Conference*.

**Bibtex**
```bibtex
@inbook{doi:10.2514/6.2025-0449,
author = {Domenico Lanza and Massimo Franco and Gregory Elliott and Marco Panesi and Francesco Panerai},
title = {PlasFlowSolver: An Aerothermodynamic Data Reduction Model for Inductively Coupled Plasma Wind Tunnel Facilities},
booktitle = {AIAA SCITECH 2025 Forum},
chapter = {},
pages = {},
doi = {10.2514/6.2025-0449},
URL = {https://arc.aiaa.org/doi/abs/10.2514/6.2025-0449},
eprint = {https://arc.aiaa.org/doi/pdf/10.2514/6.2025-0449},
abstract = { Aerothermodynamic data reduction models are useful tools for analyzing experiments in high-enthalpy plasma wind tunnels, which are essential for evaluating materials used in hypersonic and reentry applications. This study introduces PlasFlowSolver, a data reduction model developed to estimate flow properties such as temperature, enthalpy, and velocity from experimental data, including pressure, stagnation pressure, and stagnation-point cold-wall heat flux. The model is based on boundary layer theory and assumes thermochemical equilibrium, providing an engineering framework for efficient analysis. The model assumptions and the computation of the stagnation-point cold-wall heat flux are thoroughly discussed. Sensitivity analyses of input parameters, such as wall temperature and jet radius, explore the applicability of the model. Results are presented, including the generation of a high-altitude partial operational map for the Plasmatron X wind tunnel at the University of Illinois at Urbana-Champaign. Limitations are discussed, and verification against an existing model is provided. }
}
```
