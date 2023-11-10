Delta_t = 8 # tijdsinterval (h)

# kost energie (varieert per tijdsinterval) (EUR/kWh)
c1 = 0.1
c2 = 0.5 # meest gebruik over de middag
c3  = 0.3

ewm = 0.15 # verbruik wasmachine (kW = kWh/h)
# irradiantie van de zon (varieert per tijdsinterval) (kWh/m^2)
r1 = 0
r2 = 0 # meest zon over de middag
r3  = 0

zp_opp = 0.9 # oppervlakte zonnepaneel (m^2)
eff = 0.2  # efficientie zonnepaneel

M = 1000 # grote M
import pyomo.environ as pe
import pyomo.opt as po
solver = po.SolverFactory('glpk')

m = pe.ConcreteModel()
# variabelen z1 en z2 die zeggen of we kopen of verkopen
m.z1_1 = pe.Var(domain = pe.Binary)
m.z1_2 = pe.Var(domain = pe.Binary)
m.z1_3 = pe.Var(domain = pe.Binary)
m.z2_1 = pe.Var(domain = pe.Binary)
m.z2_2 = pe.Var(domain = pe.Binary)
m.z2_3 = pe.Var(domain = pe.Binary)

m.conz = pe.Constraint(expr = m.z1_1 + m.z2_1 <= 1)
m.conz2 = pe.Constraint(expr = m.z1_2 + m.z2_2 <= 1)
m.conz3 = pe.Constraint(expr = m.z1_3 + m.z2_3 <= 1)
# Create variables: wm1, wm2, wm3: de aan/uit-stand van de wasmachine gedurende tijdsinterval t1, t2 en t3 respectivelijk
m.wm1 = pe.Var(domain = pe.Binary)
m.wm2 = pe.Var(domain = pe.Binary)
m.wm3 = pe.Var(domain = pe.Binary)

# energie die we kopen en zelf verkopen
m.ebuy1 =  pe.Var(within=pe.NonNegativeReals)
m.ebuy2 =  pe.Var(within=pe.NonNegativeReals)
m.ebuy3 =  pe.Var(within=pe.NonNegativeReals)

m.esell1 =  pe.Var(within=pe.NonNegativeReals)
m.esell2 =  pe.Var(within=pe.NonNegativeReals)
m.esell3 =  pe.Var(within=pe.NonNegativeReals)

peerijs = c1*(m.ebuy1-1/3*m.esell1) + c2*(m.ebuy2-1/3*m.esell2) + c3*(m.ebuy3-1/3*m.esell3)
m.obj = pe.Objective(expr= peerijs, sense = pe.minimize)

# Add constraints: de wasmachine moet gedurende 2 tijdsintervallen aanstaan
wm_con_expr = m.wm1 + m.wm2 + m.wm3 == 1
m.wm_con = pe.Constraint(expr = wm_con_expr)
# Add constraints: energiebalans per tijdsinterval
con_eb1 = m.ebuy1 - m.esell1 == -r1*zp_opp*eff + ewm*m.wm1*Delta_t
con_eb2 = m.ebuy2 - m.esell2 == -r2*zp_opp*eff + ewm*m.wm2*Delta_t
con_eb3 = m.ebuy3 - m.esell3 == -r3*zp_opp*eff + ewm*m.wm3*Delta_t

m.eb1 = pe.Constraint(expr = con_eb1)
m.eb2 = pe.Constraint(expr = con_eb2)
m.eb3 = pe.Constraint(expr = con_eb3)
# een maximum instellen om te kunnen kopen en verkopen
con_buymax1 = m.ebuy1 <= M*m.z1_1
con_buymax2 = m.ebuy2 <= M*m.z1_2
con_buymax3 = m.ebuy3 <= M*m.z1_3
con_sellmax1 = m.esell1 <= M*m.z2_1
con_sellmax2 = m.esell2 <= M*m.z2_2
con_sellmax3 = m.esell3 <= M*m.z2_3

m.buymax1 = pe.Constraint(expr = con_buymax1)
m.buymax2 = pe.Constraint(expr = con_buymax2)
m.buymax3 = pe.Constraint(expr = con_buymax3)
m.sellmax1 = pe.Constraint(expr = con_sellmax1)
m.sellmax2 = pe.Constraint(expr = con_sellmax2)
m.sellmax3 = pe.Constraint(expr = con_sellmax3)

result = solver.solve(m)
print(result)
print(pe.value(m.ebuy1))
print(pe.value(m.ebuy2))
print(pe.value(m.ebuy3))
print(pe.value(m.esell1))
print(pe.value(m.esell2))
print(pe.value(m.esell3))