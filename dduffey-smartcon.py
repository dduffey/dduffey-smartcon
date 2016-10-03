#!/usr/bin/python3

# In Degrees
mindiff = 1.0
maxdiff = 2.0

import json
import statistics

with open('sensors.json') as data_file:    
    data = json.load(data_file)

#print(data["thermostatList"][0]["settings"]["fanMinOnTime"])
#print(data["thermostatList"][0]["settings"]["fanMinOnTime"])

for thermostat in data["thermostatList"]:
	identifier=thermostat["identifier"]
	fanMinOnTime=thermostat["settings"]["fanMinOnTime"]
	temperatures = []
	for sensor in thermostat["remoteSensors"]:
		if sensor["inUse"]:
			for capability in sensor["capability"]:
				if capability["type"]=="temperature":
					temperatures.append(int(capability["value"])/10)
	pstdev=statistics.pstdev(temperatures)

	newFMOT=round(max(0,min(1,(pstdev-mindiff)/(maxdiff-mindiff)))*60)

	print('Thermostate:', identifier)
	print('Temperatures:',temperatures,'PSTDEV',pstdev)
	print('Fan Time:',fanMinOnTime,'->',newFMOT)

	if fanMinOnTime!=newFMOT:
		print('Changing FMOT to',newFMOT)


