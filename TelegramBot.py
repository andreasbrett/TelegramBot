# -*- coding: utf-8 -*-

"""
    TelegramBot
    ~~~~~~~~~~~~~~~~~~
    Mini-Framework for sending messages through Telegram
    :copyright: © 2018 Andreas Brett
    :license: GNU General Public License v3.0, see LICENSE for more details
"""

import urllib, urllib2, json, datetime, pickle, os

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



	def _storeMessageId(self, message_id, message_store_path):
		# load message store
		dict = self._loadMessageStore(message_store_path)

		# add message with timestamp to dictionary
		dict.update({message_id: datetime.datetime.now()})

		# save message store
		self._saveMessageStore(dict, message_store_path)



	def _removeMessageId(self, message_id, message_store_path):
		# load message store
		dict = self._loadMessageStore(message_store_path)
		
		# remove message_id
		if message_id in dict:
			del dict[message_id]

		# save message store
		self._saveMessageStore(dict, message_store_path)



	def _loadMessageStore(self, message_store_path):		
		if os.path.isfile(message_store_path):
			f = open(message_store_path, "rb")
			dict = pickle.load(f)
			f.close()
		else:
			dict = {}

		return dict



	def _saveMessageStore(self, dict, message_store_path):
		f = open(message_store_path, "wb")
		pickle.dump(dict, f)
		f.close()



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
	# cleanupMessages
	# -----------------------------------------------------------------------------------
	#	* DESCRIPTION	cleans up messages in a chat
	#	* RETURNS		number of deleted messages
	# -----------------------------------------------------------------------------------
	#	* <int> age_in_days = message age in days
	#	* <string> message_store_path = path to the message store
	#	* <int> chat_id = ID of the chat / group you want to delete message from
	# -----------------------------------------------------------------------------------
	def cleanupMessages(self, age_in_days, message_store_path, chat_id = None):
		num_deleted_messages = 0

		if os.path.isfile(message_store_path):
			# load message store
			dict = self._loadMessageStore(message_store_path)

			# initiate datetime objects
			now = datetime.datetime.now()
			minDelta = datetime.timedelta(age_in_days, 0)

			# iterate over messages
			for message_id, timestamp in dict.iteritems():
				if delta > minDelta:
					# delete message from chat
					self.deleteMessage(message_id, chat_id)

					# delete message from storage
					del dict[message_id]

					# count deleted messages
					num_deleted_messages += 1

			# save message store
			self._saveMessageStore(dict, message_store_path)

		return num_deleted_messages



	# -----------------------------------------------------------------------------------
	# sendMessage
	# -----------------------------------------------------------------------------------
	#	* DESCRIPTION	sends a message to a given chat
	#	* RETURNS		message ID
	# -----------------------------------------------------------------------------------
	#	* <string> message = message you want to send
	#	* <int> chat_id = ID of the chat / group you want to send message to
	#	* <string> message_store_path = path to message store
	# -----------------------------------------------------------------------------------
	def sendMessage(self, message, chat_id = None, message_store_path = None):
			# send a message to a chat room (retrieve chat room ID via "getUpdates")
			if chat_id:
					result = self._makeApiRequest(self.uriSendMessage, {"chat_id": chat_id, "text": message})
			else:
					result = self._makeApiRequest(self.uriSendMessage, {"chat_id": self.chat_id, "text": message})

			if result is None:
					return None
			elif result["ok"]:
					message_id = result["result"]["message_id"]
					# store message_id in message store
					if message_store_path:
						self._storeMessageId(message_id, message_store_path)
					
					# return message_id
					return message_id
			else:
					return None
