Delta_t = 8 # tijdsinterval (h)

# kost energie (varieert per tijdsinterval) (EUR/kWh)
c1 = 0.1
c2 = 0.5 # meest gebruik over de middag
c3  = 0.3

ewm = 0.15 # verbruik wasmachine (kW = kWh/h)
# irradiantie van de zon (varieert per tijdsinterval) (kWh/m^2)
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
m.ekoop1 = pe.Var()
m.ekoop2 = pe.Var()
m.ekoop3 = pe.Var()

m.verkoop1 = pe.Var()
m.verkoop2 = pe.Var()
m.verkoop3 = pe.Var()

# Set objective: zo weinig mogelijk kosten
obj_expr = (c1*m.ekoop1 + c2*m.ekoop2 + c3*m.ekoop3) -1/3*(m.verkoop1 + m.verkoop2 + m.verkoop3)
m.obj = pe.Objective(sense = pe.minimize, expr = obj_expr)

# Add constraints: de wasmachine moet gedurende 2 tijdsintervallen aanstaan
wm_con_expr = m.wm1 + m.wm2 + m.wm3 == 1
m.wm_con = pe.Constraint(expr = wm_con_expr)
# Add constraints: energiebalans per tijdsinterval
con_eb1_expr = m.ekoop1 == max(0,Delta_t*m.wm1*(ewm - r1*zp_opp*eff))
con_eb2_expr = m.ekoop2 == max(0,Delta_t*m.wm2*(ewm - r2*zp_opp*eff))
con_eb3_expr = m.ekoop3 == max(0,Delta_t*m.wm3*(ewm - r3*zp_opp*eff))

con_everkoop1 = m.verkoop1 == min(0,Delta_t*m.wm1*(ewm - r1*zp_opp*eff))
con_everkoop2 = m.verkoop2 == min(0,Delta_t*m.wm2*(ewm - r2*zp_opp*eff))
con_everkoop3 = m.verkoop3 == min(0,Delta_t*m.wm3*(ewm - r3*zp_opp*eff))


m.eb1 = pe.Constraint(expr = con_eb1_expr)
m.eb2 = pe.Constraint(expr = con_eb2_expr)
m.eb3 = pe.Constraint(expr = con_eb3_expr)
m.everkoop1 = pe.Constraint(expr = con_everkoop1)
m.everkoop2 = pe.Constraint(expr = con_everkoop2)
m.everkoop3 = pe.Constraint(expr = con_everkoop3)


print(pe.value(m.obj))
print(pe.value(m.wm1))
print(pe.value(m.wm2))
print(pe.value(m.wm3))
