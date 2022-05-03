# import flask dependencies
from flask import Flask, request, make_response
import json
import pandas as pd
import re
import random
import twilio
from twilio.rest import Client

# initialize the flask app
app = Flask(__name__)

generatedOTP = 0

# default route
@app.route('/')
def index():
	return 'Hello World!'


# create a route for webhook
@app.route('/webhook', methods=["POST"])
def webhook():
	global sendOTP
	global generatedOTP
	req = request.get_json(silent=True, force=True)
	result = req.get('queryResult')
	action = result.get('action')
	parameters = result.get('parameters')
	contact_no = parameters.get('contact_no')
	dob = parameters.get('dob')
	otp = parameters.get('otp')

	# initialize data of user as temp database table.
	data = {'Name': ['Rahul', 'Jack', 'nick', 'juli'],
			'PolicyNo': [123456, 111122, 333333, 444444],
			'ContactNo': [9561885596, 9874563210, 9632587410, 9874321010],
			'dob': ['14/03/97', '15/03/97', '16/03/97', '17/03/97'],
			'PolicyDetails': ['please find policy details', 'please find policy details', 'please find policy details', 'please find policy details'],
			'FundValue' : ['896.00', '321.32', '475.36', '547.23']}
	# Creates pandas DataFrame.
	df = pd.DataFrame(data, index=['1', '2', '3', '4'])

	if action == 'Act_Policy':
		if int(contact_no) in df.values:   # check if user exist
			res = json.dumps({'fulfillmentText': 'Here are your policy details.'})
			r = make_response(res)
			r.headers['Content-Type'] = 'application/json'
			return r
		else:
			res = json.dumps({'fulfillmentText': 'User not found'})
			r = make_response(res)
			r.headers['Content-Type'] = 'application/json'
			return r

	if action == 'Act_Fund':
		if int(contact_no) in df.values:  # check if user exist
			generatedOTP = sendOTP(contact_no)
			res = json.dumps({'fulfillmentText': 'Please enter the OTP'})
			r = make_response(res)
			r.headers['Content-Type'] = 'application/json'
			return r
		else:
			res = json.dumps({'fulfillmentText': 'User not found'})
			r = make_response(res)
			r.headers['Content-Type'] = 'application/json'
			return r


def sendOTP(contact_no):
	print('contact_no-', contact_no)
	otp = random.randint(100000, 999999)
	print("Your OTP is - ", otp)
	# Your Account Sid and Auth Token from twilio.com/console
	# DANGER! This is insecure. See http://twil.io/secure
	account_sid = 'AC5aea09f905a787131c81aec29c6c46e0'
	auth_token = '39d5ec88c9a7e3a36b78deb96fd48f41'
	client = Client(account_sid, auth_token)
	try:
		message = client.messages.create(
			body='Your OTP is - ' + str(otp) + '...',
			from_='+13254200323',
			to='+91'+contact_no
		)
		print(message.sid)
		return otp
	except Exception as e:
		return e


def verifyOTP(generatedOTP, otp):
	if generatedOTP != otp:
		return False
	else:
		return True


# run the app
if __name__ == '__main__':
	app.run(host='0.0.0.0')
