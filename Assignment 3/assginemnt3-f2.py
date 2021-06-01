#part f subgradiant method

from pyomo.environ import *
import logging
logging.getLogger('pyomo.core').setLevel(logging.ERROR)

def produceCuts(u):
    i = [ii for ii in range(6)]
    model = ConcreteModel()
    model.x = Var(i, within=Binary)
    model.objective = Objective(expr=2*model.x[0] + model.x[1] + 2*model.x[2] + 3*model.x[3] + model.x[4] + 2*model.x[5]
                                + u[0]*(- model.x[0] - model.x[3])
                                + u[1]*(- model.x[1] - model.x[4])
                                + u[2]*(- model.x[2] - model.x[5]), sense=maximize)

    model.c1 = Constraint(expr=20*model.x[0] + 10*model.x[1] + 15*model.x[2]<=25)
    model.c2 = Constraint(expr=15*model.x[3] + 8*model.x[4] + 12*model.x[5] <=21)
    
    ### SOLVE
    solver_manager = SolverFactory('gurobi_persistent')
    solver_manager.set_instance(model)
    solver_manager.solve()
    
    _, ob = lagrangianHeuristic([model.x[i].value for i in range(6)])
    print(f"Langragian heuristic: {lagrangianHeuristic([model.x[i].value for i in range(6)])}")
    return ([model.x[i].value for i in range(6)], model.objective.value(), ob)

def lagrangianHeuristic(x):
    for m in range(50):
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

x = 0
sol = 0
u = [5,0,0]

hist = []
gaps = []
UBs = []

for i in range(100000):
    x, sol, ob = produceCuts(u)
    print(f"UB: {sol+u[0]+u[1]+u[2]}")
    UBs.append(sol+u[0]+u[1]+u[2])
    print(f"heuristic solution gap: {sol+u[0]+u[1]+u[2] - ob}")
    gaps.append(sol+u[0]+u[1]+u[2] - ob)
    u[0] = max(0, u[0] - 0.001 * (1 - x[0] - x[3]))
    u[1] = max(0, u[1] - 0.001 * (1 - x[1] - x[4]))
    u[2] = max(0, u[2] - 0.001 * (1 - x[2] - x[5]))
    print(u)
    if (sol+u[0]+u[1]+u[2] - ob == 0):
        print(f"iteration number: {i}")
        break
    print("***")
    

print(x, sol)
