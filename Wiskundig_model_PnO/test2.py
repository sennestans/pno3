import random

def create_p_data(n):
    P_data = []
    for _ in range(n):
        random_num = random.randint(0, 4)
        P_data.extend([random_num] * 4)
    return P_data

n = 10
P_data = create_p_data(n)
print(P_data)
mylist = [str(1)]
mylist = [float(i) for i in mylist]
myotherlist = [int(1)]
print(float(1)+1)
print(mylist[0]+1)
print(myotherlist[0]+1)
P_out = [1,2, 3, 4, 5]
T_out = [1,2, 3, 4, 5]
S_rad = [1,2, 3, 4, 5]
N = 2
def extend_list(L, N):
    temp_list = []
    for i in L:
        temp_list.extend([i] * N)
    return temp_list
for L in [P_out, T_out, S_rad]:  # voor elke lijst in de van de input
    temp_list = []  # maak een tijdelijke lijst
    for i in L:  # voor elk element in de lijst L
        temp_list.extend([i] * N)  # voeg het element N keer toe aan de tijdelijke lijst
    L = temp_list  # vervang de lijst L door de tijdelijke lijst
print(P_out)
print(T_out)
print(S_rad)
print(extend_list(P_out, N))
print(extend_list(T_out, N))
print(extend_list(S_rad, N))
import numpy as np
from scipy.integrate import odeint, solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def lorenz(t, state, sigma, beta, rho):
    x, y, z = state

    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z

    return [dx, dy, dz]


sigma = 10.0
beta = 8.0 / 3.0
rho = 28.0

p = (sigma, beta, rho)  # Parameters of the system

y0 = [1.0, 1.0, 1.0]  # Initial state of the system

t_span = (0.0, 40.0)
t = np.arange(0.0, 40.0, 0.01)

result_odeint = odeint(lorenz, y0, t, p, tfirst=True)
result_solve_ivp = solve_ivp(lorenz, t_span, y0, args=p)

fig = plt.figure()
ax = fig.add_subplot(1, 2, 1, projection='3d')
ax.plot(result_odeint[:, 0],
        result_odeint[:, 1],
        result_odeint[:, 2])
ax.set_title("odeint")

ax = fig.add_subplot(1, 2, 2, projection='3d')
ax.plot(result_solve_ivp.y[0, :],
        result_solve_ivp.y[1, :],
        result_solve_ivp.y[2, :])
ax.set_title("solve_ivp")
plt.show()