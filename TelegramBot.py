# -*- coding: utf-8 -*-

import urllib, urllib2, json

class tgb:


	# ==========================================================================================================
	#  URIs for different API requests
	# ==========================================================================================================
	uriGetUpdates = "https://api.telegram.org/bot%ID%/getUpdates"
	uriSendMessage = "https://api.telegram.org/bot%ID%/sendMessage"



	# ==========================================================================================================
	#  CONSTRUCTOR
	# ==========================================================================================================
	def __init__(self, access_token, chat_id = None):
		self.access_token = access_token
		if chat_id:
			self.chat_id = chat_id



	def jprint(self, oJson):
		print json.dumps(oJson, indent=4, sort_keys=True)



	def makeApiRequest(self, apiUri, queryParams = None):
		apiUri = apiUri.replace("%ID%", self.access_token)

		# build request if queryParams are present
		if queryParams:
			apiUri = apiUri + "?%s" % urllib.urlencode(queryParams)

		try:
			# fetch response
			request = urllib2.Request(apiUri)
			response = urllib2.urlopen(request).read()

			# return json data
			return json.loads(response.decode("utf-8"))

		except urllib2.URLError as e:
			return None



	def getUpdates(self, queryParams = None):
		# retrieve latest messages
		result = self.makeApiRequest(self.uriGetUpdates, queryParams)
		self.jprint(result)



	def sendMessage(self, message, chat_id = None):
		# send a message to a chat room (retrieve chat room ID via "getUpdates")
		if chat_id:
			result = self.makeApiRequest(self.uriSendMessage, {"chat_id": chat_id, "text": message})
		else:
			result = self.makeApiRequest(self.uriSendMessage, {"chat_id": self.chat_id, "text": message})

		if result is None:
			return False
		elif result["ok"]:
			return True
		else:
			return False
