import Bot, API

import botogram

import sqlite3
conn = sqlite3.connect('IATA-bot.db')
c = conn.cursor()

def process(bot, chains, update):
    message = update.callback_query.message
    chat = message.chat
    query = update.callback_query.data
    callback_id = update.callback_query.id
    sender = update.callback_query.sender

    if query == "contact":
        text = (
            "Digita il <b>messaggio</b> che vuoi inviare a <b>IATA</b>"
            "\nChiunque invierà messaggi di <b>spam</b> o <b>intimidatori</b> sarà <b>bannato permanentemente</b> dal bot"
        )

        bot.api.call("editMessageText", {
            "chat_id":chat.id, "message_id": message.message_id, "text": text, "parse_mode":"HTML", "reply_markup":
            '{"inline_keyboard": [[{"text":"❌Annulla", "callback_data":"cancel"}]]}'
        }
        )

        API.db.updateState(chat.id, "contact1", 0)
