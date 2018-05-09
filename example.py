# -*- coding: utf-8 -*-

import TelegramBot

# create TelegramBot object
tgb_init = TelegramBot.tgb("ENTER-YOUR-ACCESS-TOKEN")

# print latest updates (= all messages sent to it) to find out chat IDs
tgb_init.getUpdates()

# create TelegramBot object
tgb = TelegramBot.tgb("ENTER-YOUR-ACCESS-TOKEN", "ENTER-YOUR-GLOBAL-CHAT-ID-HERE")

# if you're behind a proxy => set it
tgb.setProxy("http://THIS-IS-MY-PROXY-ADDRESS:THIS-IS-MY-PROXY-PORT")

# send message to (globally defined) chat
message_id = tgb.sendMessage("Hey there!\nI'm your new bot.")

# send message to (globally defined) chat and store message_id in message store
message_id = tgb.sendMessage("Hey there!\nI'm your new bot.", None, "ENTER-YOUR-MESSAGE-STORE.db")

# send message to specific chat
message_id = tgb.sendMessage("Hey there!\nI'm your new bot.", "ENTER-YOUR-CHAT-ID-HERE")

# delete message from (globally defined) chat
tgb.deleteMessage(message_id)

# delete message from specific chat
tgb.deleteMessage(message_id, "ENTER-YOUR-CHAT-ID-HERE")

# clean up old messages (> 7 days) from (globally defined) chat
tgb.cleanupMessages(7, "ENTER-YOUR-MESSAGE-STORE.db")
