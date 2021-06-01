from pyomo.environ import *
import logging
import numpy as np
logging.getLogger('pyomo.core').setLevel(logging.ERROR)
from pyomo.util.infeasible import log_infeasible_constraints

NUM_ITEMS = 25

i = [ii for ii in range(NUM_ITEMS)]
j = [jj for jj in range(NUM_ITEMS)]
s = ['x', 'y', 'z']
np.random.seed(50546)

def generateItems():    
    items = {i: {'x':np.random.randint(20, 60), 'y':np.random.randint(20, 60), 'z':np.random.randint(20, 60)} for i in range(NUM_ITEMS)}
    return items

lis = generateItems()
Ls = {'x':59, 'y':59, 'z':500}

def slave(p_ijs):
    model = ConcreteModel('Slave Problem')
    model.dual = Suffix(direction=Suffix.IMPORT)
    
    model.cis = Var(i,s,within=NonNegativeReals)
    model.h = Var(within=NonNegativeReals)
    
    model.objective = Objective(expr=model.h, sense=minimize)
             
    model.withinBoundaries = ConstraintList()
    for ii in i:
        for ss in s:
            model.withinBoundaries.add(0<=model.cis[ii,ss]<=Ls[ss]-lis[ii][ss])
    
    model.nonOverlapping = ConstraintList()
    for ii in i:
        for jj in j:
            if (ii != jj):
                for ss in s:
                    model.nonOverlapping.add(model.cis[ii,ss] + lis[ii][ss] <= model.cis[jj,ss]+ Ls[ss]*(1- p_ijs[ii,jj,ss]))
    
    model.maxHeight = ConstraintList()
    for ii in i:
        model.maxHeight.add(model.cis[ii,'z'] + lis[ii]['z']<=model.h)
    
    model.pprint()
    
    ### SOLVE
    solver_manager = SolverFactory('gurobi_persistent')
    solver_manager.set_instance(model)
    solver_manager.solve()
    
    log_infeasible_constraints(model)

    
    h = model.h.value
    cis = {(ii,ss):model.cis[ii,ss].value for ii in i for ss in s}
    

        
    return h, cis

def master():
    model = ConcreteModel('Master Problem')
            
    model.theta = Var(within=NonNegativeReals)
    model.pijs = Var(i,j,s, within=Binary)
    model.cis = Var(i,s, within=NonNegativeReals)
    model.objective = Objective(expr=model.theta, sense=minimize)
    for ww in range(5):
        
        model.oneSpatialCorrelation = ConstraintList()
        for ii in range(len(i)):
            for jj in range(len(j)):
                if (jj > ii):
                    model.oneSpatialCorrelation.add(sum((model.pijs[ii, jj, ss]+model.pijs[jj, ii, ss]) for ss in s)>=1)
        
        model.cannotPrecedeFollow = ConstraintList()
        for ii in range(len(i)):
            for jj in range(len(j)):
                if (jj > ii):
                    for ss in s:
                        model.cannotPrecedeFollow.add(model.pijs[ii,jj,ss]+model.pijs[jj,ii,ss] <= 1)
        
        
        ### SOLVE
        solver_manager = SolverFactory('gurobi_persistent')
        solver_manager.set_instance(model)
        solver_manager.solve()
        
        pijs = {(ii,jj,ss):model.pijs[ii,jj,ss].value for ii in i for jj in j for ss in s}
        
        return pijs

pijs =master()
#print(slave(pijs))