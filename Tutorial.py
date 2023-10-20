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

wm_con_expr = (m.wm1 ==1 and m.wm2 == 1 and m.wm3==0) or m.wm1 ==1 & m.wm2 == 1 or
wm_con_expr = m.wm2 + m.wm3 == 2
wm_con_expr = m.wm1 + m.wm2 + m.wm3 == 2

m.wm_con = pe.Constraint(expr = wm_con_expr)
m.wm_con = pe.Constraint(expr = wm_con_expr)
m.wm_con = pe.Constraint(expr = wm_con_expr)

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

# irradiantie van de zon (varieert per tijdsinterval) (kWh/m^2)
r1 = 0.05
r2 = 0.8 # meest zon over de middag
r3  = 0.2

zp_opp = 0.9 # oppervlakte zonnepaneel (m^2)
eff = 0.2  # efficientie zonnepaneel
'''