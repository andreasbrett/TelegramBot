# -*- coding: utf-8 -*-

import TelegramBot

# create TelegramBot object
tgb_init = TelegramBot.tgb("ENTER-YOUR-ACCESS-TOKEN")

# print latest updates (= all messages sent to it) to find out chat IDs
tgb_init.getUpdates()

# create TelegramBot object
tgb = TelegramBot.tgb("ENTER-YOUR-ACCESS-TOKEN", "ENTER-YOUR-GLOBAL-CHAT-ID-HERE")

# send message to (globally defined) chat
tgb.sendMessage("Hey there!\nI'm your new bot.")

# send message to specific chat
tgb.sendMessage("Hey there!\nI'm your new bot.", "ENTER-YOUR-CHAT-ID-HERE")
