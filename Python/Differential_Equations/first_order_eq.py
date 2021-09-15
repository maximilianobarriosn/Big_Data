# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import matplotlib

'''
	Ejercicio 5 GTP 3
'''

'''
	Calculo de la derivada de la funcion
'''
def derivative(Vc,t_aux):
	''' 
		Generacion de la senal de entrada Vi y retorno la expresion
		de la derivada de mayor orden segun la ecuacion diferencial.
		En este caso Vc' = Vi/RC - Vc/RC
	'''
	Vamp=0.5
	R=2
	C=1
	Vi=Vamp					# Vi seria un escalon
	#Vi=Vamp*np.cos(t_aux)	# Vi seria una senoidal
	#Vi=t_aux*Vamp			# Vi seria una rampa
	return (Vi-Vc)*1/(R*C)

'''
	Resolucion utilizando ODEINT
'''
if __name__=='__main__':
	font = {'family' : 'normal',	# Modifico el tamano de las letras y numeros del grafico
        	'weight' : 'bold',
        	'size'   : 22}

	matplotlib.rc('font', **font)
	t=np.linspace(0,20,100) 			# Vector de tiempos
	Vc0=0								# Condicion inicial
	Vo=odeint(derivative,Vc0,t)			# Llamado a ODEINT
	Vo=np.array(Vo).flatten()			# Devuelvo una copia del vector
	plt.xlabel("t[s]")
	plt.ylabel("Vo(t) [V]")
	plt.plot(t,Vo)
	plt.show()	
