from flask import Flask, request, redirect
import twilio.twiml
from twilio.rest import TwilioRestClient
 
class Etxt_server():

	def setup(self):
		f = open('data.txt', 'r')
		#self.url            = f.readline().strip('\n')
		#self.webController  = f.readline().strip('\n')
		self.sid = f.readline().strip('\n')
		self.auth = f.readline().strip('\n')
		self.clientNumber = f.readline().strip('\n')
		self.serverNumber = f.readline().strip('\n')
		self.client = TwilioRestClient(self.sid, self.auth)
		#print(self.url)

	def text(self, msg):
		message = self.client.messages.create(
			body="|" + msg,
			to=self.clientNumber,
			from_=self.serverNumber)
		#print (message.sid)
		print ('texting', msg)
		#print (msg)

ES = Etxt_server()
ES.setup()
#ES.text("HELLO WORLD")
#print("EOF")

app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""
    resp = twilio.twiml.Response()
    rq = ES.client.messages.list();
    print ("MESSAGE")
    print(rq[0].body)
    print(len(rq))
    #for x in range (0,5):
    #	print(rq[x].body)
    #for message in rq:
    #	print (message.body)
    resp.message(rq[0].body)
    return str(resp)
 
if __name__ == "__main__":
    app.run(debug=True)