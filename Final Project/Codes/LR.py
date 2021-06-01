from pyomo.environ import *
import random
import numpy as np

import logging
logging.getLogger('pyomo.core').setLevel(logging.ERROR)
from time import time 

NUM_ITEMS = 5

i = [ii for ii in range(NUM_ITEMS)]
j = [jj for jj in range(NUM_ITEMS)]
s = ['x', 'y', 'z']
np.random.seed(50546)

def generateItems():    
    items = {i: {'x':np.random.randint(20, 60), 'y':np.random.randint(20, 60), 'z':np.random.randint(20, 60)} for i in range(NUM_ITEMS)}
    return items

lis = generateItems()
Ls = {'x':59, 'y':59, 'z':10000}

t1 = 0
t2 = 0

def subproblem1(mu):
    
    model = ConcreteModel('Sub Problem 1')
    model.pijs = Var(i,j,s, within=Binary)
    
    model.oneSpatialCorrelation = ConstraintList()
    for ii in range(len(i)):
        for jj in range(len(j)):
            if (jj > ii):
                model.oneSpatialCorrelation.add(sum((model.pijs[ii, jj, ss]+model.pijs[jj, ii, ss]) for ss in s)>=1)
                model.oneSpatialCorrelation.add(sum((model.pijs[ii, jj, ss]+model.pijs[jj, ii, ss]) for ss in s if ss=='z')==1)

    model.cannotPrecedeFollow = ConstraintList()
    for ii in range(len(i)):
        for jj in range(len(j)):
            if (jj > ii):
                for ss in s:
                    if ss=='z':
                        model.cannotPrecedeFollow.add(model.pijs[ii,jj,ss]+model.pijs[jj,ii,ss] == 1)
                    else:
                        model.cannotPrecedeFollow.add(model.pijs[ii,jj,ss]+model.pijs[jj,ii,ss] <= 1)
                    

    #print((mu))
    
    model.obj = Objective(expr=sum(mu[ii,jj,ss]*Ls[ss]*model.pijs[ii,jj,ss] for ss in s for jj in j for ii in i if ii != jj), sense=minimize)

    ### SOLVE
    solver_manager = SolverFactory('gurobi_persistent')
    solver_manager.set_instance(model)
    solver_manager.solve()

    pijs = {(ii,jj,ss): model.pijs[ii,jj,ss].value for ii in i for jj in j for ss in s}
    
    return pijs, model.obj.value()
    

def subproblem2(mu):
    
    model = ConcreteModel('Sub Problem 2')
    model.cis = Var(i,s, within=NonNegativeReals)
    model.h = Var(within=NonNegativeReals)
    
    model.withinBoundaries = ConstraintList()
    for ii in i:
        for ss in s:
            model.withinBoundaries.add(0<=model.cis[ii,ss]<=Ls[ss]-lis[ii][ss])
            
    model.maxHeight = ConstraintList()
    for ii in i:
        model.maxHeight.add(model.cis[ii,'z'] + lis[ii]['z']<=model.h)
        model.maxHeight.add(lis[ii]['z']<=model.h)
        
    model.objective = Objective(expr=model.h + sum(mu[ii,jj,ss]*(model.cis[ii,ss]-model.cis[jj,ss]) for ss in s for jj in j for ii in i if ii!=jj), sense=minimize)
    
    ### SOLVE
    solver_manager = SolverFactory('gurobi_persistent')
    solver_manager.set_instance(model)
    solver_manager.solve()
    
    cis = {(ii,ss): model.cis[ii,ss].value for ii in i for ss in s}
    h = model.h.value
    
    #print(h)
    #print(cis)
    return cis, h, model.objective.value()
        

def masterproblem():
    t1 = time()
    model = ConcreteModel('Master Problem')
    model.theta = Var([1,2])
    model.mu = Var(i,j,s, within=NonNegativeReals, bounds=(None, 25000))
    model.constraint1 = ConstraintList()
    model.constraint2 = ConstraintList()
    
    model.objective = Objective(expr=model.theta[1] + model.theta[2] + sum(model.mu[ii,jj,ss]*(lis[ii][ss]-Ls[ss]) for ss in s for jj in j for ii in i if ii!=jj), sense=maximize)
    
    mu = {(ii,jj,ss): 123 for ii in i for jj in j for ss in s}
    sol = []
    bes = 0
    master_bes = 1
    while(int(bes)!=int(master_bes)):
        pijs, obj1 = subproblem1(mu)
        cis, h, obj2 = subproblem2(mu)

        model.constraint1.add(expr=model.theta[1] <= sum(model.mu[ii,jj,ss]*Ls[ss]*pijs[ii,jj,ss] for ii in i for jj in j for ss in s if ii!=jj))
        model.constraint2.add(expr=model.theta[2] <= h + sum(model.mu[ii,jj,ss]*(cis[ii,ss]-cis[jj,ss]) for ss in s for jj in j for ii in i if ii!=jj))
        
        ### SOLVE
        solver_manager = SolverFactory('gurobi_persistent')
        solver_manager.set_instance(model)
        print(solver_manager.solve())

        #print(model.display())
        mu = {(ii,jj,ss):model.mu[ii,jj,ss].value for ii in i for jj in j for ss in s}
        
        master_bes = model.objective.value()
        sol.append(obj1 + obj2 + sum(mu[ii,jj,ss]*(lis[ii][ss]-Ls[ss]) for ii in i for jj in j for ss in s if ii != jj))
        
        bes = max(sol)
        
        print((bes, master_bes))
    
    t2 = time()
    print(mu)
    print("##########")
    print(sol)
    import matplotlib.pyplot as plt
    plt.plot(sol)
    plt.show()
    
    #print(model.pprint())
    
    #print(f"pijs={pijs}")
    print(f"cis={cis}")
    #print(f"new (2) cis= {heuristic(pijs, cis)}")
    
    
    

def masterproblem2():
    t1 = time()
    print("t1", t1)
    mu = {(ii,jj,ss): 12 for ii in i for jj in j for ss in s}
    sol = []
    bes = 0
    master_bes = 1
    for rr in range(4):
        pijs, obj1 = subproblem1(mu)
        cis, h, obj2 = subproblem2(mu)

        print(obj1 + obj2 + sum(mu[ii,jj,ss]*(lis[ii][ss]-Ls[ss]) for ii in i for jj in j for ss in s if ii != jj))
        sol.append(obj1 + obj2 + sum(mu[ii,jj,ss]*(lis[ii][ss]-Ls[ss]) for ii in i for jj in j for ss in s if ii != jj))

        #print(model.display())
        for ii in i:
            for jj in j:
                for ss in s:
                    if (ii!= jj):
                        mu[ii,jj,ss] = min(0, mu[ii,jj,ss] -0.001*(cis[ii, ss] - lis[ii][ss] - cis[jj,ss] - Ls[ss]*(1-pijs[ii,jj,ss])))
        
        
        bes = max(sol)
        
        print(bes)
    
    t2 = time()
    print("t2", t2)
    print("t2-t1", t2,t1, t2-t1)
    print(mu)
    
    print("##########")
    print(sol)
    #print(model.pprint())
    
    #print(f"pijs={pijs}")
    #print(f"cis={cis}")
    #print(f"new (2) cis= {heuristic(pijs, cis)}")







masterproblem2()

print(t2-t1)




                        