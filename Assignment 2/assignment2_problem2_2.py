from pyomo.environ import *
import gurobipy
import numpy as np

model = ConcreteModel()

cij = [[10000000000, 82, 34, 64, 141, 201, 62], [82, 10000000000, 94, 124, 79, 142, 123], [34, 94, 10000000000, 57, 154, 214, 52], [64, 124, 57, 10000000000, 184, 244, 22], [141, 79, 154, 184, 10000000000, 81, 179], [201, 142, 214, 244, 81, 10000000000, 239], [62, 123, 52, 22, 179, 239, 10000000000]]

'''
cij = [[np.random.randint(10,100) for i in range(500)] for j in range(500)]
for i in range(200):
    for j in range(200):
        if (i == j):
            cij[i][ j] = 100000000000
'''

model.xij = Var([i for i in range(len(cij))], [j for j in range(len(cij))], within=Binary)

def exitingEdges(model, i):
    return sum(model.xij[i, j] for j in range(len(cij))) == 1
model.exitingEdges = Constraint([i for i in range(len(cij))], rule=exitingEdges)

def enteringEdges(model, i):
    return sum(model.xij[j, i] for j in range(len(cij))) == 1
model.enteringEdges = Constraint([i for i in range(len(cij))], rule=enteringEdges)

model.cuts = ConstraintList()
model.obj = Objective(expr=sum(sum(model.xij[i,j]*cij[i][j] for i in range(len(cij))) for j in range(len(cij))), sense=minimize)

def check():
    xij = {(i,j): model.xij[i,j].value for i in range(len(cij)) for j in range(len(cij))}
    edges = []
    for i in range(len(cij)):
        for j in range(len(cij)):
            if (model.xij[i,j].value):
                edges.append((i,j))
    tours = []
    tour = []
    visited = set()
    goneThrough = []
    edgeID = 0
    while(edgeID != len(edges)):
        tour = []
        if (edges[edgeID][1] not in visited):
            visited.add(edges[edgeID][0])
            visited.add(edges[edgeID][1])
            edgeID += 1
        else:
            if (edges[edgeID] in goneThrough):
                edgeID += 1
                continue
            tourVisited = []
            tour.append(edges[edgeID])
            tourVisited.append(edges[edgeID][0])
            tourVisited.append(edges[edgeID][1])
            visited.add(edges[edgeID][0])
            visited.add(edges[edgeID][1])
            indx = 0
            while(indx != len(edges)):
                try:
                    if ((edges[indx][0] in tourVisited or edges[indx][1] in tourVisited) and edges[indx] not in tour):
                        tour.append(edges[indx])
                        tourVisited.append(edges[indx][0])
                        tourVisited.append(edges[indx][1])
                        indx = 0
                    else:
                        indx += 1
                except:
                    break
            tours.append(tour)
            for t in tour:
                goneThrough.append(t)
        
            edgeID = 0
    return tours

def cut(tours):
    for tour in tours:
        model.cuts.add(sum(model.xij[edge[0], edge[1]] for edge in tour)<= len(tour) - 1)
        if (len(tour) == len(cij)):
            print("***Optimal***")
            print(f"Optimal tour= {tour}")
        else:
            print(f"eliminating subtour {tour}")

### SOLVE
while(1):
    solver_manager = SolverFactory('gurobi_persistent')
    solver_manager.set_instance(model)
    
    solver_manager.solve()
    
    tours = check()
    cut(tours)
    if (len(tours)==1):
        break

print(model.display(filename="result.txt"))

