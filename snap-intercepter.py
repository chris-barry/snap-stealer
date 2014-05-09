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
	return

def response(context, flow):
	# If the data is not from Snapchat, skip analysis.
	if not (flow.response.request.host in DOMAINS):
		return

	# opens log file
	myfile = open(LOG_FILE, 'a')

	try:
		path = str(flow.request.path)

		# received snaps
		if path == '/bq/blob':
			content = str(flow.response.request.content)
			form = urlparse.parse_qs(content)

			# lets get our picId to have a filename
			picId = str(form['id'][0])

			# actual encrypted blob
			blob = str(flow.response.content)

			# saves and decrypts snap to a given pictId
			saveSnap(blob, picId)
	finally:
		myfile.close()

def request(context, flow):
	# If the data is not from Snapchat, skip analysis.
	if not (flow.request.host in DOMAINS):
		return

	myfile = open(LOG_FILE, 'a')

	try:
		path = str(flow.request.path)
		form = str(flow.request.content)

		# Start processing the request.
		if path == '/bq/upload':
			# Handling multipart form is a pain
			# trimming down to encrypted blob
			mediaIdString = 'Content-Disposition: form-data; name="media_id"'
			tmp = form.find(mediaIdString)
			mediaId = form[(tmp + len(mediaIdString)):]

			# more trimming down to encrypted blob
			mediaIdStringAfter = 'Content-Disposition: form-data; name="req_token"'
			tmp = mediaId.find(mediaIdStringAfter)
			mediaId = mediaId[:(tmp - len('--Boundary+XXXXXXXXXXXXXXXXX') - 2)].strip()

			# more trimming!
			dataString = 'Content-Type: application/octet-stream'
			test = form.find(dataString)
			data = form[(test + len(dataString)):]

			# and even more trimming
			extras = '--Boundary'
			loc = data.find(extras)
			tmp = data[:loc]
			data = tmp
			data = data.strip()
			
			# saves and decrypts snap
			saveSnap(data, mediaId)
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
	c = AES.new(snapchat_aes_key, AES.MODE_ECB)
	# pkcs5 is used to pad the data
	padCount = 16 - len(data) % 16
	# actually decrypt data with pad and key
	decryptedData = c.decrypt(data + (chr(padCount) * padCount).encode('utf-8'))
	return decryptedData

# saves a given snapchat
def saveSnap(data, path):
	decryptedData = decrypt(data)

	# checks if .jpg
	if (decryptedData[:4] == '\xFF\xD8\xFF\xE0'):
		outFile = open("./saved_media/" + path + ".jpg", "w")
	# checks if .mp4
	elif (decryptedData[:2] == '\x00\x00'):
		outFile = open("./saved_media/" + path + ".mp4", "w")

	outFile.write(decrypt(data))
	outfile.close()
