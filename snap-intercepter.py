import urlparse
from Crypto.Cipher import AES

# Globals
LOG_FILE = 'logs.txt'
snapchat_aes_key = 'M02cnQ51Ji97vwT4'
DOMAINS = ['feelinsonice-hrd.appspot.com', 'data.flurry.com']

def start(context, flow):
	myfile = open(LOG_FILE, 'a')
	try:
		myfile.write('----- starting interception -----\n')
	finally:
		myfile.close()

def response(context, flow):
	if not (flow.response.request.host in DOMAINS):
		return

	myfile = open(LOG_FILE, 'a')

	try:
		# If the data is not from Snapchat, skip analysis.
		# TODO: Get fancy with responses.
		myfile.write('Response from Snapchat. OOOW\n')
	finally:
		myfile.close()

def request(context, flow):
	if not (flow.request.host in DOMAINS):
		return

	myfile = open(LOG_FILE, 'a')

	try:
		# If the data is not from Snapchat, skip analysis.

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
	finally:
		myfile.close()

def end(context, flow):
	myfile = open(LOG_FILE, 'a')
	try:
		myfile.write('----- ending interception -----\n')
	finally:
		myfile.close()

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


