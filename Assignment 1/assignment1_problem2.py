import numpy as np
from numpy.core.numeric import Inf
import timeit
from scipy.optimize import linprog

# for keeping track of the computatoin time of each step, I record times in a series of arrays
enteringArray = []
exitingArray = []
basisArray = []

# this is a random seed, so as we would produce similar random numbers for the sake of traceablity
#np.random.seed(1)

def random_problem(m, n):
    A = np.concatenate((np.random.randint(2, size=(m, n)), np.identity(m)), axis=1)
    b = np.ones(shape=(m, 1))
    c = np.concatenate((np.ones(shape=(1, n)), np.random.randint(5000000, 5000001, size=(1, m))), axis=1)
    basis = [i for i in range(n, m+n)]
    nonBasis = [i for i in range(0, n)]
    B = A[:, basis]
    N = A[:, nonBasis]
    return A, b, c, basis, nonBasis, B, N

# random problem 
rows = 4
columns = 14

# produce a random problem
A, b, c, basis, nonBasis, B, N = random_problem(rows, columns)

# problem defined in our assignment
# A = np.array([[1,0,1,0,0, 1, 0, 0],[0,1,1,1,0,0,1,0],[1,1,0,0,1,0,0,1]])
# b = np.array([[1],[1],[1]])
# c = np.array([[1, 1, 1, 1, 1, 50000000,50000000,50000000]])
# basis = [5,6,7]
# nonBasis = [0,1,2,3,4]
# B = np.array([[1,0,0],[0,1,0],[0,0,1]])
# N = np.array([[1,0,1,0,0], [0,1,1,1,0], [1,1,0,0,1]])

# solve using linprog
startTime = timeit.default_timer()
print(linprog(c, A_eq=A, b_eq=b, method='revised simplex'))
endTime = timeit.default_timer()
print(f"took: {endTime - startTime}")

def entering(c, B, basis, nonBasis, N):
    startEntering = timeit.default_timer()
    status = 0
    cN = c[:, nonBasis]
    cB = c[:, basis]
    reducedCosts = cN - np.matmul(np.matmul(cB, np.linalg.inv(B)), N)
    en = np.argmin(reducedCosts)
    if (reducedCosts[0][en] >= 0):
        status = 1
        endEntering = timeit.default_timer()
        t = endEntering - startEntering
        enteringArray.append(t)
        return status, en, cB, cN, t
    else:
        endEntering = timeit.default_timer()
        t = endEntering - startEntering
        enteringArray.append(t)
        return status, en, cB, cN, t

def exiting(b, B, N, enteringIndex, ):
    startExiting = timeit.default_timer()
    status = 0
    ratioTest = []
    Bb = np.matmul(np.linalg.inv(B), b)
    Ai = np.matmul(np.linalg.inv(B), N[:, enteringIndex])
    for i in range(len(Bb)):
        if (Ai[i]<0):
            ratioTest.append(Inf)
        elif (Ai[i] == 0):
            ratioTest.append(1000000)
        else:
            sth = Bb[i]/Ai[i]
            ratioTest.append(sth[0])
    ratioTest = np.array(ratioTest)
    ex = np.argmin(ratioTest)
    if (ratioTest[ex]>=0):
        endExiting = timeit.default_timer()
        t = endExiting - startExiting
        exitingArray.append(t)
        return status, ex, t
    else:
        status = 3
        endExiting = timeit.default_timer()
        t = endExiting - startExiting
        exitingArray.append(t)
        return status, ex, t

def change_basis(A, en, ex, basis, nonBasis):
    startBasis = timeit.default_timer()
    enteringValue = nonBasis[en]
    nonBasis[en] = basis[ex]
    basis[ex] = enteringValue
    B = A[:, basis]
    N = A[:, nonBasis]
    endBasis = timeit.default_timer()
    t = endBasis - startBasis
    basisArray.append(t)
    return B, N, basis, nonBasis, t

def checkInfeasblity(x, basis, rows, columns):
    for i in range(rows,rows+columns):
        
        if (i in basis):
            inde = basis.index(i)
            if (x[inde][0] == 0):
                continue
            else:
                return "True"
        else:
            continue
    return "False"

### main body

status = 0
justEntered = 6666

startTime = timeit.default_timer()
while (status != 1):
    status, enteringIndex, cB, cN, t = entering(c, B, basis, nonBasis, N)
    if (status == 1):
        print("Optimal")
        print(f"Function: {np.matmul(np.matmul(cB, np.linalg.inv(B)), b)}")
        x = np.matmul(np.linalg.inv(B), b)
        print(f"x: {x}")
    else:
        status, exitingIndex, t = exiting(b, B, N, enteringIndex)
        B, N, basis, nonBasis, t = change_basis(A, enteringIndex, exitingIndex, basis, nonBasis)

endTime = timeit.default_timer()
print(f"Took: {endTime - startTime}")
print(f"This problem's infeasbility: {checkInfeasblity(x, basis, rows, columns)}")
if (status == 3):
    print(f"This problem's unboundedness: True")
print(f"Average entering: {np.average(enteringArray)}")
print(f"Average exiting: {np.average(exitingArray)}")
print(f"Average changing basis: {np.average(basisArray)}")