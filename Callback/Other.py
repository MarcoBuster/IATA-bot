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
            '[{"text":"📞Contatta IATA", "callback_data":"contact"}],'
            '[{"text":"ℹ️Link utili", "callback_data":"links"}]'+
        ']}'
    })
        API.db.updateState(chat.id, "home", 0)

    if query == "links":
        text = "Ecco dei <b>link utili</b> di <b>IATA</b>"
        bot.api.call("editMessageText",{
            "chat_id":chat.id, "message_id":message.message_id, "text":text, "parse_mode":"HTML", "reply_markup":
                '{"inline_keyboard":[[{"text":"📢Canale ufficiale", "url":"telegram.me/IATAlliance"},{"text":"☕️Bar", "url":"telegram.me/IATABar"}],'+
                '[{"text":"🚫Blacklist", "url":"telegram.me/IATABlacklist"}, {"text":"🌐Sito web", "url":"https://www.iata.ovh"}],'
                '[{"text":"🔙Torna indietro", "callback_data":"cancel"}]'
            ']}'
    })

    if query == "bans":
        c.execute('''SELECT * FROM ban''')
        rows = c.fetchall()

        initial = "<b>Ecco la lista degli utenti bannati dal bot, con motivazione:</b>"
        row = "\n"

        for res in rows:
            user_id = str(res[0])
            motivazione = res[1]
            row = row + "🆔<b>ID: {0}</b>, ✍️per {1}\n".format(user_id, motivazione)

        if row == "\n":
            row = "\n<i>Nessun utente bannato</i>"

        bot.api.call("editMessageText",{
            "chat_id":chat.id, "message_id":message.message_id, "text":(initial + row), "parse_mode":"HTML", "reply_markup":
            '{"inline_keyboard":[[{"text":"🔙Torna all\'admin panel", "callback_data":"admin"}]]}'
    })

    if query == "adminhelp":
        text = (
            "<b>ADMIN GUIDE</b>"
            "\n\n<b>Bannare e sbannare un utente</b>"
            "\nPer <b>bannare</b> un utente, basta utilizzare il comando <code>/ban</code>"
            "\nPer <b>sbannare</b> un utente, invece, bisogna utilizzare il comando <code>/unban</code>"
            "\nLa <b>sintassi</b> è: <code>/ban USER_ID MOTIVAZIONE</code>, <code>/unban USER_ID MOTIVAZIONE</code>"
            "\nAttenzione! La motivazione sarà <b>sempre</b> <b>inviata</b> all\' utente bannato e <b>salvata</b> nel database, quindi accessibile a tutti gli <b>admins</b>"
            "\n\n<b>Rispondere a un messaggio</b>"
            "\nPer <b>rispondere</b> a un messaggio inviato da un utente, bisogna utilizzare il comando <code>/r</code>"
            "\nEsempio: <code>/r USER_ID Per avere altre informazioni su IATA vai sul sito www.iata.ovh</code>"
            "\nLa risposta <b>supporta il Markdown</b>"
            "\n\n<b>Codice sorgente</b>"
            "\nIl codice sorgente è disponibile nella REPO di IATA-dev: <a href=\"www.GitHub.com/IATA-dev/IATA-bot\">Link alla repo</a>"
            "\n\n<b>Sviluppatore e altro</b>"
            "\nIl bot è stato sviluppato da @MarcoBuster, è scritto in <b>Python 3.5</b> ed utilizza il framework <b>botogram (modificato)</b>"
        )
        bot.api.call("editMessageText",{
            "chat_id":chat.id, "message_id":message.message_id, "text":text, "parse_mode":"HTML", "reply_markup":
            '{"inline_keyboard":[[{"text":"🔙Torna all\'admin panel", "callback_data":"admin"}]]}'
    })

    if query == "wakeup":
        text = (
            "@MarcoBuster! <b>Un admin IATA</b> ({0}, @{1}, #id{2}) <b>ti sta cercando per un problema con il bot!</b>".format(sender.name, str(sender.username), str(sender.id))
        )

        bot.chat(26170256).send(text)
        bot.chat(chat.id).send("<b>Lo sviluppatore risponderà il prima possibile!</b>")

    if query == "admin":
        text = (
            "<b>Benvenuto nel pannello admin del bot</b>"
        )
        bot.api.call("editMessageText", {
            "chat_id":chat.id, "message_id":message.message_id, "text":text, "parse_mode":"HTML", "reply_markup":
                '{"inline_keyboard":[[{"text":"❓Aiuto admins", "callback_data":"adminhelp"}],'+
                '[{"text":"🔨Bannati", "callback_data":"bans"}, {"text":"⏰Chiama il dev", "callback_data":"wakeup"}]'+
            ']}'
    })
