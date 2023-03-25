import sys
# pathnameto_eppy = 'c:/eppy'
pathnameto_eppy = '../'
sys.path.append(pathnameto_eppy)

from eppy import modeleditor
from eppy.modeleditor import IDF

iddfile = "/Applications/OpenStudio-2.9.1/EnergyPlus/Energy+.idd"
fname1 = "/Users/abdollahforoutan/ml4iot/in.idf"

IDF.setiddname(iddfile)
idf1 = IDF(fname1)

#print(idf1.idfobjects['ScheduleTypeLimits'][21]) # put the name of the object you'd like to look at in brackets
#idf1.idfobjects['ScheduleTypeLimits'][0].Name
#print(idf1.idfobjects['Schedule:Day:Interval'][0].Time_1)



#print(len('Schedule:Day:Interval'))
#print(idf1.idfobjects['Schedule:Day:Interval'][-1]) # put the name of the object you'd like to look at in brackets
#idf1.saveas('something2.idf')


#to finde schedule object to do any changes we have to know object day number on mondays it is something like this: Schedule day 19
#tin order to do that we have to lookup on the Schedule:Week:Daily.[].names to fined the name we want 
#then we have to return  monday day nname of the same object which is unique name for schedule:day:interval[].names list 
#after finding the object we remove it and make a newobject with the same name ant attrebute but different time schedules
times=['08:00','10:00','15:00','24:00']
values=[1,0,0,0]
def schedule_modifier(schedule_name , times_list, value_list ):
    #between all Schedule:Week:Daily we should find the on which has the name we looking for
    objects = idf1.idfobjects['Schedule:Week:Daily']
    for object in range(len(objects)):
        if idf1.idfobjects['Schedule:Week:Daily'][object].Name == schedule_name:
            
            corresponding_day=idf1.idfobjects['Schedule:Week:Daily'][object].Monday_ScheduleDay_Name
    #then we have to fine schedule:day:interval object with corresponding_day
    interval_objects = idf1.idfobjects['Schedule:Day:Interval']
    for interval_object in range(len(interval_objects)):
        if  idf1.idfobjects['Schedule:Day:Interval'][interval_object].Name == str(corresponding_day):
            #here we store some att of corresponding obj in order to not loos anything becasue we just want to change intervals not the other att
            corresponding_object= idf1.idfobjects['Schedule:Day:Interval'][interval_object].Value_Until_Time_1
            att3=idf1.idfobjects['Schedule:Day:Interval'][interval_object].Interpolate_to_Timestep
            att2=idf1.idfobjects['Schedule:Day:Interval'][interval_object].Schedule_Type_Limits_Name
            obect_index=interval_object
    #remove object from idf file
    num_befor=len(idf1.idfobjects['Schedule:Day:Interval'])
    removed_obj=idf1.idfobjects['Schedule:Day:Interval'].pop(obect_index) 
    num_after=len(idf1.idfobjects['Schedule:Day:Interval'])

    #generate dictionary of new item 
    
    new_item_args={
        'Name':removed_obj.Name,
        'Interpolate_to_Timestep':removed_obj.Interpolate_to_Timestep,
        'Schedule_Type_Limits_Name':removed_obj.Schedule_Type_Limits_Name
    }
    #add time intervals and values to the arg dictionary
    for i in range(len(times)):
        new_item_args[f'Time_{i+1}']=times[i]
        new_item_args[f'Value_Until_Time_{i+1}']=values[i]

    #create a new object based on new time intervals and values
    newobj=idf1.newidfobject("Schedule:Day:Interval",defaultvalues=False,**new_item_args)
    idf1.saveas('something.idf')
    return corresponding_object,att2,att3,num_befor,num_after,removed_obj,newobj

def single_parameter_modifier(object_type, zone_name, new_value): #people , zone name
    #based on object type we have to descide what is the name of attrebute would be change
    if object_type == "People": #---> Number of People
        objects=idf1.idfobjects['People']
        for object in range(len(objects)):
            if idf1.idfobjects['People'][object].Zone_or_ZoneList_Name == zone_name: 
                idf1.idfobjects['People'][object].Number_of_People = new_value #here it is

    
    if object_type == "Lights": #---> Lighting Level
        objects=idf1.idfobjects['Lights']
        for object in range(len(objects)):
            if idf1.idfobjects['Lights'][object].Zone_or_ZoneList_Name == zone_name: 
                idf1.idfobjects['Lights'][object].Lighting_Level = new_value #here it is

    if object_type == "Lights": #---> Lighting Level
        objects=idf1.idfobjects['Lights']
        for object in range(len(objects)):
            if idf1.idfobjects['Lights'][object].Zone_or_ZoneList_Name == zone_name: 
                idf1.idfobjects['Lights'][object].Lighting_Level = new_value #here it is
    idf1.saveas('something.idf')
    return
    



        

  





    

a=schedule_modifier('Lighting hallway Week Rule - Jan1-Dec31',0,0)
print(a)


