from pyomo.environ import *

model = ConcreteModel()

model.y = Var([1,2,3], within=Binary)
model.z = Var([1,2,3], within=NonNegativeReals)

model.obj = Objective(expr=12*model.y[1]+20*model.y[2]+15*model.y[3]-8*model.z[1]-6*model.z[2]+2*model.z[3], sense=minimize)

model.constraint1 = Constraint(expr=10*model.y[1]+8*model.y[2]-2*model.z[1]-model.z[2]+model.z[3]>=4)
model.constraint2 = Constraint(expr=5*model.y[1]+8*model.y[3]-model.z[1]-model.z[2]-model.z[3]>=3)
model.constraint3 = Constraint(expr=model.y[1]+model.y[2]+model.y[3]>=1)

### SOLVE
solver_manager = SolverFactory('glpk')

results = solver_manager.solve(model)

print(model.display())