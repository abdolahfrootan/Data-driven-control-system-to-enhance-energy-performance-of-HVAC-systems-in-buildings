#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#This file need "test.csv", 'temperature_t_step.csv', in future an input file to work
#Power_supply= A_surface*fraction_active*Solar radiation incident*module efficiency(T)*DC to AC efficiency
#module efficiency(T) from table
#T of the cell
            #  -> decoupled Ullberg Dynamic

import numpy as np

Solar_rad_file='test.csv'
Solar_incident_radiation=np.array([])
with open(Solar_rad_file,"r") as f:
    for line in f:
        words=line.split(";")
        for i in range(6):
            Solar_incident_radiation=np.append(Solar_incident_radiation,float(words[3]))

temperature='temperature_t_step.csv'
temperatures=np.array([])
with open(temperature,"r") as f:
    for line in f:
        temperatures=np.append(temperatures,float(line))

def T_cell(T_ambient,efficiency,tau_alpha,G_T,UL,T_a=20):
    if G_T!=0:
        T_c=T_a+(1-efficiency/tau_alpha)/(G_T*tau_alpha/UL)
    else: T_c=T_a
    return T_c

def module_efficiency(T_cell):
    efficiency=22.6-(T_cell-25>0)*0.27*(T_cell-25)
    return efficiency

def PV(Solar_incident_radiation,module_efficiency,DC_to_AC_efficiency,area=231,fraction=1):
    Pv=area*fraction*Solar_incident_radiation*module_efficiency*DC_to_AC_efficiency*10**(-3)
    Pv=(Pv<36/6)*Pv+(Pv>36/6)*36/6 #total production of energy is less than 36 kW
    return Pv


efficiency=module_efficiency(temperatures)/100

DC_AC=98.3/100
energy=PV(Solar_incident_radiation,efficiency,DC_AC)

with open('PV.txt', 'w') as f:
    for i in energy:
        f.write(str(i)+"\n") #values are in one column, stored in kWh!!!

