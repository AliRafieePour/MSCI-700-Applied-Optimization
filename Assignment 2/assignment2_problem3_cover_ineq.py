from pyomo.environ import *
import pyomo.environ
import gurobipy
weights = [20,16,24,27,28,13,13,30,22,24,37,41,16,21,18]


model = ConcreteModel()


model.ykl = Var([i for i in range(6)], [j for j in range(15)], within=Binary)
model.zk = Var([i for i in range(6)], within=Binary)

model.maximumBins = Constraint(expr = sum(model.zk[i] for i in range(6)) <= 6)

model.cuts = ConstraintList()

def maximumItems(model, i):
    return sum(model.ykl[i, j] for j in range(15)) <= 3
model.maximumItems = Constraint([i for i in range(6)], rule=maximumItems)

def eachIteminOneBin(model, item):
    return sum(model.ykl[i, item] for i in range(6)) == 1
model.eachItem = Constraint([i for i in range(15)], rule=eachIteminOneBin)

def act(model, i, j):
    return model.ykl[i,j]<=model.zk[i]
model.act = Constraint([i for i in range(6)], [j for j in range(15)], rule=act)
model.Objective = Objective(expr = sum(model.zk[i] for i in range(6)), sense=minimize)

def check():
    ineq = []
    assignments = {(i,j): model.ykl[i,j].value for i in range(6) for j in range(15)}
    addedCuts = 0
    for i in range(6):
        summ = 0
        count = 0
        for j in range(15):
            summ += weights[j] * model.ykl[i, j].value
            if (model.ykl[i,j].value):
                count += 1
        if (summ>70):
            print(f"adding cut over bin {i}")
            alist = {j: model.ykl[i,j].value*weights[j] for j in range(15) if model.ykl[i,j]}
            model.cuts.add(sum(model.ykl[i, j] for j in range(15) if model.ykl[i, j]) <= count - 1)
            addedCuts += 1
    if (addedCuts == 0):
        alist = {i: sum(model.ykl[i,j].value*weights[j] for j in range(15)) for i in range(6)}
        print("***Optimal***")
        print(f"current bins: {alist}")
        return "Optimal"
    else:
        alist = {i: sum(model.ykl[i,j].value*weights[j] for j in range(15)) for i in range(6)}
        print(f"current bins: {alist}")
        return "ongoing"

import time
status = "ongoing"
while(status == "ongoing"):
    solver_manager = SolverFactory('gurobi_persistent')
    solver_manager.set_instance(model)
    solver_manager.solve()
    status = check()

print(model.display(filename="result.txt"))
