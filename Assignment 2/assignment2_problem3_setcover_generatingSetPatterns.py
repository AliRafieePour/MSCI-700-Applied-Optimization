# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 18:19:48 2021

@author: urafi
"""

from pyomo.environ import *
import numpy as np
patterns = []
slacks = []
weights = [20,16,24,27,28,13,13,30,22,24,37,41,16,21,18]

for iterat in range(2000):
    
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
        slacks.append(model.bound.slack())
print(patterns)