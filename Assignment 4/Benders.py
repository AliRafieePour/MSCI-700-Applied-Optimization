from pyomo.environ import *
import time
#subproblem

def subproblem(y):
    model = ConcreteModel()
    model.dual = Suffix(direction=Suffix.IMPORT)

    model.mu = Var([1,2,3,4,5], within=NonNegativeReals)
    
    model.objective = Objective(expr=model.mu[1]*(4-10*y[1]-8*y[2])+model.mu[2]*(3-5*y[1]-8*y[3]), sense=maximize)
    
    model.constraint = Constraint(expr=-(-8+2*model.mu[1]+model.mu[2]-model.mu[3]) == 0)
    model.constraint2 = Constraint(expr=-(-6+model.mu[1]+model.mu[2]-model.mu[4]) == 0)
    model.constraint3 = Constraint(expr=-(2-model.mu[1]+model.mu[2]-model.mu[5]) == 0)
    
    solver_manager = SolverFactory('gurobi_persistent')
    solver_manager.set_instance(model)
    solver_manager.solve()
    mu = [model.mu[i].value for i in [1,2,3,4,5]]
    print(f"mu={mu}")
    
    z= [0]
    for c in [model.constraint,model.constraint2,model.constraint3]:
        z.append(model.dual[c])
    print(f"z={z}")
    return z,{i: model.mu[i].value for i in [1,2,3,4,5]}

def subproblem2(y):
    model = ConcreteModel()
    model.dual = Suffix(direction=Suffix.IMPORT)
    model.z= Var([1,2,3], within=NonNegativeReals)
    
    model.constraint1 = Constraint(expr=10*y[1]+8*y[2]-2*model.z[1]-model.z[2]+model.z[3]>=4)
    model.constraint2 = Constraint(expr=5*y[1]+8*y[3]-model.z[1]-model.z[2]-model.z[3]>=3)
    
    model.obj = Objective(expr=-8*model.z[1]-6*model.z[2]+2*model.z[3],sense=minimize)

    solver_manager = SolverFactory('gurobi_persistent')
    solver_manager.set_instance(model)
    solver_manager.solve()
    
    mu = [0]
    for c in [model.constraint1,model.constraint2]:
        mu.append(model.dual[c])
    
    z = [0]
    for i in [1,2,3]:
        z.append(model.z[i].value)
    
    return z,mu
    
    
    
def masterproblem():
    model = ConcreteModel()
    model.y = Var([1,2,3], within=Binary)
    model.theta = Var()
    model.constraint = Constraint(expr= model.y[1]+model.y[2]+model.y[3]>=1)
    model.cuts = ConstraintList()
    
    model.objective = Objective(expr=12*model.y[1]+20*model.y[2]+15*model.y[3]+model.theta,sense=minimize)
    UB = 1000000
    LB = -1000000
    y = [0,1,0,0]
    while(UB!=LB):
        z, mu = subproblem(y)
        print(f"mu={mu}")
        print(f"z={z}")
        model.cuts.add(expr=model.theta>=mu[1]*(4-10*model.y[1]-8*model.y[2])+mu[2]*(3-5*model.y[1]-8*model.y[3]))
        
        solver_manager = SolverFactory('glpk') 
        results = solver_manager.solve(model)
        #print(model.display())

        UB = model.objective.value()
        print(f"UB={UB}")
        y = [0,model.y[1].value, model.y[2].value, model.y[3].value]
        print(f"y={y}")
        LB = upperBound(y, z)
        print(f"LB={LB}")

        print(f"theta={model.theta.value}")
        print("****")
        time.sleep(5)


def upperBound(y,z):
    return 12*y[1]+20*y[2]+15*y[3]-8*z[1]-6*z[2]+2*z[3]

masterproblem()

