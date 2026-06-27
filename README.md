# The `std2` Package: A Computationally Efficient Program to Compute Molecular Response Properties and Excited States using Simplified Quantum Chemistry Methods

P. Beaujean, A. Liger, A. Satisha, M. G. Maraldi, C. Bannwarth, and M. de Wergifosse.

The [`std2` modular program package](https://github.com/Theoretical-Chemistry-Group-UCLouvain/std2) is dedicated to the computation of excited states and molecular response properties using simplified quantum chemistry (sQC) approaches.
The framework involves several variants of the simplified time-dependent density functional theory, including sTDA, sTD-DFT, SF-sTD-DFT, XsTDA, XsTD-DFT, and SF-XsTD-DFT methods.
Combining controlled approximations with efficient implementations, the `std2` program enables routine calculations on systems containing thousands of atoms while retaining a favorable balance between computational cost and predictive accuracy.
Therefore, the framework supports all-atom quantum mechanics (AQM) methodologies for the treatment of surrounding and dynamical structural effects considering realistic systems. In this contribution, the capabilities of the `std2` package are illustrated for spectroscopic observables such as one- and two-photon absorption, electronic circular dichroism, optical rotation, second-harmonic generation, and excited-state absorption.
Among results, benchmark calculations show that the recent XsTD-DFT scheme improves the description of excited states relative to sTD-DFT especially, for charge-transfer excitations while preserving a speedup of two to three orders of magnitude compared to standard TD-DFT.
Applications of AQM methodologies to explicitly solvated systems and ultra-large systems are also highlighted, showing the adequacy of the `std2` program to treat such systems. 
Overall, `std2` provides an efficient platform for large-scale excited-state and spectroscopic simulations, especially in AQM protocols.

Latest PDF: [Main text](https://github.com/Theoretical-Chemistry-Group-UCLouvain/publi-sQC-std2-2026/releases/download/latest/Main_Text.pdf), [Supporting information](https://github.com/Theoretical-Chemistry-Group-UCLouvain/publi-sQC-std2-2026/releases/download/latest/SI.pdf).
