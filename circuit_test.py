import qutip as qt
from IICMCircuit import IICMCircuit


def main():
    N=4
    c = IICMCircuit(N)
    c.start_state("00++")
    c.add_cnots([1],[2])
    c.add_cnots([0],[1])
    c.add_cnots([0],[2])
    c.move_to(0,1)
    c.png()
    return

if __name__ == '__main__':
    main()
