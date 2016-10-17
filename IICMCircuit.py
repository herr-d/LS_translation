import qutip as qt


class IICMCircuit:
    def __init__(self,N):
        """
        create empty circuit
        """
        self._N = N
        self._circ = qt.QubitCircuit(N,reverse_states=False)
        return

    def translate_circuit(self):
        """
        translate circuit to the format required for lattice surgery
        """
        while(bool(len(self.__targetpos__())) or bool(len(self.__gatepos__()))):
            #remove gates that target qbits initialized to +
            for i in range(len(self.__targetpos__())):
                gate=self.__targetpos__()[0]
                self.move_front(gate)
                self.deleteCNOTS_front()
            #remove cnots whose control qubit is given by a gate initialized to 0
            for i in range(len(self.__gatepos__())):
                gate = self.__gatepos__()[0]
                self.move_front(gate)
                self.deleteCNOTS_front()
        #merge same cnots
        self.simplify()
        return

    def add_cnots(self, control, targets):
        """
        using multiple target cnots
        """
        for i in targets:
            self._circ.add_gate("CNOT",targets=[i],controls=control)
        return

    def start_state(self,states):
        if (len(states)==self._N):
            if type(states)== list:
                self._start = ""
                for i in states:
                    self._start += i
            if type(states)== str:
                self._start=states
            return
        print("need to have the same number of qubits")
        return

    def detect_swap(self,i):
        """
        returns true only if gate i and i+1 perform a swap
        """
        if ((self._circ.gates[i].controls == self._circ.gates[i+1].targets)
        and (self._circ.gates[i].targets == self._circ.gates[i+1].controls)):
            return True
        return False

    def resolve_swap(self,state):
        if not self.detect_swap(state):
            return
        print("detected swap")
        #delete gate state and state+1
        swap1=self._circ.gates[state].targets[0]
        swap2=self._circ.gates[state].controls[0]
        self._circ.gates.pop(state)
        self._circ.gates.pop(state)
        print("SWAP: " +str(swap1) +" "+ str(swap2))
        #swap all gates in the following
        for j in range(len(self._circ.gates)):
            if self._circ.gates[j].controls[0] == swap1:
                self._circ.gates[j].controls[0]=swap2
            elif self._circ.gates[j].controls[0] == swap2:
                self._circ.gates[j].controls[0]=swap1

            if self._circ.gates[j].targets[0] == swap1:
                self._circ.gates[j].targets[0]=swap2
            elif self._circ.gates[j].targtes[0] == swap2:
                self._circ.gates[j].targets[0]=swap1
        return

    def deleteCNOTS_front(self):
        """
        Delete redundant CNOTS at the front of the circuit
        """
        targeted=[]
        #while(len(self._circ.gates) and (self._circ.gates[0].controls[0] in self.__indexch__()) and (not self._circ.gates[0].controls[0] in targeted)):
        while(len(self._circ.gates) and (self._circ.gates[0].controls[0] in self.__indexch__() or (not self._circ.gates[0].targets[0] in self.__indexch__())) and (not self._circ.gates[0].controls[0] in targeted)):
            #delete CNOT
            deleted = self._circ.gates.pop(0)
            for t in deleted.targets:
                targeted.append(t)
        return

    def move_front(self,i):
        """
        Permutes the specified CNOT to the front
        """
        return self.move_to(i,0)

    def move_to(self,target,destination):
        ""
        if (target> destination):
            #move forward
            print("target: " +str(target) + " destination: " + str(destination))
            for s in range(target-destination):
                if self.__localswap__(target-1-s):
                    break #encountered a swap and resolved it
        elif(destination>target):
            #move backward: harder as permutations introduce more cnots
            #just implement a move forward by all following gates
            while(target != destination):
                length = len(self._circ.gates)
                if self.__localswap__(target):
                    break #encountered a swap and resolved it
                if length<len(self._circ.gates):
                    # since not necessarily commuting an error gate was inserted at i+1
                    # shifting all the all the following qubits by 1
                    destination += 1
                    target += 1
                #target moved forward by 1
                target+=1
        return

    def png(self):
        self._circ.png


    def simplify_loop(self):
        for i in range(len(self._circ.gates)):
            for j in range(i):
                if self._circ.gates[i].controls == self._circ.gates[j].controls and self._circ.gates[i].targets == self._circ.gates[j].targets:
                    #move them together then delete
                    if not self.permutation(i,j):
                        self._circ.gates.pop(i)
                        self._circ.gates.pop(j)
                        return True
        return False

    def simplify(self):
        """
        two identical cnots without any change between them cancel
        """
        res = self.simplify_loop()
        while(res == True):
            res=self.simplify_loop()
        return    

    def permutation(self,i,j):
        """
        checks whether additional cnots need to be implemented while permuting gate i to location j
        """
        targets = self._circ.gates[i].targets
        control = self._circ.gates[i].controls[0]
        for k in range(min(i+1,j),max(i,j),1):
            if self._circ.gates[k].controls[0] in targets:
                return True
            if control in self._circ.gates[k].targets:
                return True
        return False

    def check(self):
        """
        Can this circuit be made into a lattice surgery state praperation procedure
        """
        # control qubit on + state?
        gstate= self.__indexch__()
        for i in range(len(self._circ.gates)):
            if self._circ.gates[i].controls[0] in gstate:
                return False
        return True

    def output_simple(self):
        """
        returns several lists of numbers that need to be initialized together and then split using smooth splits
        """
        #merge cnot with the same control:
        if not self.check():
            self.translate_circuit()

        assert(self.check())
        blocks = {}
        for i in range(len(self._circ.gates)):
            cont = self._circ.gates[i].controls[0]
            #add to list
            if cont in blocks:
                for t in self._circ.gates[i].targets:
                    if t in blocks[cont]:
                        blocks[cont].remove(t)
                    else:
                        blocks[cont].append(t)
            else:
                blocks[cont]=[cont]+self._circ.gates[i].targets.copy()
        re = []
        for key in blocks:
            re.append(sorted(blocks[key]))
        return re

    def __control_qubits__(self):
        """
        which qubits are used as control qubit for one of the cnots
        """
        qubits = []
        for i in range(len(self._circ.gates)):
            for j in self._circ.gates[i].controls:
                if j not in qubits:
                    qubits.append(j)
        return sorted(qubits)

    def __indexch__(self,character="0"):
        """
        which qubits are initialized to 0
        """
        return [i for i, ltr in enumerate(self._start) if ltr == character]

    def __gatepos__(self):
        """
        which gates use a controlqubit initially set to 0
        """
        gates=[]
        qubits = self.__indexch__()
        for i in range(len(self._circ.gates)):
            if self._circ.gates[i].controls[0] in qubits:
                gates.append(i)
        return gates

    def __targetpos__(self):
        """
        which gates target a qubit initially set to +
        """
        gates=[]
        qubits = self.__indexch__("+")
        for i in range(len(self._circ.gates)):
            if self._circ.gates[i].targets[0] in qubits:
                gates.append(i)
        return gates

    def __localswap__(self,i):
        """"swaps i and i+1"""
        #first ensure no swap
        if self.detect_swap(i):
            self.resolve_swap(i)
            return True

        gate1 =self._circ.gates[i]
        gate2 =self._circ.gates[i+1]
        #perform swap
        self._circ.gates[i] = gate2
        self._circ.gates[i+1]=gate1
        #add error gates due to non commuting swap
        if gate1.controls[0] in gate2.targets:
            #add cnot with control from gate2 and target from gate 1
            self._circ.gates.insert(i+1,qt.Gate("CNOT",targets=gate1.targets.copy(),controls=gate2.controls.copy()))
        elif gate2.controls[0] in gate1.targets:
            #add cnot with control from gate 1 and target from gate 2
            self._circ.gates.insert(i+2,qt.Gate("CNOT",targets=gate2.targets.copy(),controls=gate1.controls.copy()))
        return False
