'''
by Maddie Pero 

In this example we will get data from Airtable
'''

'''
These statements allow us to make get requests of the Airtable API & parse that information
'''
import requests # you may need to run 'pip install requests' to install this library
import json 


''' This function makes a get request to the airtable API which will tell us how fast to spin the wheels'''

''' Put the URL for your Airtable Base here'''
#URL = 'https://api.airtable.com/v0/appPFWlX5Bx83P1XM/Projects?api_key=keyV4gvD2zJLNdP6d'

#'https://api.airtable.com/v0/' + BaseID + '/' + tableName + '?api_key=' + APIKey

#r = requests.get(url = URL, params = {})
'''
The get request data comes in as a json package. We will convert this json package to a python dictionary so that it can be parsed
'''
URL = 'https://api.airtable.com/v0/appPFWlX5Bx83P1XM/Projects?api_key=keyV4gvD2zJLNdP6d'

r = requests.get(url = URL, params = {})


data1 = r.json()
#angular
Angularx=data1['records'][1]['fields']['X']
Angulary=data1['records'][1]['fields']['Y']
Angularz=data1['records'][1]['fields']['Z']

Linearx=data1['records'][2]['fields']['X']
Lineary=data1['records'][2]['fields']['Y']
Linearz=data1['records'][2]['fields']['Z']

#This is a dictionary
print(data1)
print(Linearx)




