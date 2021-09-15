# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import matplotlib

'''
	Calculo de la derivada de la funcion y generacion de la senal de entrada
'''
def derivative(Vo,t_aux):
	Vamp=0.5
	#Vi=Vamp					# Vi seria un escalon
	Vi=Vamp*np.cos(2*t_aux)		# Vi seria una senoidal
	#Vi=t_aux*Vamp				# Vi seria una rampa
	return [Vo[1], -2*Vo[1] -2*Vo[0] + Vi]	# Retorno la expresion de la derivada de mayor orden

'''
	Resolucion utilizando ODEINT
	Ecuacion diferencial: 
	Vo(t)″+2*Vo(t)′+2Vo(t)=Vamp*cos(2t)
'''
if __name__=='__main__':
	font = {'family' : 'normal',	# Modifico el tamano de las letras y numeros del grafico
        	'weight' : 'bold',
        	'size'   : 18}
	matplotlib.rc('font', **font);
	t=np.linspace(0,20,1000) 		#Vector de tiempos
	Y0=[ 0 , 0]						#Condiciones iniciales
	Y=odeint(derivative,Y0,t)		#Vectores de la salida y su derivada primera (y , y')
	y_t=Y[:,0]						#Primer parametro :Me quedo con todas las filas (:) 
									#Segundo parametro : me quedo solo con la primer columna (0)
	
	plt.xlabel("t[s]")
	plt.ylabel("y_t(t) [V]")
	plt.plot(t,y_t)
	plt.show()