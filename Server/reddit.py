import praw
from flask import Flask, request, redirect
import twilio.twiml
from twilio.rest import TwilioRestClient
import requests

r = praw.Reddit(user_agent='my_cool_app')
submissions = r.get_subreddit("dota2").get_hot(limit=10)
y = ['']*11
i = 0
for x in submissions:
	txt = x.selftext.lower()
	print x
	y[i] = x
	i+=1
	print("______________")
	print(txt)
	#flat_comments = praw.helpers.flatten_tree(x.comments)
	#for comment in x.comments:#flat_comments:
#		print comment
	#print("===================================")

#s = r.get_submission("https://www.reddit.com/r/DotA2/comments/3lkiju/chess_supergrandmaster_ian_nepomniachtchi_wearing/")
#s = r.get_submission(y)
#for x in range (10):
#for comment in s.comments:
#	comment = s.comments[x]
	#print("===============")
#	print(comment.author)
#	print("------------")
#	print(comment.body)
#	print("------------")
#	for cr in comment.replies:
#		print ("  " + cr.body)
#		for cr2 in cr.replies:
#			print ("    " + cr2.body)

class Comm():
	def setup(self):
		f = open('data.txt', 'r')
		self.sid = f.readline().strip('\n')
		self.auth = f.readline().strip('\n')
		self.clientNumber = f.readline().strip('\n')
		self.serverNumber = f.readline().strip('\n')
		self.client = TwilioRestClient(self.sid, self.auth)
		self.subReddit = ""
		self.url = ""

	#responces have to be less than 1562 characters
	def text(self, msg):
		message = self.client.messages.create(
			body="|" + msg,
			to=self.clientNumber,
			from_=self.serverNumber)
		#print (message.sid)
		print ('texting', msg)

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

	def getSubmissions(self, name, maxThreads = 10):
		print (name)
		self.r = praw.Reddit(user_agent='my_cool_app')
		self.submissions = ['']*maxThreads
		submission = r.get_subreddit(name).get_hot(limit = maxThreads)
		n = 0
		for i in submission:
			self.submissions[n] = i
			print    (str(n) + " "+i.title)
			self.text(str(n) + " "+i.title)
			n+=1
		self.url = ""
	def sendThreads(self, id):
		print(self.submissions[id].selftext.lower())
		self.text (self.submissions[id].selftext.lower())
		self.url = self.submissions[id].url
	def sendComments(self):
		s = self.r.get_submission(self.url)
		msg = ""
		for i in range(5):
			com = s.comments[i]
			msg += "~|" + com.body + "\n"
			for n in range (5):
				com1 = com.replies[n]
				msg += "~~|" + com1.body + "\n"
				
		sendMail(msg)

#s = r.get_submission(y)
#for x in range (10):
#for comment in s.comments:
#	comment = s.comments[x]
	#print("===============")
#	print(comment.author)
#	print("------------")
#	print(comment.body)
#	print("------------")
#	for cr in comment.replies:
#		print ("  " + cr.body)
#		for cr2 in cr.replies:
#			print ("    " + cr2.body)

ES = Comm()
ES.setup()

app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
	"""Respond to incoming texts"""
	#resp = twilio.twiml.Response()
	rq = ES.client.messages.list();
	print ("____MESSAGE____")
	msg = rq[0].body
	print(msg)
	#for x in range (0,5):
	#for message in rq:
	#	print (message.body)	
	#resp.message(rq[0].body)
	#resp.message(email)
	#return str(resp)

	if "open" in msg:
		ES.getSubmissions(msg[5:])
		#ES.sendThreads()
	elif "thread" in msg:
		ES.sendThreads(int(msg[7:]))
	elif "comments" in msg:
		if ES.url != "":
			ES.sendComments()

	#ES.text(rq[0].body)
	#send an email
	#ES.sendEmail(rq[0].body)
	#ES.sendMail(email)
	return "eof"
 
if __name__ == "__main__":
	app.run(debug=True)
