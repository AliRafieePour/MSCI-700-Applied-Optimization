from pyomo.environ import *
import random
import numpy as np

import logging
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

from yellowbrick.cluster import KElbowVisualizer
logging.getLogger('pyomo.core').setLevel(logging.ERROR)

NUM_ITEMS = 10

i = [ii for ii in range(NUM_ITEMS)]
j = [jj for jj in range(NUM_ITEMS)]
s = ['x', 'y', 'z']
np.random.seed(50546)

def generateItems():    
    items = {i: {'x':np.random.randint(20, 60), 'y':np.random.randint(20, 60), 'z':np.random.randint(20, 60)} for i in range(NUM_ITEMS)}
    items2 = []
    for k in range(NUM_ITEMS):
        items2.append([items[k]['x'], items[k]['y'], items[k]['z']])
        
    return items, items2

lis, lis2 = generateItems()

Ls = {'x':59, 'y':59, 'z':25000}


   
model = KMeans()
visualizer = KElbowVisualizer(model, k=(1,NUM_ITEMS-1))
visualizer.fit(np.array(lis2))
kmeans = KMeans(n_clusters=visualizer.elbow_value_, random_state=0).fit(lis2)

bags = []
indexes = []
for g in range(visualizer.elbow_value_):
    bag = []
    index = []
    for gg in range(len(kmeans.labels_)):
        if kmeans.labels_[gg] == g:
            bag.append(lis2[gg])
            index.append(gg)
    bags.append(bag)
    indexes.append(index)

cis_bags = []
counter = 0
for bag in range(len(bags)):
    counter += 1
    print(counter)
    ncis = [[0,0,0] for i in range(len(bags[bag]))]
    ba = {r :{'x': bags[bag][r][0], 'y':bags[bag][r][1], 'z':bags[bag][r][2]} for r in range(len(bags[bag]))}
    
    
    i = j = indexes[bag]
    
    model = ConcreteModel()

    model.p_ijs = Var(i,j,s, within=Binary)
    
    model.c_is = Var(i,s, within=NonNegativeReals)
    
    model.h = Var(within=NonNegativeReals)
    
    model.objective = Objective(expr=model.h, sense=minimize)
    
    model.oneSpatialCorrelation = ConstraintList()
    for ii in range(len(i)):
        for jj in range(len(j)):
            if (jj > ii):
                model.oneSpatialCorrelation.add(sum((model.p_ijs[i[ii], j[jj], ss]+model.p_ijs[j[jj], i[ii], ss]) for ss in s)>=1)
    
    model.cannotPrecedeFollow = ConstraintList()
    for ii in range(len(i)):
        for jj in range(len(j)):
            if (jj > ii):
                for ss in s:
                    model.cannotPrecedeFollow.add(model.p_ijs[i[ii], j[jj],ss]+model.p_ijs[j[jj], i[ii],ss] <= 1)
    
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
    solver_manager = SolverFactory('gurobi_persistent')
    solver_manager.set_instance(model)
    print(solver_manager.solve())
    
    cis_new = [[model.c_is[ii,ss].value for ss in s] for ii in i]
    cis_bags.append(cis_new)
    
    

print(cis_bags)
for co in range(len(bags)):
    if co == 0:
        pass
    else:
        ls = [cis_bags[co-1][k][2]+bags[co-1][k][2] for k in range(len(cis_bags[co-1]))]
        mx = max(ls)
        ix = ls.index(mx)
        for g in range(len(bags[co])):
            cis_bags[co][g][2] += mx 


print(cis_bags)
            






  
 





# opt = SolverFactory("cplex")
# solver_manager = SolverManagerFactory('neos')
# results = solver_manager.solve(model, opt=opt)
# results.write()

# print(model.display(filename="result.txt"))