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

    if query == "cancel":
        args = None
        c.execute('''DELETE FROM report WHERE chat_id=?''',(chat.id,))
        c.execute('''DELETE FROM submit WHERE chat_id=?''',(chat.id,))
        conn.commit()
        text = (
                "Benvenuto nel <b>bot ufficiale</b> di <b>IATA</b>!\n"
                "<b>Cosa vuoi fare?</b>"
            )
        bot.api.call("editMessageText",{
            "chat_id":chat.id, "message_id":message.message_id, "text":text, "parse_mode":"HTML", "reply_markup":
                '{"inline_keyboard":[[{"text":"🔒Segnala utente", "callback_data":"report"}, {"text":"📝Sottoscrivi gruppo", "callback_data":"submit"}],'+
                '[{"text":"ℹ️Link utili", "callback_data":"links"}]'+
            ']}'
        })
        API.db.updateState(chat.id, "home", 0)

    if query == "links":
        text = "Ecco dei <b>link utili</b> di <b>IATA</b>"
        bot.api.call("editMessageText",{
            "chat_id":chat.id, "message_id":message.message_id, "text":text, "parse_mode":"HTML", "reply_markup":
                '{"inline_keyboard":[[{"text":"📢Canale ufficiale", "url":"https://www.telegram.me/IATAlliance"},{"text":"☕️Bar", "url":"https://www.telegram.me/IATABar"}],'+
                '[{"text":"🚫Blacklist", "url":"https://www.telegram.me/IATABlacklist"}, {"text":"🌐Sito web", "url":"https://www.iata.ovh"}],'
                '[{"text":"🔙Torna indietro", "callback_data":"cancel"}]'
            ']}'
        }
        )
