'''
IATA TELEGRAM BOT (www.telegram.me/IATA_bot)
=====================
EN: With this bot you can report a user for IATA Blacklist
IT: Con questo bot puoi segnalare un utente da mettere nella IATA Blacklist

EN: You can else submit your supergroup for join in IATA Alliance
IT: Puoi anche sottoscrivere il tuo supergruppo per farlo entrare in IATA Alliance

EN: Bot developed by @MarcoBuster (www.GitHub.com/MarcoBuster)
IT: Bot sviluppato da @MarcoBuster (www.GitHub.com/MarcoBuster)
=====================
'''

from Callback import Report, Submit, Other
import API

import botogram.objects.base
class CallbackQuery(botogram.objects.base.BaseObject):
    required = {
        "id": str,
        "from": botogram.User,
        "data": str,
    }
    optional = {
        "inline_message_id": str,
        "message": botogram.Message,
    }
    replace_keys = {
        "from": "sender"
    }
botogram.Update.optional["callback_query"] = CallbackQuery

import botogram
bot = botogram.create("TOKEN")

import sqlite3
conn = sqlite3.connect('IATA-bot.db')
c = conn.cursor()
API.db.createTables()
conn.commit()

@bot.command("start")
def start(chat, message, args):
    '''Hello, world!'''
    text = (
            "Benvenuto nel <b>bot ufficiale</b> di <b>IATA</b>!\n"
            "<b>Cosa vuoi fare?</b>"
        )
    bot.api.call("sendMessage",{
        "chat_id":chat.id, "text":text, "parse_mode":"HTML", "reply_markup":
            '{"inline_keyboard":[[{"text":"🔒Segnala utente", "callback_data":"report"}, {"text":"📝Sottoscrivi gruppo", "callback_data":"submit"}],'+
            '[{"text":"ℹ️Link utili", "callback_data":"links"}]'+
        ']}'
    })

    API.db.updateState(chat.id, "home", 0)
    conn.commit()

def process_callback(bot, chains, update):
    '''Process callback'''
    Report.process(bot, chains, update)
    Submit.process(bot, chains, update)
    Other.process(bot, chains, update)
bot.register_update_processor("callback_query", process_callback)

@bot.process_message
def report1(chat, message):
    '''Report a user'''
    state, temp = API.db.getState(chat.id)
    conn.commit()
    if state != "report1":
        return

    if message.text == None:
        message.reply("<b>Attenzione!</b>\nIl messaggio inviato <b>non contiene testo</b>, per favore inviare l\'ID dell'utente o il suo username.")
        return

    reported_info = str(message.text)

    conn.commit()
    c.execute('''DELETE FROM report WHERE chat_id=?''',(chat.id,))
    c.execute('''INSERT INTO report VALUES(?,?,?)''',(chat.id, "None", "None",))
    c.execute('''UPDATE report SET reported_info=? WHERE chat_id=?''',(reported_info, chat.id,))
    conn.commit()

    text = (
        "✍Ora invia una <b>prova valida</b> per la tua segnalazione. Può essere un semplice screen o, se preferisci, un messaggio testuale"
    )

    bot.api.call("sendMessage", {
        "chat_id":chat.id, "text": text, "parse_mode":"HTML", "reply_markup":
            '{"inline_keyboard": [[{"text":"❌Annulla", "callback_data":"cancel"}]]}'
    }
    )

    API.db.updateState(chat.id, "report2", 0)
    conn.commit()

@bot.process_message
def report2(chat, message):
    '''Report a user'''
    state, temp = API.db.getState(chat.id)
    conn.commit()
    if state != "report2":
        return

    if state == "report2" and temp == 0:
        API.db.updateState(chat.id, "report2", 1)
        conn.commit()
        return

    if message.text == None and message.photo == None:
        message.reply("<b>Attenzione!</b>\nIl messaggio inviato <b>non contiene testo e non è un\'immagine</b>, per favore inviare l\'ID dell'utente o il suo username.", format="HTML")
        return

    c.execute('''SELECT * FROM report WHERE chat_id=?''',(chat.id,))
    rows = c.fetchall()

    for res in rows:
        reported_info = res[1]

    if message.photo == None:
        reported_evidence = message.text
        bot.chat(26170256).send(
                                "<b>NUOVA SEGNALAZIONE</b> (#report)\n"
                                "<b>Info sul reportato</b>: {0}\n"
                                "<b>Prove</b>: {1}\n"
                                "<b>SEGNALATO DA</b>:\n"
                                "<b>Nome</b>: {2}\n"
                                "<b>Username</b>: @{3}\n"
                                "<b>ID</b>: #da{4}".format(reported_info, reported_evidence, message.sender.name, str(message.sender.username), str(message.sender.id))
                        )
        API.db.updateState(chat.id, "nullstate", 0)

    else:
        file_id = message.photo.file_id
        caption = (
                    "Info sul reportato: {0}\n"
                    "Segnalato da: {1} (@{2}, #da{3})"
                    .format(str(reported_info), str(message.sender.name), str(message.sender.username), str(message.sender.id))
                )

        bot.api.call("sendPhoto", {
        "chat_id": 26170256, "photo":file_id, "caption":caption
        }
        )
        API.db.updateState(chat.id, "nullstate", 0)

    message.reply("👍<b>Grazie!</b>\nLa tua segnalazione è stata <b>inviata</b>, un team di <b>moderatori</b> la analizzerà presto")

if __name__ == "__main__":
    bot.run()
