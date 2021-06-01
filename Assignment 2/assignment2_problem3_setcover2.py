# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 19:46:29 2021

@author: urafi
"""

from pyomo.environ import *
import numpy as np
patterns = []
slacks = []
weights = [20,16,24,27,28,13,13,30,22,24,37,41,16,21,18]

for iterat in range(2500):
    
    model = ConcreteModel()
        
    model.ykl = Var([i for i in range(15)], within=Binary)
    model.bound = Constraint(expr = sum(model.ykl[i]*weights[i] for i in range(15))<=70)
    
    model.Objective = Objective(expr = sum(np.random.randint(0, 100000000) * model.ykl[i] for i in range(15)), sense= maximize)
    
    ### SOLVE
    solver_manager = SolverFactory('glpk')
    
    results = solver_manager.solve(model)
    
    
    for v in model.component_objects(Var, active=True):
        varobject = getattr(model, str(v))
        pattern = np.zeros(15)
        for index in varobject:
            pattern[index] = varobject[index].value
        patterns.append(pattern)

for p in range(len(patterns)):
    patterns[p] = list(patterns[p])


model = ConcreteModel()

dic = {(p, s): patterns[p][s] for p in range(len(patterns)) for s in range(15)}
model.dic = Param([p for p in range(len(patterns))], [s for s in range(15)], initialize = dic, within=Any, mutable=True)

# if pattern i is used
model.pi = Var([i for i in range(len(patterns))], within=Binary)

# only one usage in bins
def onlyOne(model, item):
    return sum(model.pi[j]*model.dic[j, item] for j in range(len(patterns))) == 1
model.onlyOnePattern = Constraint([i for i in range(15)], rule=onlyOne)

model.objective = Objective(expr=sum(model.pi[i] for i in range(len(patterns))), sense=minimize)

from gurobipy import *
### SOLVE
solver_manager = SolverFactory('glpk')

results = solver_manager.solve(model)

print(model.display(filename="result.txt"))
