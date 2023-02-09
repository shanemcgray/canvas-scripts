'''
This script will be run at the beginning of every other script.
It handles the authentication with the Canvas environment.
It also allows the user to select which environment to work in (test, production, multiple institutions, etc.)
A Canvas admin must create an access token and use it as the 'password' for this script.
'''

# Import the Canvas API and a password-entry library
from canvasapi import Canvas
import pwinput

# This is the function that will be called from the other scripts
def Start():
	# Create a dictionary containing the URLS for all the Canvas environments an admin may need to connect to.
	canvasUrls = {
		1: 'https://example.instructure.com',
		2: 'https://example.test.instructure.com',
		3: 'https://example.beta.instructure.com'
	}
	# Present the choice to the user
	print('\nSelect Canvas environment to use.\n')
	for env in canvasUrls:
		print(str(env) + ": " + canvasUrls[env])
	envChoice = int(input(""))
	# Set API_URL to the user's choice from canvasUrls
	API_URL = canvasUrls[envChoice]
	# Securely store the user's access token in API_KEY using the library pwinput
	API_KEY = pwinput.pwinput(prompt='Enter API key: ')
	# Initialize a new Canvas object
	canvas = Canvas(API_URL, API_KEY)
	# Return three things to the script calling startSession:
	# canvas 		| the canvas object 								| access with startSession.Start()[0]
	# canvasUrls 	| the dictionary containing available Canvas URLS 	| access with startSession.Start()[1]
	# envChoice 	| the number declaring which environment to use 	| access with startSession.Start()[2]
	return canvas, canvasUrls, envChoice

