import numpy as np
from pyomo.environ import *
import gurobipy

NUM_ITEMS = 1

i = [ii for ii in range(NUM_ITEMS)]
j = [jj for jj in range(NUM_ITEMS)]
s = ['x', 'y', 'z']
np.random.seed(50546)

def generateItems():    
    items = {i: {'x':np.random.randint(20, 60), 'y':np.random.randint(20, 60), 'z':np.random.randint(20, 60)} for i in range(NUM_ITEMS)}
    return items

lis = generateItems()
Ls = {'x':59, 'y':59, 'z':25000}


model = ConcreteModel()

model.p_ijs = Var(i,j,s, within=Binary)

model.c_is = Var(i,s, within=NonNegativeReals)

model.h = Var(within=NonNegativeReals)

model.objective = Objective(expr=sum(model.c_is[ii,'z'] for ii in i), sense=minimize)

model.oneSpatialCorrelation = ConstraintList()
for ii in range(len(i)):
    for jj in range(len(j)):
        if (jj > ii):
            model.oneSpatialCorrelation.add(sum((model.p_ijs[ii, jj, ss]+model.p_ijs[jj, ii, ss]) for ss in s)>=1)

model.cannotPrecedeFollow = ConstraintList()
for ii in range(len(i)):
    for jj in range(len(j)):
        if (jj > ii):
            for ss in s:
                model.cannotPrecedeFollow.add(model.p_ijs[ii,jj,ss]+model.p_ijs[jj,ii,ss] <= 1)

model.nonOverlapping = ConstraintList()
for ii in i:
    for jj in j:
        if (ii != jj):
            for ss in s:
                model.nonOverlapping.add(model.c_is[ii,ss] + lis[ii][ss] <= model.c_is[jj,ss]+ Ls[ss]*(1- model.p_ijs[ii,jj,ss]))

model.withinBoundaries = ConstraintList()
for ii in i:
    for ss in s:
        model.withinBoundaries.add(0<=model.c_is[ii,ss]<=Ls[ss]-lis[ii][ss])

model.maxHeight = ConstraintList()
for ii in i:
    model.maxHeight.add(model.c_is[ii,'z'] + lis[ii]['z']<=model.h)

### SOLVE
# solver_manager = SolverFactory('gurobi_persistent')
# solver_manager.set_instance(model)
# solver_manager.solve()

opt = SolverFactory("cplex")

solver_manager = SolverManagerFactory('neos')
results = solver_manager.solve(model, opt=opt)
results.write()

print(model.display(filename="result.txt"))
print({(ii,jj,ss): model.p_ijs[ii,jj,ss].value for ii in i for jj in j for ss in s})