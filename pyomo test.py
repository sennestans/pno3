import pyomo.environ as pyo
import pyomo.opt as po
solver = po.SolverFactory('glpk')
m = pyo.ConcreteModel()
m.x = pyo.Var(within=pyo.NonNegativeReals)
m.aftrek = pyo.Var(within=pyo.NonNegativeReals)
m.waarde = 5 -m.aftrek
m.obj = pyo.Objective(expr=m.x -m.aftrek+ 1/3*m.waarde, sense=pyo.minimize)

m.conx1 = m.x <=5
m.conaftrek1 = m.aftrek <= m.x
m.con1 = pyo.Constraint(expr = m.conx1)
m.con2 = pyo.Constraint(expr = m.conaftrek1)

result = solver.solve(m)
print(result)
print(pyo.value(m.x))
print(pyo.value(m.aftrek))
print(pyo.value(m.waarde))
