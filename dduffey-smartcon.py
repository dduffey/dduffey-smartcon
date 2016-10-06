#!/usr/bin/python3

# Applicaiton API Key
api_key='uf6hfcAXSr3nK9joQd75QMMoXHirtXRa'

# In Degrees
mindiff = 1.0
maxdiff = 2.0

import requests
import json
import statistics

#url = 'https://api.ecobee.com/authorize'
#params = {'response_type': 'ecobeePin',
#          'client_id': api_key, 'scope': 'smartWrite'}
#request = requests.get(url, params=params)
#authorization_code = request.json()['code']
#pin = request.json()['ecobeePin']
#print('Please authorize your ecobee developer app with PIN code '
#      + pin + '\nGoto https://www.ecobee.com/consumerportal'
#      '/index.html, click\nMy Apps, Add application, Enter Pin'
#      ' and click Authorize.\nAfter authorizing, call request_'
#      'tokens() method.')
#print('authorization_code',authorization_code)

authorization_code=

#url = 'https://api.ecobee.com/token'
#params = {'grant_type': 'ecobeePin', 'code': authorization_code,
#          'client_id': api_key}
#request = requests.post(url, params=params)
#if request.status_code == requests.codes.ok:
#    access_token = request.json()['access_token']
#    refresh_token = request.json()['refresh_token']
#else:
#    print('Error while requesting tokens from ecobee.com.'
#          ' Status code: ' + str(request.status_code))
#
#print('access_token',access_token)
#print('refresh_token',refresh_token)

access_token=
refresh_token=

url = 'https://api.ecobee.com/1/thermostat'
header = {'Content-Type': 'application/json;charset=UTF-8',
          'Authorization': 'Bearer ' + access_token}
params = {'json': ('{"selection":{"selectionType":"registered",'
                    '"includeSensors":"true",'
                    '"includeSettings":"true"}}')}
request = requests.get(url, headers=header, params=params)
if request.status_code == requests.codes.ok:
    authenticated = True
    thermostats = request.json()['thermostatList']
else:
    authenticated = False
    print("Error connecting to Ecobee while attempting to get "
          "thermostat data.  Refreshing tokens and trying again.")

#with open('sensors.json') as data_file:    
#    data = json.load(data_file)

#print(data["thermostatList"][0]["settings"]["fanMinOnTime"])
#print(data["thermostatList"][0]["settings"]["fanMinOnTime"])

#for thermostat in data["thermostatList"]:
for thermostat in thermostats:
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

# TODO
# actually change the run time
# refesh keys
# store tokens
# use existing library
