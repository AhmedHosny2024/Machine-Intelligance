from typing import Tuple
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint

#TODO (Optional): Import any builtin library or define any helper function you want to use

# This is a class to define for cryptarithmetic puzzles as CSPs
class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None: continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) +  ")" 
        return formula

    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match: raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i+1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS

        #TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).


        problem.variables = []
        problem.domains = {}
        problem.constraints = []

        # reverse all the strings so adding letter will be easier
        LHS0 = LHS0[::-1]
        LHS1 = LHS1[::-1]
        RHS = RHS[::-1]
        # set the variables of the problem
        for i in LHS0:
            problem.variables.append(i)
        for i in LHS1:
            problem.variables.append(i)
        for i in RHS:
            problem.variables.append(i)

        # remove duplicates
        problem.variables = list(set(problem.variables))
        # make each two variables different constrain
        for i in problem.variables:
            for j in problem.variables:
                if i != j:
                    b: BinaryConstraint = BinaryConstraint((i, j), lambda x, y: x != y)
                    problem.constraints.append(b)
        # make carry variables
        m=len(RHS)
        for i in range(m):
            problem.variables.append("c"+str(i)) # carry variables            

        # set the domain for each variable
        for i in problem.variables:
            # domain for carry variables
            if(i == 'c0'):
                problem.domains[i] = {0}
            elif(i[0] == 'c'):
                problem.domains[i] = {0,1}
            # domain for last letter of each word
            elif(i == RHS[-1] or i == LHS0[-1] or i == LHS1[-1]):
                problem.domains[i] = {1,2,3,4,5,6,7,8,9}
            # domain for other letters
            else:
                problem.domains[i] = {0,1,2,3,4,5,6,7,8,9}

        # check for if last carry variable is equal to the last letter of RHS
        if(m != len(LHS0) and m != len(LHS1)):
            con: BinaryConstraint = BinaryConstraint((RHS[-1], 'c'+str(m-1) ), lambda x, y: x == y)
            problem.constraints.append(con)

        # make constrain between carry variables and letters except the last letter
        for i in range(m-1):
            # case last letter and no letters in LHS0 and LHS1
            if(i >= len(LHS0) and i >= len(LHS1)):
                b: BinaryConstraint = BinaryConstraint((RHS[i], 'c'+str(i) ), lambda x, y: x == y)
                continue
            # case LHS0 is empty and LHS1 is not empty
            elif(i >= len(LHS0)):
                # create new two variables for each letter and carry variable
                data1=LHS1[i]+"c"+str(i)
                data2=RHS[i]+"c"+str(i+1)
                problem.variables.append(data1)
                problem.variables.append(data2)
                # set the domain for x as all compinations of domain of problem.varaible[c+str(i)] and problem.variables[LHS1[i]]
                problem.domains[data1] = {(b,a,b) for a in problem.domains["c"+str(i)] for b in problem.domains[LHS1[i]]}
                problem.domains[data2] = {(b,a) for a in problem.domains["c"+str(i+1)] for b in problem.domains[RHS[i]]}
                # constrains between the two variables
                b: BinaryConstraint = BinaryConstraint((data1, data2), lambda x, y: ( x[0]+x[1] == y[0]+10*y[1] if len(x) == 3 else y[0]+y[1] == x[0]+10*x[1]) )
                problem.constraints.append(b)
                # constraine between the two variables and the original variables and carry variables
                b1: BinaryConstraint = BinaryConstraint((data1, 'c'+str(i) ), lambda x, y: x==y[1] if isinstance(x, int) else x[1] == y)
                problem.constraints.append(b1)
                b2: BinaryConstraint = BinaryConstraint((data1, LHS1[i]), lambda x, y: x==y[0] if isinstance(x, int) else x[0] == y)
                problem.constraints.append(b2)
                b4: BinaryConstraint = BinaryConstraint((data2, RHS[i]),lambda x, y: x==y[0] if isinstance(x, int) else x[0] == y)
                problem.constraints.append(b4)
                b5: BinaryConstraint = BinaryConstraint((data2, 'c'+str(i+1)), lambda x, y: x==y[1] if isinstance(x, int) else x[1] == y)
                problem.constraints.append(b5)
            # case LHS1 is empty and LHS0 is not empty
            elif(i >= len(LHS1)):
                # create new two variables for each letter and carry variable
                data1=LHS0[i]+"c"+str(i)
                data2=RHS[i]+"c"+str(i+1)
                problem.variables.append(data1)
                problem.variables.append(data2)
                # set the domain for x as all compinations of domain of problem.varaible[c+str(i)] and problem.variables[LHS0[i]]
                problem.domains[data1] = {(b,a,b) for a in problem.domains["c"+str(i)] for b in problem.domains[LHS0[i]]}
                problem.domains[data2] = {(b,a) for a in problem.domains["c"+str(i+1)] for b in problem.domains[RHS[i]]}  
                # constrains between the two variables
                b: BinaryConstraint = BinaryConstraint((data1, data2), lambda x, y: (x[0] + x[1] == y[0]+10*y[1] if len(x) == 3 else y[0] + y[1] == x[0]+10*x[1]) )
                problem.constraints.append(b)
                # constraine between the two variables and the original variables and carry variables
                b1: BinaryConstraint = BinaryConstraint((data1, 'c'+str(i) ),lambda x, y: x==y[1] if isinstance(x, int) else x[1] == y)
                problem.constraints.append(b1)
                b2: BinaryConstraint = BinaryConstraint((data1, LHS0[i]),  lambda x, y: x==y[0] if isinstance(x, int) else x[0] == y)
                problem.constraints.append(b2)
                b4: BinaryConstraint = BinaryConstraint((data2, RHS[i]),lambda x, y: x==y[0] if isinstance(x, int) else x[0] == y)
                problem.constraints.append(b4)
                b5: BinaryConstraint = BinaryConstraint((data2, 'c'+str(i+1)),lambda x, y: x==y[1] if isinstance(x, int) else x[1] == y)
                problem.constraints.append(b5)
            # case LHS0 and LHS1 are not empty
            else :
                # create new two variables for each letter and carry variable
                data1=LHS0[i]+LHS1[i]+"c"+str(i)
                data2=RHS[i]+"c"+str(i+1)
                problem.variables.append(data1)
                problem.variables.append(data2)
                # set the domain for x as all compinations of domain of problem.varaible[c+str(i)] and problem.variables[LHS0[i]] and problem.variables[LHS1[i]]
                problem.domains[data1] = { (b,c,a) for a in problem.domains["c"+str(i)] for b in problem.domains[LHS0[i]] for c in problem.domains[LHS1[i]]}
                problem.domains[data2] = { (b,a) for a in problem.domains["c"+str(i+1)] for b in problem.domains[RHS[i]]}
                # constrains between the two variables
                b: BinaryConstraint = BinaryConstraint((data1, data2),lambda x, y: (x[2]+x[1]+x[0] == y[0]+ 10 * y[1] if len(x) == 3 else y[2]+y[1]+y[0] == x[0]+ 10 * x[1]) )
                problem.constraints.append(b)
                b1: BinaryConstraint = BinaryConstraint((data1, 'c'+str(i)), lambda x, y: x==y[2] if isinstance(x, int) else x[2] == y)
                problem.constraints.append(b1)
                b2: BinaryConstraint = BinaryConstraint((data1, LHS0[i]), lambda x, y: x==y[0] if isinstance(x, int) else x[0] == y)
                problem.constraints.append(b2)
                b3: BinaryConstraint = BinaryConstraint((data1, LHS1[i]), lambda x, y: x==y[1] if isinstance(x, int) else x[1] == y)
                problem.constraints.append(b3)
                b4: BinaryConstraint = BinaryConstraint((data2, RHS[i]), lambda x, y: x==y[0] if isinstance(x, int) else x[0] == y)
                problem.constraints.append(b4)
                b5: BinaryConstraint = BinaryConstraint((data2, 'c'+str(i+1)), lambda x, y: x==y[1] if isinstance(x, int) else x[1] == y)
                problem.constraints.append(b5)
        # make constrain for last carry variable and last letter of RHS if LHS0 and LHS1 are not empty
        if(m==len(LHS0) and m==len(LHS1)):
            i=m-1
            data1=LHS0[i]+LHS1[i]+"c"+str(i)
            data2=RHS[i]
            problem.variables.append(data1)
            problem.domains[data1] = { (b,c,a) for a in problem.domains["c"+str(i)] for b in problem.domains[LHS0[i]] for c in problem.domains[LHS1[i]]}
            b: BinaryConstraint = BinaryConstraint((data1, data2),lambda x, y: (y[2]+y[1]+y[0] == x if isinstance(x, int) else x[2]+x[1]+x[0] == y ) )
            problem.constraints.append(b)
            b1: BinaryConstraint = BinaryConstraint((data1, 'c'+str(i)), lambda x, y: x==y[2] if isinstance(x, int) else x[2] == y)
            problem.constraints.append(b1)
            b2: BinaryConstraint = BinaryConstraint((data1, LHS0[i]), lambda x, y: x==y[0] if isinstance(x, int) else x[0] == y)
            problem.constraints.append(b2)
            b3: BinaryConstraint = BinaryConstraint((data1, LHS1[i]), lambda x, y: x==y[1] if isinstance(x, int) else x[1] == y)
            problem.constraints.append(b3)
            
        # make constrain for last carry variable and last letter of RHS if LHS0 is empty
        elif(m==len(LHS0)):
            i=m-1
            data1=LHS0[i]+"c"+str(i)
            data2=RHS[i]
            problem.variables.append(data1)
            problem.domains[data1] = {(b,a,b) for a in problem.domains["c"+str(i)] for b in problem.domains[LHS0[i]]}
            b: BinaryConstraint = BinaryConstraint((data1, data2), lambda x, y: ( y[0]+y[1] == x if isinstance(x, int) else x[0]+x[1] == y) )
            problem.constraints.append(b)
            b1: BinaryConstraint = BinaryConstraint((data1, 'c'+str(i) ), lambda x, y: x==y[1] if isinstance(x, int) else x[1] == y)
            problem.constraints.append(b1)
            b2: BinaryConstraint = BinaryConstraint((data1, LHS0[i]), lambda x, y: x==y[0] if isinstance(x, int) else x[0] == y)
            problem.constraints.append(b2)
        # make constrain for last carry variable and last letter of RHS if LHS1 is empty
        elif(m==len(LHS1)):
            i=m-1
            data1=LHS1[i]+"c"+str(i)
            data2=RHS[i]
            problem.variables.append(data1)
            problem.domains[data1] = {(b,a,b) for a in problem.domains["c"+str(i)] for b in problem.domains[LHS1[i]]}
            b: BinaryConstraint = BinaryConstraint((data1, data2), lambda x, y: ( y[0]+y[1] == x if isinstance(x, int) else x[0]+x[1] == y) )
            problem.constraints.append(b)
            b1: BinaryConstraint = BinaryConstraint((data1, 'c'+str(i) ), lambda x, y: x==y[1] if isinstance(x, int) else x[1] == y)
            problem.constraints.append(b1)
            b2: BinaryConstraint = BinaryConstraint((data1, LHS1[i]), lambda x, y: x==y[0] if isinstance(x, int) else x[0] == y)
            problem.constraints.append(b2)
        problem.variables = list(set(problem.variables))
                
        return problem
    
    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())