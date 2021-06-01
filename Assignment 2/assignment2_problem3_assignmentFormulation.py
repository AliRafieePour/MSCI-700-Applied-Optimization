from pyomo.environ import *

model = ConcreteModel()

weights = [20,16,24,27,28,13,13,30,22,24,37,41,16,21,18]

model.ykl = Var([i for i in range(6)], [j for j in range(15)], within=Binary)
model.zk = Var([i for i in range(6)], within=Binary)

model.maximumBins = Constraint(expr = sum(model.zk[i] for i in range(6)) <= 6)

def bins(model, i):
    return sum(model.ykl[i, j] * weights[j] for j in range(15)) - 70*model.zk[i] <= 0
model.bins = Constraint([i for i in range(6)], rule=bins)

def maximumItems(model, i):
    return sum(model.ykl[i, j] for j in range(15)) <= 3
model.maximumItems = Constraint([i for i in range(6)], rule=maximumItems)

def eachIteminOneBin(model, item):
    return sum(model.ykl[i, item] for i in range(6)) == 1
model.eachItem = Constraint([i for i in range(15)], rule=eachIteminOneBin)

model.Objective = Objective(expr = sum(model.zk[i] for i in range(6)), sense=minimize)
#model.Objective = Objective(expr= sum(model.ykl[i, j] * weights[j] for j in range(15) for i in range(6)), sense=maximize)
### SOLVE
solver_manager = SolverFactory('glpk')

results = solver_manager.solve(model)
print(results)
print(model.display(filename="result.txt"))
