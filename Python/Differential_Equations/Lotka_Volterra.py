# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


#Ecuacion de Lotka-Volterra
'''
    dx/dt=αx−βxy
    dy/dt=−γy+δyx
    
    Ecuacion diferencial acoplada ( las variables dependientes se ven envueltas en 
    ambas ecuaciones diferenciales ), autonoma ( la variable independiente no aparece 
    explicitamente ) y no lineal. 

    a: es la tasa instantánea de aumento de conejos en ausencia de zorros
    b: es la tasa instantánea de disminución de zorros en el caso de ausencia de conejos.
    c: mide la susceptibilidad de los conejos a ser cazados.
    d: mide la capacidad de depredación de los zorros
'''

a,b,c,d = 1,1,1,1

def dP_dt(P, t):
    return [P[0]*(a - b*P[1]), -P[1]*(c - d*P[0])]

ts = np.linspace(0, 12, 100)
P0 = [1.5, 1.0]
Ps = odeint(dP_dt, P0, ts)
prey = Ps[:,0]
predators = Ps[:,1]

'''
	Poblaciones en funcion del tiempo
'''
plt.subplot(311)
plt.plot(ts, prey, "+", label="Rabbits")
plt.plot(ts, predators, "x", label="Foxes")
plt.xlabel("Time")
plt.ylabel("Population")
plt.legend();

'''
	Poblacion de zorros en funcion de la poblacion de conejos
'''
plt.subplot(312)
plt.plot(prey, predators, "-")
plt.xlabel("Rabbits")
plt.ylabel("Foxes")
#plt.title("Rabbits vs Foxes");


'''
	Poblacion de zorros en funcion de la poblacion de conejos variando parametros iniciales
'''
plt.subplot(313)
ic = np.linspace(1.0, 3.0, 21)
for r in ic:
    P0 = [r, 1.0]
    Ps = odeint(dP_dt, P0, ts)
    plt.plot(Ps[:,0], Ps[:,1], "-")
plt.xlabel("Rabbits")
plt.ylabel("Foxes")
#plt.title("Rabbits vs Foxes");

plt.show()