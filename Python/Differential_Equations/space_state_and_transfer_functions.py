# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import matplotlib
from scipy.signal import lti, step2
import scipy

#R-C en paralelo con L, en serie con un capacitor en derivacion
if __name__=='__main__' :
	font = {'family' : 'normal',
        	'weight' : 'bold',
        	'size'   : 18}
	matplotlib.rc('font', **font);
	
	R = 10e-3
	L = 10e-3										# Variables a utilizar
	C1 = 10e-6
	C2 = 10e-6
	
	A = [ [ 0 , 1 , -1/L ] ,						# Generacion de las matrices de estado, cada coma
	 	[0 , -1/(C1*R) , -1/(C1*R)] , 			#  fuera de los corchetes separa las filas de la matriz
	 	[ 1/C2 , -1/(C2*R) , -1/(C2*R)] ]
	
	B = [ [1/L] , 
		[1/(C1*R)] , 
		[1/(C2*R)] ]

	C = [0,0,1]
	D = [1/R]

	SYS1 = signal.StateSpace(A,B,C,D)				# Generacion de un objeto a partir de las matrices
	t = np.linspace(0,20,400)						# Generacion del vector de tiempos
	t1,y1 = signal.step(SYS1, T=t)					# Calculo de la respuesta al escalon del sistema
	plt.xlabel('t[s]')	
	plt.ylabel('Vo(t) [V]')
	plt.plot(t1,y1)
	plt.show()
	
