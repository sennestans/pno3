print('objectief')
Delta_t = 8 # tijdsinterval (h)

# kost energie (varieert per tijdsinterval) (EUR/kWh)
c1 = 0.1
c2 = 0.5 # meest gebruik over de middag
c3  = 0.3

ewm = 0.15 # verbruik wasmachine (kW = kWh/h)

# irradiatie van de zon (varieert per tijdsinterval) (kWh/m^2)
r1 = 0.05
r2 = 0.8 # meest zon over de middag
r3  = 0.2

zp_opp = 0.9 # oppervlakte zonnepaneel (m^2)
eff = 0.2  # efficientie zonnepaneel

import pyomo.environ as pe
import pyomo.opt as po
solver = po.SolverFactory('glpk')

m = pe.ConcreteModel()

# Create variables: wm1, wm2, wm3: de aan/uit-stand van de wasmachine gedurende tijdsinterval t1, t2 en t3 respectivelijk
m.wm1 = pe.Var(domain = pe.Binary)
m.wm2 = pe.Var(domain = pe.Binary)
m.wm3 = pe.Var(domain = pe.Binary)
# Create additional help variables: e1, e2, e3: aangekochte energie gedurende t1, t2 en t3 respectievelijk
m.e1 = pe.Var()
m.e2 = pe.Var()
m.e3 = pe.Var()

m.E1 = pe.Var()
m.E2 = pe.Var()
m.E3 = pe.Var()

#zonne-energie over per uur
m.tank1 = r1*zp_opp*eff - m.E1
m.tank2 = r2*zp_opp*eff - m.E2
m.tank3 = r3*zp_opp*eff - m.E3
# Set objective: zo weinig mogelijk kosten
obj_expr = (c1*m.e1 + c2*m.e2 + c3*m.e3) -4*(m.tank1+m.tank2+m.tank3)
m.obj = pe.Objective(sense = pe.minimize, expr = obj_expr)

# Add constraints: de wasmachine moet gedurende 2 tijdsintervallen aanstaan
wm_con_expr = m.wm1 + m.wm2 + m.wm3 == 1
m.wm_con = pe.Constraint(expr = wm_con_expr)

# constraints tank en zonne energie
# E_i betekent wat we gebruiken van de energie opgewekt door zonnepannelen in 1 tijdsinterval

con_E1 = m.E1 >= 0
con_E2 = m.E2 >= 0
con_E3 = m.E3 >= 0
con_E1_2 = m.E1 <= m.tank1
con_E2_2 = m.E2 <= m.tank2
con_E3_2 = m.E3 <= m.tank3
con_E1_3 = m.E1 <= ewm
con_E2_3 = m.E2 <= ewm
con_E3_3 = m.E3 <=ewm

# constraints toepassen
m.var1 = pe.Constraint(expr= con_E1)
m.var2 = pe.Constraint(expr= con_E1_2)
m.var3 = pe.Constraint(expr= con_E1_3)
m.var4 = pe.Constraint(expr= con_E2)
m.var5 = pe.Constraint(expr= con_E2_2)
m.var6 = pe.Constraint(expr= con_E2_3)
m.var7 = pe.Constraint(expr= con_E3)
m.var8 = pe.Constraint(expr= con_E3_2)
m.var9 = pe.Constraint(expr= con_E3_3)

# Add constraints: energiebalans per tijdsinterval
con_eb1_expr = m.e1 == Delta_t*m.wm1*(ewm - m.E1)
con_eb2_expr = m.e2 == Delta_t*m.wm2*(ewm - m.E2)
con_eb3_expr = m.e3 == Delta_t*m.wm3*(ewm - m.E3)
m.eb1 = pe.Constraint(expr = con_eb1_expr)
m.eb2 = pe.Constraint(expr = con_eb2_expr)
m.eb3 = pe.Constraint(expr = con_eb3_expr)


## Optimize model
result = solver.solve(m)

print(result)

print(pe.value(m.obj))

print(pe.value(m.wm1))
print(pe.value(m.wm2))
print(pe.value(m.wm3))
print(pe.value(m.E1))
print(pe.value(m.E3))
print(pe.value(m.E2))