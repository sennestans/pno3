#model warmtecircuit per 15 minuten
import numpy as np
import matplotlib.pyplot as plt
import random
#functions
def create_p_data(n):
    P_data = []
    N = n
    for _ in range(int(N)):
        random_num = random.randint(0, 6)
        P_data.extend([random_num]*1)
    return P_data
# Define parameters
t0 = 0
t_end = 24*60*60 #aantal seconden in een dag
n = 4*24 #aantal stappen = aantal minuten * 60 seconden, elke 15 minuten een stap
h = (t_end-t0)/(n) #dag wordt opgedeeld in 900 kwartieren
T_in_0 = 20 + 273.15
T_m_0 = 18 + 273.15
K_stop = 1000
# Parameters equations
C_i = 2.44*10**6
C_m = 9.40*10**7
R_i = 8.64*10**(-4)
R_e = 1.05*10**(-2)
R_vent = 7.98*10**(-3)
gA = 12
frad = 0.3

P_in = np.zeros(n)
P_data1 = create_p_data(n/2)
P_data1 = list(P_data1)
for i in range(int(n/4)):
    P_data1 += [0]
P_data2 = create_p_data(int(n/4))
P_data1 += list(P_data2)
#vul P_data tot lengte gelijk aan n
while len(P_data1) < n:
    P_data1 += [0]
print(P_data1)
#fill P_in with the values of P_data, each value is multiplied by 1500
for i in range(n):
    P_in[i] = P_data1[i] * 500
print(P_in)
CoP = 3
S_rad = []
#Maak een lijst S_rad met lengte n en vul deze met waarden tussen 0 en 100, normaal verdeeld rond het middelste element
for i in range(int(n/3)):
    S_rad += [0]
for i in range(int(n/3)):
    S_rad += [80]
for i in range(int(n/3)):
    S_rad += [0]
while len(S_rad) < n:
    S_rad += [0]
print(S_rad)
#
t = np.linspace(t0,t_end, n)
T_in = np.zeros([n])
T_m = np.zeros([n])
T_in[0] = T_in_0
T_m[0] = T_m_0
T_out = [10+273.15]
for i in range(60**3):
    T_out += [10+273.15]
for i in range(1,n):
    T_in[i] = T_in[i-1] + h * (1/C_i)*(P_in[i-1]*(1-frad)*CoP - (T_in[i-1]-T_out[i-1])/R_vent - (T_in[i-1]-T_m[i-1])/R_i)
    T_m[i] = T_m[i-1] + h * (1/C_m)*(P_in[i-1]*frad*CoP+gA*S_rad[i-1] - (T_m[i-1]-T_out[i-1])/R_e - (T_m[i-1]-T_in[i-1])/R_i)

#grafieken
plt.figure("Temperatuur")
plt.plot(t/(60*60),T_in-273.15,'b', label='T_in')
plt.plot(t/(60*60),T_m-273.15,'g', label='T_m')
plt.xlabel('Tijd (uur)')
plt.ylabel('Temperatuur (°C)')
plt.title('Binnen- en buitentemperatuur zonnehuis')
plt.grid()
plt.legend(loc='upper right')
plt.figure("Warmtepomp")
plt.plot(t/(60*60),P_in)
plt.xlabel('Tijd (uur)')
plt.ylabel('Vermogen (W)')
plt.title('Vermogen van de warmtepomp')
plt.grid()
plt.show()
#test!