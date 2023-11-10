## Voorbeeld 1: slimme wasmachine

#Hallo!



#**Gegevens:** \
#We verdelen de dag in 3 tijdsintervallen: \
'''
t1 : 00h --> 08h \
t2: 08h --> 16h \
t3: 16h --> 24h \

Δt = 8h \\
'''
#De kost van energie voor elk tijdsinterval is: \
'''c1 = 0.1 EUR/kWh \
c2 = 0.5 EUR/kWh \
c3 = 0.3 EUR/kWh \
''''''
Gedurende deze dag moet de wasmachine 1 tijdsinterval aanstaan.
Wat is het optimale aan/uit-profiel van de wasmachine ervan uitgaande dat we zo weinig mogelijk willen betalen? \
wm1 ∈ {0,1} \
wm2 ∈ {0,1} \
wm3 ∈ {0,1} \

ewm = 0.15 kW
'''

Delta_t = 8 # tijdsinterval (h)

# kost energie (varieert per tijdsinterval) (EUR/kWh)
c1 = 0.1
c2 = 0.5 # meest gebruik over de middag
c3  = 0.3

ewm = 0.15 # verbruik wasmachine (kW = kWh/h)

'''

**Enkele afgeleide waarden** \
Reken de kost (EUR) uit om de wasmachine te laten draaien voor de totale duur van interval 1, 2 en 3



cost_wm_t1 = ...
cost_wm_t2 = ...
cost_wm_t3 = ...

**Optimalisatie**
'''
import pyomo.environ as pe
import pyomo.opt as po
solver = po.SolverFactory('glpk')

m = pe.ConcreteModel()
# Create variables: wm1, wm2, wm3: de aan/uit-stand van de wasmachine gedurende tijdsinterval t1, t2 en t3 respectivelijk
m.wm1 = pe.Var(domain = pe.Binary)
m.wm2 = pe.Var(domain = pe.Binary)
m.wm3 = pe.Var(domain = pe.Binary)

# Set objective: zo weinig mogelijk kosten
obj_expr = Delta_t*ewm*(c1*m.wm1 + c2*m.wm2 + c3*m.wm3)
m.obj = pe.Objective(sense = pe.minimize, expr = obj_expr)

# Add constraints: de wasmachine moet gedurende 1 tijdsinterval aanstaan
wm_con_expr = m.wm1 + m.wm2 + m.wm3 == 1
m.wm_con = pe.Constraint(expr = wm_con_expr)

# Optimize model
result = solver.solve(m)

print(result)

print(pe.value(m.obj))
print(pe.value(m.wm1))
print(pe.value(m.wm2))
print(pe.value(m.wm3))



#--> de optimale tijdsperiode om de wasmachine te laten draaien is periode t1: van middernacht tot 8h 's ochtends. De kost is 0.12 euro of 12 eurocent.

## Oefening 2: meer vuile was!
#Los op voor dezelfde situatie maar nu moet de wasmachine 2 tijdsperiodes gedraaid hebben.
wm_con_expr = m.wm1 + m.wm2 + m.wm3 == 2

m.wm_con = pe.Constraint(expr = wm_con_expr)

# Optimize model
result = solver.solve(m)

print(result)

print(pe.value(m.obj))
print(pe.value(m.wm1))
print(pe.value(m.wm2))
print(pe.value(m.wm3))


## Oefening 3
#Los op voor dezelfde situatie maar nu moet de wasmachine 2 tijdsperiodes na elkaar gedraaid hebben.

wm_con_expr = m.wm1 + m.wm2 + m.wm3==2
wm_con_expr_2 = m.wm1 + m.wm3 ==1

m.wm_con = pe.Constraint(expr = wm_con_expr)
m.wm_con_2 = pe.Constraint(expr = wm_con_expr_2)

# Optimize model
result = solver.solve(m)

print(result)

print(pe.value(m.obj))
print(pe.value(m.wm1))
print(pe.value(m.wm2))
print(pe.value(m.wm3))

## Oefening 4: + zonne-energie
'''Los op voor dezelfde situatie (wasmachine moet 1 tijdsperiode draaien), maar deze keer heb je een klein zonnepaneel ter beschikking

**extra gegevens** \
zonnepaneel_oppervlakte = 0.9 m<sup>2</sup> \
radiation_t1 = 50 W/m<sup>2</sup> \
radiation_t2 = 800 W/m<sup>2</sup> \
radiation_t3 = 200 W/m<sup>2</sup> \
efficientie_zonnepaneel = 20% \
(deze energie kost je niets!)
'''
# irradiantie van de zon (varieert per tijdsinterval) (kWh/m^2)
r1 = 0.05
r2 = 0.8 # meest zon over de middag
r3  = 0.2

zp_opp = 0.9 # oppervlakte zonnepaneel (m^2)
eff = 0.2  # efficientie zonnepaneel

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
obj_expr = (c1*m.ekoop1 + c2*m.ekoop2 + c3*m.ekoop3)
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
#print(result)

print(pe.value(m.obj))
print(pe.value(m.wm1))
print(pe.value(m.wm2))
print(pe.value(m.wm3))