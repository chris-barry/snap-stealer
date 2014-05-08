import urlparse
from Crypto.Cipher import AES

# Globals
LOG_FILE = 'logs.txt'
snapchat_aes_key = 'M02cnQ51Ji97vwT4'
DOMAINS = ['feelinsonice-hrd.appspot.com', 'data.flurry.com']

def start(context, flow):
	with open(LOG_FILE,'a') as myfile:
		myfile.write('----- starting interception -----\n')

def response(context, flow):
	with open(LOG_FILE,'a') as myfile:
		# If the data is not from Snapchat, skip analysis.
		if not (flow.response.request.host in domain):
			return
		# TODO: Get fancy with responses.
		myfile.write('Response from Snapchat. OOOW\n')

def request(context, flow):
	with open(LOG_FILE, 'a') as myfile:
		# If the data is not from Snapchat, skip analysis.
		if not (flow.request.host in DOMAINS):
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
			# TODO: Decrypt.
			#myfile.write(username)
			#myfile.write(' is uploading an image\n')
			saveSnap(data, str(form['media_ia'][0]))
			"""
			media_id:   YOURUSERNAME~6AABF95C-C466-417B-904D-ED4CC3
			type:       0 # I sent a picture, so I would imagine 0 is picture.
			username:   yourUserName
			zipped:     0
			data:
			"""

		if path == '/bq/blob':
			# TODO: Decrypt.
			myfile.write(username)
			myfile.write(' is blobing.\n')
			"""
			id:         513637398565409770r
			"""

def end(context, flow):
	with open(LOG_FILE,'a') as myfile:
		myfile.write('----- ending interception -----\n')

def decrypt(data):
	# using AES_KEY and ECB to decrypt
	c = AES.new(AES_KEY, AES.MODE_ECB)
	# pkcs5 is used to pad the data
	padCount = 16 - len(data) % 16
	# actually decrypt data with pad and key
	return c.decrypt(data + (chr(padCount) * padCount).encode('utf-8'))

def saveSnap(data, path):
	outFile = open("./saved_images/" + path, "w")
	outFile.write(decrypt(data))
	outfile.close()


