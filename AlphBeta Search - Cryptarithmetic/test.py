from CSP import BinaryConstraint

variables = []
domains = {}
constraints = []

LHS0="GO"
LHS1="TO"
RHS="OUT"
# reverse all the strings 
LHS0 = LHS0[::-1]
LHS1 = LHS1[::-1]
RHS = RHS[::-1]
# set the variables of the problem
for i in LHS0:
 variables.append(i)
for i in LHS1:
 variables.append(i)
for i in RHS:
 variables.append(i)

variables = list(set( variables))
print("variables",variables)

# make binary constrain between each two variables not equal
# and check if this constrain is not exist before insert it 
unary=0
dic={}
for i in variables:
    for j in variables:
        if i != j: 
            b: BinaryConstraint = BinaryConstraint((i, j), lambda x, y: x != y)
            if dic.get((i,j)) != 1 or dic.get((j,i)) != 1:
                dic[(i,j)]=1
                dic[(j,i)]=1
                unary+=1
                print("not equal : ",(i, j))
                constraints.append(b)

m=len(RHS)
for i in range(m):
 variables.append("c"+str(i)) # carry variables            

# set the domain for each variable
for i in  variables:
    if(i == 'c0'):
        domains[i] = {0}
    # domain for carry variables
    elif(i[0] == 'c'):
        domains[i] = {0,1}
    # domain for last letter of each word
    elif(i == RHS[-1] or i == LHS0[-1] or i == LHS1[-1]):
        domains[i] = {1,2,3,4,5,6,7,8,9}
    # domain for other letters
    else:
        domains[i] = {0,1,2,3,4,5,6,7,8,9}

con: BinaryConstraint = BinaryConstraint((RHS[-1], 'c'+str(m-1) ), lambda x, y: x == y)
print(RHS[-1], 'c'+str(m-1))
constraints.append(con)
count=0
for i in range(m-1):
    count+=1
    if(i >= len(LHS0) and i >= len(LHS1)):
        b: BinaryConstraint = BinaryConstraint((RHS[i], 'c'+str(i) ), lambda x, y: x == y)
    elif(i >= len(LHS0)):
        x="c"+str(i)+LHS1[i]
        y="c"+str(i+1)+RHS[i]
        variables.append(x)
        variables.append(y)
        b: BinaryConstraint = BinaryConstraint((x, y), lambda x, y: x[2]+x[:2] == y[2]+10*y[:2])
        constraints.append(b)
        b1: BinaryConstraint = BinaryConstraint((x[0:2], 'c'+str(i+1) ), lambda x, y: x == y)
        constraints.append(b1)
        b2: BinaryConstraint = BinaryConstraint((x[2], LHS1[i]), lambda x, y: x == y)
        constraints.append(b2)
        b4: BinaryConstraint = BinaryConstraint((y[2], RHS[i]), lambda x, y: x == y)
        constraints.append(b4)
        b5: BinaryConstraint = BinaryConstraint((y[0:2], 'c'+str(i+1)), lambda x, y: x == y)
        constraints.append(b5)
    elif(i >= len(LHS1)):
        x="c"+str(i)+LHS0[i]
        y="c"+str(i+1)+RHS[i]
        variables.append(x)
        variables.append(y)
        b: BinaryConstraint = BinaryConstraint((x, y), lambda x, y: x[2]+x[:2] == y[2]+10*y[:2])
        constraints.append(b)
        b1: BinaryConstraint = BinaryConstraint((x[0:2], 'c'+str(i+1) ), lambda x, y: x == y)
        constraints.append(b1)
        b2: BinaryConstraint = BinaryConstraint((x[2], LHS0[i]), lambda x, y: x == y)
        constraints.append(b2)
        b4: BinaryConstraint = BinaryConstraint((y[2], RHS[i]), lambda x, y: x == y)
        constraints.append(b4)
        b5: BinaryConstraint = BinaryConstraint((y[0:2], 'c'+str(i+1)), lambda x, y: x == y)
        constraints.append(b5)
    else :
        x="c"+str(i)+LHS0[i]+LHS1[i]
        y="c"+str(i+1)+RHS[i]
        variables.append(x)
        variables.append(y)
 
        domains[x] = {int(str(a)+str(b)+str(c)) for a in domains["c"+str(i)] for b in domains[LHS0[i]] for c in domains[LHS1[i]]}
        domains[y] = {int(str(a)+str(b)) for a in domains["c"+str(i+1)] for b in domains[RHS[i]]}
                   
        print("equation is")
        print(x,y)
        b: BinaryConstraint = BinaryConstraint((x, y), lambda x, y: x[3]+x[2]+x[:2] == y[2]+10*y[:2])
        constraints.append(b)
        b1: BinaryConstraint = BinaryConstraint((x[0:2], 'c'+str(i) ), lambda x, y: x == y)
        print(x[0:2], 'c'+str(i+1))

        constraints.append(b1)
        b2: BinaryConstraint = BinaryConstraint((x[2], LHS0[i]), lambda x, y: x == y)
        print(x[2], LHS0[i])
        constraints.append(b2)
        b3: BinaryConstraint = BinaryConstraint((x[3], LHS1[i]), lambda x, y: x == y)
        print(x[3], LHS1[i])
        constraints.append(b3)
        b4: BinaryConstraint = BinaryConstraint((y[2], RHS[i]), lambda x, y: x == y)
        print(y[2], RHS[i])
        constraints.append(b4)
        b5: BinaryConstraint = BinaryConstraint((y[0:2], 'c'+str(i+1)), lambda x, y: x == y)
        print(y[0:2], 'c'+str(i+1))
        constraints.append(b5)

variables = list(set( variables))
print("variables",variables)
print("domains",domains)
print(len(constraints))
print(RHS[0], LHS0[0], LHS1[0])
x="123"
print( x[0])


