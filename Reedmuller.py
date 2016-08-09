import numpy as np
import qutip as qt
from IICMCircuit import IICMCircuit


def main():
    N=16

    c = IICMCircuit(N)
    c.start_state("++0+000+0000000+")
    #implementation of the reed muller code
    c.add_cnots([15],[14])
    c.add_cnots([7],[8,9,10,11,12,13,14])
    c.add_cnots([3],[4,5,6,11,12,13,14])
    c.add_cnots([1],[2,5,6,9,10,13,14])
    c.add_cnots([0],[2,4,6,8,10,12,14])
    c.add_cnots([14],[2,4,5,8,9,11])


    #now translate this circuit to the LS model
    c.translate_circuit()

    #obtain the splits (inner lists) and merges (same elements in different sublists)
    #numbers correspond to the qubits with 0 being the first.
    print(c.output_simple())

    c.png()
    return

if __name__ == '__main__':
    main()
