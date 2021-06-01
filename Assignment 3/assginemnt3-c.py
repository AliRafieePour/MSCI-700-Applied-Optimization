#part c constraint generation method

from pyomo.environ import *
import numpy as np
import logging
logging.getLogger('pyomo.core').setLevel(logging.ERROR)

i = [ii for ii in range(6)]
def produceCuts(u):
    model = ConcreteModel()
    model.x = Var(i, within=Binary)
    model.objective = Objective(expr=2*model.x[0] + model.x[1] + 2*model.x[2] + 3*model.x[3] + model.x[4] + 2*model.x[5]
                                + u[0]*(- 20*model.x[0] - 10*model.x[1] - 15*model.x[2])
                                + u[1]*(- 15*model.x[3] - 8*model.x[4] - 12*model.x[5]), sense=maximize)
    
    model.c3 = Constraint(expr=model.x[0] + model.x[3] == 1)
    model.c4 = Constraint(expr=model.x[1] + model.x[4] == 1)
    model.c5 = Constraint(expr=model.x[2] + model.x[5] == 1)
    
    ### SOLVE
    solver_manager = SolverFactory('gurobi_persistent')
    solver_manager.set_instance(model)
    solver_manager.solve()
    
    _, ob = lagrangianHeuristic([model.x[i].value for i in range(6)])
    print(f"Langragian heuristic: {lagrangianHeuristic([model.x[i].value for i in range(6)])}")
    return ([model.x[i].value for i in range(6)], model.objective.value(), ob)


def lagrangianHeuristic(x):
    if (x[0]+x[3] == 0):
        x[0] = 1
    elif (x[0]+x[3] > 1):
        x[0] = 0

    if (x[1]+x[4] == 0):
        x[1] = 1
    elif (x[1]+x[4] > 1):
        x[1] = 0

    if (x[2]+x[5] == 0):
        x[2] = 1
    elif (x[2]+x[5] > 1):
        x[2] = 0
    
    r = 0
    while (25< 15*x[3] + 8*x[4] + 12*x[5]):
        if (r == 0 and x[3]!=0):
            x[3] = 0
            r += 1
        elif (r == 1 and x[4]!=0):
            x[4] -= 1
            r += 1
        elif(x[5]!=0):
            x[5] -= 1

    r = 0
    while (21 < 20*x[0] + 10*x[1] + 15*x[2]):
        if (r == 0 and x[0]!=0):
            x[0] -= 1
            r += 1
        elif (r == 1 and x[1]!=0):
            x[1] -= 1
            r += 1
        elif(x[2]!=0):
            x[2] -= 1
    
    if (x[0]+x[3] == 0):
        x[0] = 1
    elif (x[0]+x[3] > 1):
        x[0] = 0

    if (x[1]+x[4] == 0):
        x[1] = 1
    elif (x[1]+x[4] > 1):
        x[1] = 0

    if (x[2]+x[5] == 0):
        x[2] = 1
    elif (x[2]+x[5] > 1):
        x[2] = 0
    return x, 2*x[0] + x[1] + 2*x[2] + 3*x[3] + x[4] + 2*x[5]
            
        

def addCutsandSolve():
    objValues = []
    u = [10,15]
    print(f"u: {u}")
    model = ConcreteModel()
    model.u = Var([ii for ii in range(2)], within=NonNegativeReals)
    model.theta = Var(within=NonNegativeReals)
    model.cuts = ConstraintList()
    model.obj = Objective(expr=25*model.u[0]+21*model.u[1]+model.theta, sense=minimize)

    LB=0
    UB=100
    while (LB != UB+25*u[0]+21*u[1]):
        (x, UB, ob) = produceCuts(u)
        objValues.append(UB+25*u[0]+21*u[1])
        UB = min(objValues)
        print(f"heuristic solution gap: {UB - ob}")
        print(f"x: {x}")
        print(f"cut details: {2*x[0] + x[1] + 2*x[2] + 3*x[3] + x[4] + 2*x[5]} and {- 20*x[0] - 10*x[1] - 15*x[2]} and {- 15*x[3] - 8*x[4] - 12*x[5]}")
        model.cuts.add(expr=model.theta>=2*x[0] + x[1] + 2*x[2] + 3*x[3] + x[4] + 2*x[5] + model.u[0]*(- 20*x[0] - 10*x[1] - 15*x[2]) + model.u[1]*(- 15*x[3] - 8*x[4] - 12*x[5]))
            ### SOLVE
        solver_manager = SolverFactory('gurobi_persistent')
        solver_manager.set_instance(model)
        solver_manager.solve()
        LB = model.obj.value()
        print(f"LB: {LB}")
        u = [model.u[0].value, model.u[1].value]
        print(f"UB: {UB}")
        print("***")
        print(f"u: {u}")
    print(x)
    print(objValues)
    print(f"theta: {model.theta.value}")
addCutsandSolve()