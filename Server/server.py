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
		self.fromemail = f.readline().strip('\n')
		self.toemail = f.readline().strip('\n')

	#responces have to be less than 1562 characters
	def text(self, msg):
		message = self.client.messages.create(
			body="|" + msg,
			to=self.clientNumber,
			from_=self.serverNumber)
		#print (message.sid)
		print ('texting', msg)

	def sendEmail (self, msg):
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

	def sendMail(self, msg):
		if len(msg)+10 > MAX_CHARS:
			brokenMsg = []									#to hold all the broken down messages
			index = len(msg)/MAX_CHARS + 1
			maxIndex = index
			if (maxIndex < 10):
				strMaxIndex = '0' + str(maxIndex)
			else:
				strMaxIndex = str(maxIndex)
			#firstMsg = self.startingHash + msg[:MAX_CHARS]
			#brokenMsg.append(firstMsg)
			#index -= 1
			wordIndex = 0

			for i in range (1, index+1):
				if (i < 10):
		   			counter = '0' + str(i) + '/' + strMaxIndex
				else:
					counter + str(i) + '/' + strMaxIndex
				brokenMsg.append(counter + msg[wordIndex:wordIndex+MAX_CHARS])
				wordIndex += MAX_CHARS

		#index = MAX_CHARS-6								#since im taking max_chars-6 characters in the first message, make the index max_chars-6
		#length = len(msg) + 10 - MAX_CHARS-6			#current length of the email
		#words = ES.startingHash + msg[0:MAX_CHARS-6]	#the first message to be sent
		#brokenMsg.append(words)							#add the first message to the list 
		#for x in range (0, (len(msg)+10)/MAX_CHARS):		#+6 because 1 from the | character and 5 from the possible start/end hash
		#brokenMsg.append(msg[index:index+MAX_CHARS])
		#print(msg[index:index+MAX_CHARS])
		#index += MAX_CHARS

		#sending the messages after its all broken down
			for w in brokenMsg:
				self.text(w)
		else:
			self.text(msg)
			print ("EOF")

ES = Etxt_server()
ES.setup()
#email = open("sampleEmail.txt", 'r').read()
words = "WASDSADSADSADAS"

app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
	"""Respond to incoming texts"""
	#resp = twilio.twiml.Response()
	rq = ES.client.messages.list();
	print ("____MESSAGE____")
	print(rq[0].body)
	print(len(rq))
	#for x in range (0,5):
	#for message in rq:
	#	print (message.body)	
	#resp.message(rq[0].body)
	#resp.message(email)
	#return str(resp)
	ES.text(rq[0].body)
	#send an email
	ES.sendEmail(rq[0].body)
	#ES.sendMail(email)
	return "eof"
 
if __name__ == "__main__":
	app.run(debug=True)
