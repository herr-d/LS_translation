import numpy as np
import qutip as qt
from IICMCircuit import IICMCircuit


def main():
    N=25

    c = IICMCircuit(N)
    c.start_state("++0+00000000+000+000+000+")
    #implementation of the bravyi-haah code
    c.add_cnots([1],[5])
    c.add_cnots([3],[7])
    c.add_cnots([0],[9,13,17,21])
    c.add_cnots([12],[9])
    c.add_cnots([16],[13])
    c.add_cnots([20],[17])
    c.add_cnots([24],[21])
    c.add_cnots([9],[11])
    c.add_cnots([13],[15])
    c.add_cnots([17],[19])
    c.add_cnots([21],[23])
    c.add_cnots([9],[7])
    c.add_cnots([13],[9])
    c.add_cnots([7],[13])
    c.add_cnots([17],[13])
    c.add_cnots([21],[17])
    c.add_cnots([13],[21])
    c.add_cnots([5],[9])
    c.add_cnots([9],[17])
    c.add_cnots([7],[5])
    c.add_cnots([9],[7])
    c.add_cnots([13],[9])
    c.add_cnots([17],[13])
    c.add_cnots([1],[2])
    c.add_cnots([3],[4])
    c.add_cnots([5],[6])
    c.add_cnots([7],[8])
    c.add_cnots([9],[10])
    c.add_cnots([13],[14])
    c.add_cnots([17],[18])
    c.add_cnots([21],[22])
    c.add_cnots([0],[1,3,5,7,9,13,17,21])
    #c.png()
    #return
    #now translate this circuit to the LS model
    c.translate_circuit()
    #obtain the splits (inner lists) and merges (same elements in different sublists)
    #numbers correspond to the qubits with 0 being the first.
    print(c.output_simple())
    print(len(c.output_simple()))
    c.png()
    return

if __name__ == '__main__':
    main()
