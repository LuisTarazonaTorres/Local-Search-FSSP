# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 16:29:28 2022

@author: le.tarazona
"""
import pandas as pd
import numpy as np
from time import time
import random
from random import randint
#%% FUNCIÓN MAKESPAN
def makespan(secuencia, matriz_tiempos):
    m = len(matriz_tiempos[0])
    n = len(matriz_tiempos)
    
    matriz = [[matriz_tiempos[i][j] for j in secuencia]for i in range(n)]
    
    make = [[0 for j in range(m)]for i in range(n)]
    
    make[0][0] = matriz[0][0]
    
    for i in range(1,n):
        for j in range(1,m):
            make[0][j] = make[0][j-1] + matriz[0][j]
            make[i][j] = make[i-1][0] + matriz[i][0]
    
    for i in range(1,n):
        for j in range(1,m):
            if make[i][j-1] > make [i-1][j]:
                make[i][j] = make[i][j-1] + matriz[i][j]
            else:
                make[i][j] = make[i-1][j] + matriz[i][j]
    
    return(make[-1][-1])
#%% LLAMAR INSTANCIAS Y DATOS
Inst_1 = pd.read_fwf('tai500_20.txt', skiprows = 3, nrows = 20,header = None, delim_whitespace = True,skipinitialspace = True )
Inst_2 = pd.read_fwf('tai500_20.txt', skiprows = 26, nrows = 20,header = None, delim_whitespace = True,skipinitialspace = True )
Inst_3 = pd.read_fwf('tai500_20.txt', skiprows = 49, nrows = 20,header = None, delim_whitespace = True,skipinitialspace = True )
Inst_4 = pd.read_fwf('tai500_20.txt', skiprows = 72, nrows = 20,header = None, delim_whitespace = True,skipinitialspace = True )
Inst_5 = pd.read_fwf('tai500_20.txt', skiprows = 95, nrows = 20,header = None, delim_whitespace = True,skipinitialspace = True )
Inst_6 = pd.read_fwf('tai500_20.txt', skiprows = 118, nrows = 20,header = None, delim_whitespace = True,skipinitialspace = True )
Inst_7 = pd.read_fwf('tai500_20.txt', skiprows = 141, nrows = 20,header = None, delim_whitespace = True,skipinitialspace = True )
Inst_8 = pd.read_fwf('tai500_20.txt', skiprows = 164, nrows = 20,header = None, delim_whitespace = True,skipinitialspace = True )
Inst_9 = pd.read_fwf('tai500_20.txt', skiprows = 187, nrows = 20,header = None, delim_whitespace = True,skipinitialspace = True )
Inst_10 = pd.read_fwf('tai500_20.txt', skiprows = 210, nrows = 20,header = None, delim_whitespace = True,skipinitialspace = True )

ma = Inst_1 ##Cambiar instancia
ma_2 = ma[0]
ma_3 = ma_2.apply(lambda x: pd.Series(str(x).replace("  "," ").split(" ")))
ma_4 = ma_3.drop(columns = 0)
ma_5 = ma.drop(columns = 0)
tp = pd.concat([ma_4,ma_5],axis = 1)
tp.columns = list(range(0,500))
tp.index = list(range(0,20))

secuencia = list(range(0,500))
matriz_tiempos = tp.astype('int64')
matriz_tiempos = matriz_tiempos.to_numpy().tolist()
t = tp.astype('int64')
#%% SOLO INSTANCIA 10
tp = Inst_10 ## solo para la instancia 10
tp.columns = range(0,500)

secuencia = list(range(0,500))
matriz_tiempos = tp.astype('int64')
matriz_tiempos = matriz_tiempos.to_numpy().tolist()

#%% DETERMINAR MAKESPAN

start = time()
Cmax = makespan(secuencia, matriz_tiempos)
times = time() - start
print ("El tiempo de terminación es: ", Cmax)
print(times)

#%% FUNCIÓN SWAT

def swap(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list

#%% APLICACIÓN SWAT PRIMERA MEJORA
import matplotlib.pyplot as plt

control = time() 
secuencia1 = secuencia
secuencia2 = secuencia1
Cmax_ini = Cmax
Cmax_new = Cmax_ini
k =0
FOset = []

num_cambios = 6
for k in range(0,num_cambios):
    for i in range(0,250):
      for j in range (250, len(secuencia1)):
          Cmax_ini = Cmax_new
          pos1 = secuencia1[i]
          pos2 = secuencia1[j]
          secuencia2 = swap(secuencia2, pos1, pos2)
                 
          Cmax_new = makespan(secuencia2, matriz_tiempos)
      
          if Cmax_ini < Cmax_new:
              Cmax_new = Cmax_ini
              secuencia2 = secuencia1
              
              FOset.append(Cmax_new)
              print(Cmax_ini)
        
    k = k + 1
times = time() - control 
print(times)


plt.scatter(range(0,len(FOset)), FOset, color = 'purple')
plt.title('FO Instancia 09') #cambiar nombre a instancia
plt.xlabel('Iterations')
plt.ylabel('Objective')
plt.show()


#%%LS - INSERCIÓN
import matplotlib.pyplot as plt

control = time() 
secuencia1 = secuencia
secuencia2 = secuencia1
Cmax_ini = Cmax
Cmax_new = Cmax_ini
k =0
FOset = []

num_cambios = 300000
for k in range(0,num_cambios):
    Cmax_ini = Cmax_new
    insertar = randint(0, len(secuencia2)-1)
    insertarlo = randint(0,len(secuencia2)-1)
    secuencia2.insert(insertar,secuencia2.pop(insertarlo))  
    
    Cmax_new = makespan(secuencia2, matriz_tiempos)
    

    if Cmax_ini < Cmax_new:
        Cmax_new = Cmax_ini
        secuencia2.insert(insertarlo,secuencia2.pop(insertar))
        
        FOset.append(Cmax_new)
        
        print(Cmax_ini)
 
    k = k+1
times = time() - control 
print(times)


plt.scatter(range(0,len(FOset)), FOset, color = 'purple')
plt.title('FO Instancia 07') ##CAMBIAR NÚMERO DE INSTANCIA
plt.xlabel('Iterations')
plt.ylabel('Objective')
plt.show()

