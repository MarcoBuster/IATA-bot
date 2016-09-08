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

    if query == "submit":
        text = (
            "✍<b>Ciao</b> {0}, invia il <b>nome</b> del <b>gruppo</b> o <b>canale</b> che vuoi proporre a <b>IATA</b>".format(sender.name)
        )

        bot.api.call("editMessageText", {
            "chat_id":chat.id, "message_id": message.message_id, "text": text, "parse_mode":"HTML", "reply_markup":
            '{"inline_keyboard": [[{"text":"❌Annulla", "callback_data":"cancel"}]]}'
        }
        )
        API.db.updateState(chat.id, "submit1", 0)
        conn.commit()
