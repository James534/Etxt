import requests 

r = requests.post(
    "https://api.mailgun.net/v3/sandbox494f73c04c764e64854bcde56398b12c.mailgun.org/messages",
    auth=("api", "key-8307326d9c7d3f36604ad45905f7f4b4"),
    data={"from": "Excited User <mailgun@sandbox494f73c04c764e64854bcde56398b12c.mailgun.org>",
        "to": ["bar@example.com", "sadmansazidk@gmail.com"],
        "subject": "Hello",
        "text": "Testing some Mailgun awesomness!"})
print (r.text)
