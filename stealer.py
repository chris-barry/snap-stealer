import urlparse
from Crypto.Cipher import AES

# List of domains associated with Snapchat.
domain = ['feelinsonice-hrd.appspot.com', 'data.flurry.com']
logFile = 'logs.txt'
AES_KEY = 'M02cnQ51Ji97vwT4'

def start(context, flow):
	with open(logFile,'a') as myfile:
		myfile.write('----- starting -----\n')
		
def response(context, flow):
	with open(logFile,'a') as myfile:
		# If the data is not from Snapchat, skip analysis.
		if not (flow.response.request.host in domain):
			return
		# TODO: Get fancy with responses.
		myfile.write('Response from Snapchat. OOOW\n')

def request(context, flow):
	with open(logFile, 'a') as myfile:
		# If the data is not from Snapchat, skip analysis.
		if not (flow.request.host in domain):
			return

		path = str(flow.request.path)
		url = str(flow.request.content)
		form = urlparse.parse_qs(url)

		# Every request seems to have these three attributes.
		username = str(form['username'][0])
		timestamp = str(form['timestamp'][0])
		request_token = str(form['req_token'][0])
		data = form['data'][0]

		# Start processing the request.
		if path == '/bq/upload':
			myfile.write(username)
			myfile.write(' is uploading an image\n')
			saveSnap(data)
			"""
			media_id:   YOURUSERNAME~6AABF95C-C466-417B-904D-ED4CC3
			type:       0 # I sent a picture, so I would imagine 0 is picture.
			username:   yourUserName
			zipped:     0
			data:
			"""

		if path == '/bq/send':
			myfile.write(username)
			myfile.write(' sent the image to ')
			myfile.write(str(form["recipient"]))
			myfile.write('\n')
			"""
			country_code:  US
			media_id:      YOURUSERNAME~6AABF95C-C466-417B-904D-ED4CC3B1C45D
			recipient:     whoYouSentItTo
			time:          6
			type:          0
			zipped:        0
			"""

		if path == '/bq/clear':
			myfile.write(username)
			myfile.write(' cleared their feed.\n')

		if path == '/bq/set_num_best_friends':
			myfile.write(username)
			myfile.write(' changed their number of best friends to ')
			myfile.write(str(form['num_best_friends'][0]))
			myfile.write('.\n')
			"""
			num_best_friends:  5
			"""

		# I don't know the difference between updates and all_updates.
		if path == '/bq/updates' or path == '/bq/all_updates':
			myfile.write(username)
			myfile.write(' is updating.\n')
			"""
			"""

		if path == '/bq/stories':
			myfile.write(username)
			myfile.write(' is updating their stories.\n')
			"""
			"""

		if path == '/bq/bests':
			myfile.write(username)
			myfile.write(' is updating their stories.\n')
			"""
			friend_usernames:  ["yourUserName","friend1","friend2","friend3",...]
			"""

		if path == '/bq/blob':
			myfile.write(username)
			myfile.write(' is blobing.\n')
			"""
			id:         513637398565409770r
			"""

def decrypt(data):
	# using AES_KEY and ECB to decrypt
	c = AES.new(AES_KEY, AES.MODE_ECB)
	# pkcs5 is used to pad the data
	padCount = 16 - len(data) % 16
	# actually decrypt data with pad and key
	return c.decrypt(data + (chr(padCount) * padCount).encode('utf-8'))

def saveSnap(data):
	outFile = open("./saved_images/testing.jpg", "w")
	outFile.write(decrypt(data))
	outfile.close()


def end(context, flow):
	with open(logFile,'a') as myfile:
		myfile.write('----- ending -----\n')

