# -*- coding: utf-8 -*-

"""
    TelegramBot
    ~~~~~~~~~~~~~~~~~~
    Mini-Framework for sending messages through Telegram
    :copyright: © 2018 Andreas Brett
    :license: GNU General Public License v3.0, see LICENSE for more details
"""

import urllib, urllib2, json

class tgb:


	# ==========================================================================================================
	#  URIs for different API requests
	# ==========================================================================================================
	uriGetUpdates = "https://api.telegram.org/bot%TOKEN%/getUpdates"
	uriSendMessage = "https://api.telegram.org/bot%TOKEN%/sendMessage"
	uriDeleteMessage = "https://api.telegram.org/bot%TOKEN%/deleteMessage"



	# ==========================================================================================================
	#  CONSTRUCTOR
	# ==========================================================================================================
	def __init__(self, access_token, chat_id = None):
		self.access_token = access_token
		if chat_id:
			self.chat_id = chat_id



	def _jprint(self, oJson):
		print json.dumps(oJson, indent=4, sort_keys=True)



	def _makeApiRequest(self, apiUri, queryParams = None):
		apiUri = apiUri.replace("%TOKEN%", self.access_token)

		# build request if queryParams are present
		if queryParams:
			apiUri = apiUri + "?%s" % urllib.urlencode(queryParams)

		try:
			# fetch response
			request = urllib2.Request(apiUri)
			response = urllib2.urlopen(request).read()

			# return json data
			return json.loads(response.decode("utf-8"))

		except urllib2.HTTPError as e:
			print "Could not make API request. %r" % e
			return None
		
		except urllib2.URLError as e:
			print "Could not make API request. %r" % e
			return None



	# -----------------------------------------------------------------------------------
	# setProxy
	# -----------------------------------------------------------------------------------
	#	* DESCRIPTION	define proxy to use
	#	* RETURNS		None
	# -----------------------------------------------------------------------------------
	#	* <string> proxyAddress = address of your proxy for https connections
	# -----------------------------------------------------------------------------------
	def setProxy(self, proxyAddress):
		proxyHandler = urllib2.ProxyHandler({"https": proxyAddress})
		proxyOpener = urllib2.build_opener(proxyHandler)
		urllib2.install_opener(proxyOpener)



	# -----------------------------------------------------------------------------------
	# getUpdates
	# -----------------------------------------------------------------------------------
	#	* DESCRIPTION	retrieves history of all chats / groups in the last 24h
	#	* RETURNS		None
	# -----------------------------------------------------------------------------------
	#	* <string[]> queryParams = parameters to filter updates (see Telegram Bot API)
	# -----------------------------------------------------------------------------------
	def getUpdates(self, queryParams = None):
		# retrieve latest messages
		result = self._makeApiRequest(self.uriGetUpdates, queryParams)
		self._jprint(result)



	# -----------------------------------------------------------------------------------
	# deleteMessage
	# -----------------------------------------------------------------------------------
	#	* DESCRIPTION	deletes a message from a given chat
	#	* RETURNS		True / False
	# -----------------------------------------------------------------------------------
	#	* <int> message_id = message you want to delete
	#	* <int> chat_id = ID of the chat / group you want to delete message from
	# -----------------------------------------------------------------------------------
	def deleteMessage(self, message_id, chat_id = None):
                # delete a message in a chat room (retrieve chat room ID via "getUpdates")
                if chat_id:
                        result = self._makeApiRequest(self.uriDeleteMessage, {"chat_id": chat_id, "message_id": message_id})
                else:
                        result = self._makeApiRequest(self.uriDeleteMessage, {"chat_id": self.chat_id, "message_id": message_id})

                if result is None:
                        return False
                elif result["ok"]:
                        return True
                else:
                        return False



	# -----------------------------------------------------------------------------------
	# sendMessage
	# -----------------------------------------------------------------------------------
	#	* DESCRIPTION	sends a message to a given chat
	#	* RETURNS		message ID
	# -----------------------------------------------------------------------------------
	#	* <string> message = message you want to send
	#	* <int> chat_id = ID of the chat / group you want to send message to
	# -----------------------------------------------------------------------------------
	def sendMessage(self, message, chat_id = None):
			# send a message to a chat room (retrieve chat room ID via "getUpdates")
			if chat_id:
					result = self._makeApiRequest(self.uriSendMessage, {"chat_id": chat_id, "text": message})
			else:
					result = self._makeApiRequest(self.uriSendMessage, {"chat_id": self.chat_id, "text": message})

			if result is None:
					return None
			elif result["ok"]:
					return result["result"]["message_id"]
			else:
					return None
