import pyomo.environ as pyo
import pyomo.opt as po
solver = po.SolverFactory('glpk')
m = pyo.ConcreteModel()

m.ebuy = pyo.Var(pyo.RangeSet(1, 4), within=pyo.NonNegativeReals)
m.con = pyo.ConstraintList()

for i in range(1, 4):
    m.con.add(m.ebuy[i] <= 1)

m.obj = pyo.Objective(expr = sum(m.ebuy[i] for i in range(1, 4)), sense= pyo.maximize)
result = solver.solve(m)
print(result)