#!/usr/bin/env python
# coding: utf-8

# In[42]:


#We need in the same repository the files: "eplusout.csv", "cop.csv", "objective.cvs"
#Once it runs, it takes the output of energy plus, the extimated cop at different time and the electrical energy consumption of the building it can estimate the total error (loss) with different functions
#and write on error.txt the result

import numpy as np

#We take the cop at each time of the year and store it in an array
cop_file="cop.csv"
cop=np.array([])
with open(cop_file,"r") as f:
    for value in f:
        cop=np.append(cop,float(value))
        

#File is the output of energy plus simulation
eplus_file = "eplusout.csv" 

#We create a dictionary to store the monthly sum of electrical energy consume
Energy_month={1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0}

#Let's open the file and read it line by line
with open(eplus_file,"r") as f:
    
    #in this first part we find in which column the energy is stored
    for line in f:
            words=line.split(",")
            if len(words)==0:
                    continue
            column=0
            for j in words:
                if j[:38]=='DistrictHeating:Facility [J](TimeStep)':
                    pass
                else:
                    column+=1
            break
            
    #Once we know this, we can start summing hour by hour the energy contribution
    i=0
    sim=False
    for line in f:
        data=line.split(",")
        if data[0]==" 01/01  00:10:00" or data[0]==" 01/01  00:10:00":
            sim=True
        if data[0]==" 04/15  00:10:00" or data[0]==" 04/15  00:10:00":
            sim=False
        if data[0]==" 10/15  00:10:00" or data[0]==" 10/15  00:10:00":
            sim=True
        if sim!=True:
            continue
        energy=float(data[column])/3.6*10**(-6)
        month=int((data[0].split("/"))[0])
        Energy_month[month]+=energy/cop[int(np.floor(i/6))]
        i+=1
output=np.array(list(Energy_month.values()))
        

#We now take the values we want to achieve and find the distance through different metrics
def rmse(objective,output):
    r=(objective-output)**2
    return np.sqrt(np.sum(r))
def abserr(objective,output):
    r=np.absolute((objective-output))
    return np.sum(r)
def evaluation(function,objective,output):
    return function(objective,output)

#Possibly to modify to make it automatic (takes as an input the function to use)
function=rmse

objective_file="objective.csv"
objective=np.array([])
with open(objective_file,"r") as f:
    for value in f:
        objective=np.append(objective,float(value))
error=evaluation(function,objective,output)

#We print the result on a file
with open('error.txt', 'w') as f:
    f.write(str(error))

