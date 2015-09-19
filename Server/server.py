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
ES.text("HELLO WORLD")
print("EOF")