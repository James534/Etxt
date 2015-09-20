import httplib2
import email
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Quickstart'


def get_credentials():
	"""Gets valid user credentials from storage.

	If nothing has been stored, or if the stored credentials are invalid,
	the OAuth2 flow is completed to obtain the new credentials.

	Returns:
		Credentials, the obtained credential.
	"""
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir,
								   'gmail-quickstart.json')

	store = oauth2client.file.Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else: # Needed only for compatability with Python 2.6
			credentials = tools.run(flow, store)
		print ('Storing credentials to ' + credential_path)
	return credentials

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
from httplib2 import Http

from apiclient import errors

from apiclient.discovery import build
credentials = get_credentials()
service = build('gmail', 'v1', http=credentials.authorize(Http()))

def GetMessage(service, user_id, msg_id):
	try:
		message = service.users().messages().get(userId=user_id,id=msg_id).execute()
		
		return message
	except errors.HttpError as error:
		print ("An error has occurred: %s" % error)

def SendMessage(service, user_id, message):
	"""Send an email message.

  Args:
	service: Authorized Gmail API service instance.
	user_id: User's email address. The special value "me"
	can be used to indicate the authenticated user.
	message: Message to be sent.

  Returns:
	Sent Message.
  """
	try:
		message = (service.users().messages().send(userId=user_id, body=message)
			   .execute())
		return message
	except errors.HttpError as error:
		print ('An error occurred: %s' % error)

def GetMimeMessage(service, user_id, msg_id):
	"""Get a Message and use it to create a MIME Message.

 	Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A MIME Message, consisting of data from Message.
	"""
	try:
		message = service.users().messages().get(userId=user_id, id=msg_id,
			format='raw').execute()

		msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

		mime_msg = email.message_from_string(msg_str)

		return mime_msg
	except errors.HttpError, error:
		print 'An error occurred: %s' % error


def CreateMessage(sender, to, subject, message_text):
	"""Create a message for an email.

  	Args:
	sender: Email address of the sender.
	to: Email address of the receiver.
	subject: The subject of the email message.
	message_text: The text of the email message.

  	Returns:
	An object containing a base64 encoded email object.
	"""

	message = MIMEText(message_text)
	message['to'] = to
	message['from'] = sender
	message['subject'] = subject
	return {'raw': base64.b64encode(message.as_string())}

def ListMessagesMatchingQuery(service, user_id, query=''):
	"""List all Messages of the user's mailbox matching the query.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        query: String used to filter messages returned.
        Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

    Returns:
        List of Messages that match the criteria of the query. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate ID to get the details of a Message.
	"""
	try:
		response = service.users().messages().list(userId=user_id, 
			q=query).execute()
		messages = []
		if 'messages' in response:
			messages.extend(response['messages'])

		while 'nextPageToken' in response:
			page_token = response['nextPageToken']
			response = service.users().messages().list(userId=user_id, q=query, 
                                         pageToken=page_token).execute()
			messages.extend(response['messages'])

		return messages
	except errors.HttpError as error:
		print ('An error occurred: %s' % error)



from flask import Flask, request, redirect
import twilio.twiml
from twilio.rest import TwilioRestClient
import requests
 
MAX_CHARS = 1550


class Etxt_server():
	def setup(self):
		f = open('data.txt', 'r')
		self.sid = f.readline().strip('\n')
		self.auth = f.readline().strip('\n')
		self.clientNumber = f.readline().strip('\n')
		self.serverNumber = f.readline().strip('\n')
		self.client = TwilioRestClient(self.sid, self.auth)
		self.domain = f.readline().strip('\n')
		self.mgkey = f.readline().strip('\n')
		self.fromemail = "sadmansazidk@gmail.com"
		self.toemail = "sadmansazidk@gmail.com"
		self.processingEmail = False
		self.recievedPieces = []		#list of messages to be pieced together
		self.recievedIndex  = []		#list of indexes of messages recieved

	#responces have to be less than 1562 characters
	def text(self, msg):
		message = self.client.messages.create(
			body="|" + msg,
			to=self.clientNumber,
			from_=self.serverNumber)
		#print (message.sid)
		print ('texting', msg)

	def checkMail(self):
		print ("Attempting to check for emails")
		messages = ListMessagesMatchingQuery(service, 'me', 'is:unread after:2015/09/18')

		for i in range(len(messages)):
			#get the full message
			message = GetMessage(service, 'me', messages[i]['id'])
			print (message)
			msg = ""
			for x in range(len(message['payload']['headers'])):
				if message['payload']['headers'][x]['name'].lower() == 'from':
					msg += message['payload']['headers'][x]['value']
				elif message['payload']['headers'][x]['name'].lower() == 'subject':
					msg += message['payload']['headers'][x]['value']

			for x in range(len(message['payload']['parts'])):
				if message['payload']['parts'][x]['mimeType'].lower() == 'text/plain':
					body = base64.urlsafe_b64decode(message['payload']['parts'][x]['body']['data'].encode('ASCII'))
					body = email.message_from_string(body)
					msg += str(body)
			self.sendMail(msg)


	def sendEmail(self, msg):
		print ("Attempting to dissect the message and send it: " + msg)
		#parse the target email and the subject
		target = msg[:msg.index('\n')]
		msg = msg[msg.index('\n')+1:]
		subject = msg[:msg.index('\n')]
		msg = msg[msg.index('\n')+1:]

		print ("Target", target)
		print ("Subject", subject)
		print ("msg", msg)

		#compose the email first
		message = CreateMessage(self.fromemail, target, subject, msg)

		#now send the email
		status = SendMessage(service, 'me', message)
		return status
		"""
		print ("Trying to send an email")
		#post the HTTP request to send the email
		r = requests.post(
				self.domain,
				auth=("api", self.mgkey),
				data={"from": self.fromemail,
					"to": self.toemail,
					"subject": "Will be parsed later from main text",
					"text": msg})

		#print the status of the request
		print (r.text)
		"""

	def sendMail(self, msg):
		if len(msg)+10 > MAX_CHARS:
			brokenMsg = []									#to hold all the broken down messages
			index = len(msg)/MAX_CHARS + 1
			maxIndex = index
			if (maxIndex < 10):
				strMaxIndex = '0' + str(maxIndex)
			else:
				strMaxIndex = str(maxIndex)

			wordIndex = 0

			for i in range (1, index+1):
				if (i < 10):
					counter = '0' + str(i) + '/' + strMaxIndex
				else:
					counter + str(i) + '/' + strMaxIndex
				brokenMsg.append(counter + msg[wordIndex:wordIndex+MAX_CHARS])
				wordIndex += MAX_CHARS

		#sending the messages after its all broken down
			for w in brokenMsg:
				self.text(w)
		else:
			self.text(msg)
			print ("EOF")

ES = Etxt_server()
ES.setup()


app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
	#resp = twilio.twiml.Response()
	rq = ES.client.messages.list();
	print ("____MESSAGE____")
	msg = rq[0].body
	print(msg)
	print(len(rq))
	#for x in range (0,5):
	#for message in rq:
	#	print (message.body)	
	#resp.message(rq[0].body)
	#resp.message(email)
	#return str(resp)
	if msg == 'check':
		ES.checkMail()
		return "eof"

	if not ES.processingEmail:
		if msg[2] == "/":
			ES.processingEmail = True
			ES.recievedIndex  = [False] * int(msg[3:5])		#make size of list = number of texts required
			ES.recievedPieces = [""] * int(msg[3:5])			#same with the text pieces
			ES.recievedIndex [int(msg[:2])] = True				#turn the current index to true
			ES.recievedPieces[int(msg[:2])] = msg[5:]
		else:
			ES.sendEmail(msg)
	else:
		done = True
		for i in range (len(ES.recievedIndex)):
			if ES.recievedIndex[i] == False:
				done = False
				break
		if done:
			finalMsg = ""
			for texts in ES.recievedPieces:
				finalMsg += texts
			ES.sendEmail(finalMsg)
			ES.processingEmail = False

		else:			
			ES.recievedIndex [int(msg[:2])] = True				#turn the current index to true
			ES.recievedPieces[int(msg[:2])] = msg[5:]

	ES.text(rq[0].body)
	#send an email
	#ES.sendEmail(rq[0].body)
	#ES.sendMail(email)
	return "eof"
 
if __name__ == "__main__":
	app.run(debug=True)
