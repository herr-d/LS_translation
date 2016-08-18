
## Translation from inverted ICM to Lattice Surgery

This short script will use quantum circuits given in the inverted ICM format and prepare them to a graphical representation in the lattice surgery model. This model, however, is not yet optimized for efficient space time volumes.

The code is a part of a paper *Lattice Surgery Translation for Quantum Computation* by D. Herr, F. Nori and S. J. Devitt and can be found on the arxiv: <http://www.arxiv.org>


#### Input
First a circuit needs to be created using the member functions of the Circuit class.
These are:
- start_state
- add_cnots

After the initial circuit has been build it can be optimized. Several functions are available here:
- translate_circuit
- output_simple

#### Output

After optimization the output is given as severl lists of numbers. These numbers indicate which patch of surface code corresponds to which logical qubit. And the list indicate which patches belong to one single state before being split.


### Requirements
The code was written in Python 3 but should be compatible with Python 2. It requires the following external package(s):

- qutip (Homepage: <http://qutip.org/>) and its dependencies.

### Files

__IICMCircuit.py:__ Main class that contains all the methods and structures needed for simplifying the circuit and translating it to a graphical representation.

__Reedmuller.py:__ Example circuit given by the Reedmuller 14 qubit distillation procedure. This circuit is also used as an example in the paper.
__circuit_test.py:__ Very simple example to check individual elements.

__check_equiv_ReedMuller.py:__ Using the capabilities of QUTIP the circuit is simulated and the output is compared using the original representation and the translated representation.
