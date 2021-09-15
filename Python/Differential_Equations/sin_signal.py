# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import matplotlib

if __name__ == '__main__':	
	font = {'family' : 'normal',		# Modifico el tamano de las letras y numeros del grafico
        	'weight' : 'bold',
        	'size'   : 18}
	matplotlib.rc('font', **font)

	fs=1000 					#Frecuencia de muestreo
	f=2							#Frecuencia de la senal deseada
	sample=1000 				#Cantidad de muestras
	x=np.arange(sample) 		#Generacion del vector de tiempos
	y=np.sin(2*np.pi*f*x/fs) 	#Generacion del vector de amplitudes
	plt.subplot(121) 			#Subplot para mostrar varias ventanas en una misma figura
	#plt.stem(x,y,'r',) 		#Detalle visual
	plt.plot(x,y,'r') 			#Impresion en pantalla del grafico
	plt.xlabel('Signal[n]') 	#Titulo eje x
	plt.ylabel('Amplitude[V]') 	#Titulo eje y
	print('Valor RMS de Signal1:')
	print(np.std(y))			#Calculo del valor RMS de la senal	
	print('Valor medio de Signal1:')
	print(np.mean(y))


	fs=1000
	f2=4
	sample2=1000
	x2=np.arange(sample2)
	y2=0.5*np.sin(2*np.pi*f2*x2/fs)+0.2	#Generacion de una senal de la mitad de la amplitud pero con el doble de frecuencia
	plt.subplot(122)
	#plt.stem(x,y,'r',)
	plt.plot(x2,y2,'b')
	plt.xlabel('Signal2[n]')
	plt.ylabel('Amplitude2[V]')
	plt.ylim([-1 , 1])					#Limito el maximo y minimo mostrado en el eje de amplitudes
	print('Valor RMS de Signal2:')
	print(np.std(y2))
	print('Valor medio de Signal2:')
	print(np.mean(y2))
	plt.show()
