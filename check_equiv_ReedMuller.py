import qutip as qt


def add_cnots(control,targets,state,N):
    """adds a multi cnot gate by decomposition into single cnots"""
    for t in targets:
        state = qt.cnot(N=N,control=control[0],target=t)*state
    return

def genstate(s):
    """helper function to obtain the correct initialization"""
    newstr = s.replace("+","0")
    newstr = newstr.replace("-","1")
    print(newstr)
    state = qt.ket(newstr)
    if s[0] == "+" or s[0]=="-":
        operator=qt.hadamard_transform()
    else:
        operator=qt.identity(2)
    for i in range(1,len(s),1):
        if s[i] == "+" or s[i]=="-":
            #apply hadamard
            operator = qt.tensor([operator,qt.hadamard_transform()])
        else:
            operator = qt.tensor([operator,qt.identity(2)])
    return operator * state

def main():
    #create output state for original circuit:
    N=16
    state = genstate("++0+000+0000000+")
    add_cnots([7],[8,9,10,11,12,13,14],state,N)
    add_cnots([3],[4,5,6,11,12,13,14],state,N)
    add_cnots([1],[2,5,6,9,10,13,14],state,N)
    add_cnots([0],[2,4,6,8,10,12,14],state,N)
    add_cnots([14],[2,4,5,8,9,11],state,N)



    #create output state for the translated circuit
    state2 = genstate("++0+000+0000000+")
    add_cnots([15],[2,4,5,8,9,11,14],state2,N)
    add_cnots([7],[2,4,5,10,12,13,14],state2,N)
    add_cnots([3],[2,6,8,9,12,13,14],state2,N)
    add_cnots([1],[4,6,8,10,11,13,14],state2,N)
    add_cnots([0],[5,6,9,10,11,12,14],state2,N)

    print(state == state2)
    return

if __name__ == '__main__':
    main()
