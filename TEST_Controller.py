#imports
from Simuleer_warmte_model.py import simuleer_warmte_model
#een functie om de actuele tijd bij te houden

Delta_t = 1 # tijdsinterval (h)
horizon = 10 # dit is de duur van ons tijdsinterval

# kost energie (varieert per tijdsinterval) (EUR/kWh)
kost = [533.92,479.90,480,428.70,407.75,402.06,550,598.90,600,613.59,575.09,560,525.40,526.69,528.77,521.99,511.39,542.04,580.42,645.07,644.38,600.06,552.73,524.93]

ewm = 2.5 # verbruik wasmachine (kW = kWh/h)
eau = 7.4 # vermogen laadpaal (kW)

# irradiantie van de zon (varieert per tijdsinterval) (kWh/m^2)

irradiantie = [0,0,0,0,0,0,0,0.1,0.3,0.4,0.8,1.2,2,1.6,2.2,1.2,0.3,0.3,0.2,0.1,0,0,0,0]

zp_opp = 22.4 # oppervlakte zonnepaneel (m^2)
eff = 0.2  # efficientie zonnepaneel

M = 1000 # grote M
import pyomo.environ as pe
import pyomo.opt as po
solver = po.SolverFactory('glpk')

m = pe.ConcreteModel()
# variabelen bkoop en bverkoop die binair zeggen of we kopen of verkopen
m.bkoop = pe.Var(pe.RangeSet(1,horizon), domain = pe.Binary)
m.bverkoop = pe.Var(pe.RangeSet(1,horizon), domain = pe.Binary)

m.conb = pe.ConstraintList()
for i in range(1,horizon):
    m.conb.add(m.bkoop[i] + m.bverkoop[i] <= 1)

# Create variables: wm1, wm2, wm3: de aan/uit-stand van de wasmachine gedurende tijdsinterval 1 tot 24 respectivelijk

m.wm = pe.Var(pe.RangeSet(1,horizon), domain = pe.Binary)

#aan uitstand auto
m.auto = pe.Var(pe.RangeSet(1,horizon), domain = pe.Binary)

# energie die we kopen en zelf verkopen
m.ebuy = pe.Var(pe.RangeSet(1,horizon), within=pe.NonNegativeReals)

m.esell = pe.Var(pe.RangeSet(1,horizon), within=pe.NonNegativeReals)

peerijs = sum(kost[i-1]/1000*(m.ebuy[i]-1/3*m.esell[i]) for i in range(1,horizon))
m.obj = pe.Objective(expr= peerijs, sense = pe.minimize)

#auto staat 1 interval aan
auto_con_expr = sum(m.auto[i] for i in range(1,horizon)) == 3
m.auto_con = pe.Constraint(expr = auto_con_expr)

# Add constraints: de wasmachine moet gedurende 2 tijdsintervallen aanstaan
wm_con_expr = sum(m.wm[i] for i in range(1,horizon)) == 2
m.wm_con = pe.Constraint(expr = wm_con_expr)

# 2 tijdsintervallen na elkaar voor het wasmachien
m.wm_start = pe.Var(pe.RangeSet(1,horizon), domain = pe.Binary)
wm_startcon_expr = sum(m.wm_start[i] for i in range(1,horizon)) == 1
m.wm_startcon = pe.ConstraintList()
m.wm_startcon.add(m.wm[1] == m.wm_start[1])
for k in range(2,horizon):
    m.wm_startcon.add(m.wm[k] == m.wm_start[k-1] + m.wm_start[k])

# Add constraints: energiebalans per tijdsinterval
m.con_eb = pe.ConstraintList()
for j in range(1,horizon):
    m.con_eb.add(m.ebuy[j] - m.esell[j] == -irradiantie[j-1]*zp_opp*eff + ewm*m.wm[j]*Delta_t + eau*m.auto[j]*Delta_t)


# een maximum instellen om te kunnen kopen en verkopen
m.con_buymax = pe.ConstraintList()
for n in range(1,horizon):
    m.con_buymax.add(m.ebuy[n] <= M*m.bkoop[n])

m.con_sellmax = pe.ConstraintList()
for l in range(1,horizon):
    m.con_sellmax.add(m.esell[l] <= M*m.bverkoop[l])
##horizon implementatie
horizon_length = 12  # Lengte van de horizon in tijdstappen (bijv. 12 uur)

current_time = 0  # Begin met tijd 0
total_time = 36
while current_time < total_time:

    # Definieer de huidige horizon op basis van de huidige tijd
    horizon_start = current_time
    horizon_end = min(current_time + horizon_length, total_time)

    # Maak een nieuw optimalisatieprobleem voor de huidige horizon
    # Dit omvat het opstellen van variabelen, constraints, en doelfunctie op basis van de huidige horizon

    # Definieer je variabelen, parameters, constraints en doelfunctie voor de huidige horizon
    # ...

    # Los het optimalisatieprobleem op

result = solver.solve(m)
print(result)
for i in range(1,horizon):
    print(pe.value(m.auto[i]), 'tijdsinterval voor auto', i)
for i in range(1,horizon):
    print(pe.value(m.wm[i]), 'tijdsinterval voor wm', i)
print(pe.value(m.ebuy[10]))
print(pe.value(m.esell[10]))
print(eff*zp_opp*irradiantie[9]*kost[9]/1000)

