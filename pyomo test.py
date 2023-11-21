#een functie om de actuele tijd bij te houden
def klok(t):
    if t+1 < 24:
        return t+1
    else:
        return 0

Delta_t = 1 # tijdsinterval (h)
horizon = 17 # dit is de duur van ons tijdsinterval
wm_aanuit = 1
auto_aanuit = 1

actuele_tijd = klok(0)
print(actuele_tijd)
#start- en stopuren
wm_startuur = 8
wm_einduur = 16
auto_startuur = 19
auto_einduur = 6
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
#zitten we binnen het interval wanneer de auto aanwezig is?
if actuele_tijd < auto_startuur//24 and actuele_tijd >= auto_einduur//24:
    index = auto_einduur - actuele_tijd
    auto_con_tijd1 = sum(m.auto[i] for i in range(1,index)) == 0
    m.auto_con_tijd1 = pe.Constraint(expr = auto_con_tijd1)
if (actuele_tijd+horizon)//24 < auto_einduur//24 and (actuele_tijd + horizon)//24 >= auto_einduur//24:
    index_einduur = horizon
    index_startuur_uit = (auto_einduur-actuele_tijd)//24
    auto_con_tijd2 = sum(m.auto[i] for i in range(index_startuur_uit,index_einduur)) == 0
    m.auto_con_tijd2 = pe.Constraint(expr= auto_con_tijd2)


# energie die we kopen en zelf verkopen
m.ebuy = pe.Var(pe.RangeSet(1,horizon), within=pe.NonNegativeReals)

m.esell = pe.Var(pe.RangeSet(1,horizon), within=pe.NonNegativeReals)

peerijs = sum(kost[i-1]/1000*(m.ebuy[i]-1/3*m.esell[i]) for i in range(1,horizon))
m.obj = pe.Objective(expr= peerijs, sense = pe.minimize)

#auto staat 1 interval aan
auto_con_expr = sum(m.auto[i] for i in range(1,horizon)) == 3*auto_aanuit
m.auto_con = pe.Constraint(expr = auto_con_expr)

# Add constraints: de wasmachine moet gedurende 2 tijdsintervallen aanstaan
wm_con_expr = sum(m.wm[i] for i in range(1,horizon)) == 2*wm_aanuit
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


result = solver.solve(m)
print(result)
for i in range(1,horizon):
    print(pe.value(m.auto[i]), 'tijdsinterval voor auto', i)
for i in range(1,horizon):
    print(pe.value(m.wm[i]), 'tijdsinterval voor wm', i)
print(pe.value(m.ebuy[10]))
print(pe.value(m.esell[10]))
print(eff*zp_opp*irradiantie[9]*kost[9]/1000)

