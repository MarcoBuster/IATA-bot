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

from Callback import Report, Submit, Other, Contact
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

@bot.before_processing
def ban_system(chat, message):
    c.execute('''SELECT * FROM ban WHERE user_id=?''',(message.sender.id,))
    found = c.fetchall()
    conn.commit()
    if found:
        message.reply("<b>ATTENZIONE! Sei bannato dall\'utilizzo di questo bot!</b>")
        return True
    if not found:
        return False

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
            '[{"text":"📞Contatta IATA", "callback_data":"contact"}],'
            '[{"text":"ℹ️Link utili", "callback_data":"links"}]'+
        ']}'
    })

    API.db.updateState(chat.id, "home", 0)
    conn.commit()

@bot.command("help")
def help(chat, message, args):
    '''Need help? Nope!'''
    chat.send("Ti sto rindirizzando al comando */start*...")
    start(chat, message, args)

def process_callback(bot, chains, update):
    '''Process callback'''
    Report.process(bot, chains, update)
    Submit.process(bot, chains, update)
    Contact.process(bot, chains, update)
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
                                "#REPORT<b> UTENTE</b>\n"
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

    text = "👍<b>Grazie!</b>\nLa tua segnalazione è stata <b>inviata</b>, un team di <b>moderatori</b> la analizzerà presto\n<b>Cosa vuoi fare ora?</b>"
    bot.api.call("sendMessage", {
        "chat_id":chat.id, "text": text, "parse_mode":"HTML", "reply_markup":
            '{"inline_keyboard":[[{"text":"🔐Segnala un altro utente", "callback_data":"report"}],[{"text":"🔙Torna al menù principale", "callback_data":"cancel"}]]}'
    }
    )

@bot.process_message
def submit1(chat, message):
    '''Submit your supergroup - Which is the name?'''
    state, temp = API.db.getState(chat.id)
    conn.commit()
    if state != "submit1":
        return

    if message.text == None:
        message.reply("<b>Attenzione!</b>\nIl messaggio inviato <b>non contiene testo</b>, per favore invia il <b>nome</b> del <b>gruppo</b> che vuoi fare entrare in <b>IATA</b>")
        return

    group_name = str(message.text)

    c.execute('''DELETE FROM submit WHERE chat_id=?''',(chat.id,))
    c.execute('''INSERT INTO submit VALUES(?,?,?,?,?)''',(chat.id, "None", "None", "None", "None"))
    c.execute('''UPDATE submit SET name=? WHERE chat_id=?''',(group_name, chat.id,))
    conn.commit()

    text = (
        "✍Ora invia il <b>link d\'invito</b> del gruppo"
    )

    bot.api.call("sendMessage", {
        "chat_id":chat.id, "text": text, "parse_mode":"HTML", "reply_markup":
            '{"inline_keyboard": [[{"text":"❌Annulla", "callback_data":"cancel"}]]}'
    }
    )

    API.db.updateState(chat.id, "submit2", 0)
    conn.commit()

@bot.process_message
def submit2(chat, message):
    '''Submit your supergroup - Which is the link?'''
    state, temp = API.db.getState(chat.id)
    conn.commit()
    if state != "submit2":
        return

    if state == "submit2" and temp == 0:
        API.db.updateState(chat.id, "submit2", 1)
        conn.commit()
        return

    if message.text == None and message.photo == None:
        message.reply("<b>Attenzione!</b>\nIl messaggio inviato <b>non contiene testo</b>, per favore invia il <b>link</b> del <b>gruppo</b> che vuoi fare entrare in <b>IATA</b>")
        return

    link = message.text
    c.execute('''UPDATE submit SET link=? WHERE chat_id=?''',(link, chat.id,))
    conn.commit()

    text = (
        "<b>Stai andando bene!</b>\n"
        "✍Ora invia la <b>lista completa</b> degli amministratori, <b>in un unico messaggio</b>"
    )

    bot.api.call("sendMessage", {
        "chat_id":chat.id, "text": text, "parse_mode":"HTML", "reply_markup":
            '{"inline_keyboard": [[{"text":"❌Annulla", "callback_data":"cancel"}]]}'
    }
    )

    API.db.updateState(chat.id, "submit3", 0)
    conn.commit()

@bot.process_message
def submit3(chat, message):
    '''Submit your supergroup - Admins?'''
    state, temp = API.db.getState(chat.id)
    conn.commit()
    if state != "submit3":
        return

    if state == "submit3" and temp == 0:
        API.db.updateState(chat.id, "submit3", 1)
        conn.commit()
        return

    if message.text == None and message.photo == None:
        message.reply("<b>Attenzione!</b>\nIl messaggio inviato <b>non contiene testo</b>, per favore invia la <b>lista completa</b> degli admins del <b>gruppo</b> che vuoi fare entrare in <b>IATA</b>")
        return

    admins = message.text
    c.execute('''UPDATE submit SET admins=? WHERE chat_id=?''',(admins, chat.id,))
    conn.commit()

    text = (
        "<b>Ultimo passaggio</b>!\n"
        "✍Ora invia <b>una descrizione</b> del gruppo che vuoi far entrare in <b>IATA</b>"
    )

    bot.api.call("sendMessage", {
        "chat_id":chat.id, "text": text, "parse_mode":"HTML", "reply_markup":
            '{"inline_keyboard": [[{"text":"❌Annulla", "callback_data":"cancel"}]]}'
    }
    )

    API.db.updateState(chat.id, "submit4", 0)
    conn.commit()

@bot.process_message
def submit4(chat, message):
    '''Submit your supergroup - Admins?'''
    state, temp = API.db.getState(chat.id)
    conn.commit()
    if state != "submit4":
        return

    if state == "submit4" and temp == 0:
        API.db.updateState(chat.id, "submit4", 1)
        conn.commit()
        return

    if message.text == None and message.photo == None:
        message.reply("<b>Attenzione!</b>\nIl messaggio inviato <b>non contiene testo</b>, per favore invia la <b>descrizione</b> del <b>gruppo</b> che vuoi fare entrare in <b>IATA</b>")
        return

    description = message.text
    c.execute('''UPDATE submit SET description=? WHERE chat_id=?''',(description, chat.id,))
    c.execute('''SELECT * FROM submit''')
    rows = c.fetchall()
    conn.commit()

    for res in rows:
        chat_id = res[0]
        name = res[1]
        link = res[2]
        admins = res[3]
        description = res[4]

    bot.chat(26170256).send("<b>RICHIESTA D\'</b>#ISCRIZIONE"
                            "\n\n<b>INFORMAZIONI SUL GRUPPO</b>"
                            "\n<b>Nome del gruppo</b>: {0}"
                            "\n<b>Link del gruppo</b>: {1}"
                            "\n<b>Lista degli admins del gruppo</b>: {2}"
                            "\n<b>Descrizione del gruppo</b>: {3}"
                            "\n\n<b>INFORMAZIONI DEL RICHIEDENTE</b>"
                            "\n<b>Nome</b>: {4}"
                            "\n<b>ID</b>: #id{5}"
                            "\n<b>Username</b>: @{6}".format(name, link, admins, description, message.sender.name, str(message.sender.id), str(message.sender.username))
                    )

    text = (
        "<b>Grazie!</b>"
        "\nLa tua richiesta è stata <b>presa in carico</b> e degli <b>admins IATA</b> la valuteranno."
    )

    bot.api.call("sendMessage", {
        "chat_id":chat.id, "text": text, "parse_mode":"HTML", "reply_markup":
            '{"inline_keyboard": [[{"text":"🔙Torna al menù principale", "callback_data":"cancel"}]]}'
    }
    )

    API.db.updateState(chat.id, "nullstate", 0)
    conn.commit()

@bot.process_message
def contact1(chat, message):
    '''Submit a suggestion'''
    state, temp = API.db.getState(chat.id)
    conn.commit()
    if state != "contact1":
        return

    if message.text == None:
        message.reply("<b>Attenzione!</b>\nIl messaggio inviato <b>non contiene testo</b>, per favore <b>invia del testo</b> da inviare a <b>IATA</b>")
        return

    text = str(message.text)

    bot.chat(26170256).send("#MESSAGGIO<b> IN ARRIVO</b>"
                            "\n<b>Nome</b>: {0}"
                            "\n<b>Username</b>: {1}"
                            "\n<b>ID</b>: #id{2}"
                            "\n<b>Testo</b>: {3}"
                            "\n\n<i>Se il messaggio è offensivo lo puoi bannare facendo /ban {2}</i>"
                            "\n<i>Puoi rispondere a questo messaggio facendo /r {2} RISPOSTA</i>".format(message.sender.name, str(message.sender.username), str(message.sender.id), text)
                            , syntax="HTML"

    )

    chat.send("Grazie! A breve un <b>admin IATA</b> ti risponderà")

    API.db.updateState(chat.id, "nullstate", 0)
    conn.commit()

@bot.command("ban")
def ban(chat, message, args):
    IATA_admins = [26170256, 195973896, 41600129, 39156973, 187120083, 127354414, 138388750, 40955937, 68797644, 36536108]
    if message.sender.id not in IATA_admins:
        message.reply("<b>Non puoi bannare gente dal bot, non hai i permessi.</b>"
                    "\nSe credi che questo sia un <b>errore</b> o sei un <b>nuovo admin IATA</b>, contatta @MarcoBuster o @lollofra"
                    )
        return

    if len(args) == 0:
        message.reply(
                    "\nPer <b>bannare</b> utenti dal bot devi sapere il loro <b>id utente</b>, poi fare: <code>/ban IDUTENTE</code>."
                    "\nEsempio: <code>/ban 12345678 MOTIVO</code>"
                    )
        return

    user_id = args[0]
    if len(args) > 1:
        motivazione = ' '.join(args[1:])
    else:
        motivazione = "Nessuna motivazione specificata"

    try:
        int(user_id)
    except ValueError:
        message.reply("L\'<b>ID utente</b> specificato ({0}) non è valido".format(str(user_id)))
        return

    c.execute('''DELETE FROM ban WHERE user_id=?''', (user_id,))
    c.execute('''INSERT INTO ban VALUES(?, ?)''', (user_id, motivazione))
    conn.commit()

    try:
        bot.chat(user_id).send("Sei stato <b>bannato</b> da questo bot da un <b>admin IATA</b>\n"
        "<b>ATTENZIONE!</b> Questo non significa che sei stato messo in <a href=\"telegram.me/IATABlacklist\">Blacklist</a>, ma solo che non potrai più usare questo bot\n"
        "<b>Motivo</b>: {0}".format(motivazione)
        , preview=False
        )
    except Exception as e:
        pass

    message.reply("Utente {0} aggiunto nei database <b>bannati</b> con motivazione {1}"
                "\nSe hai sbagliato puoi sbannarlo facendo <code>/unban {0}</code>".format(str(user_id), motivazione)
            )

@bot.command("unban")
def unban(chat, message, args):
    IATA_admins = [26170256, 195973896, 41600129, 39156973, 187120083, 127354414, 138388750, 40955937, 68797644, 36536108]
    if message.sender.id not in IATA_admins:
        message.reply("<b>Non puoi sbannare gente dal bot, non hai i permessi.</b>"
                    "\nSe credi che questo sia un <b>errore</b> o sei un <b>nuovo admin IATA</b>, contatta @MarcoBuster o @lollofra"
                    )
        return

    if len(args) == 0:
        message.reply(
                    "\nPer <b>sbannare</b> utenti dal bot devi sapere il loro <b>id utente</b>, poi fare: <code>/ban IDUTENTE</code>."
                    "\nEsempio: <code>/unban 12345678 MOTIVO</code>"
                    )
        return

    user_id = args[0]
    if len(args) > 1:
        motivazione = ' '.join(args[1:])
    else:
        motivazione = "Nessuna motivazione specificata"

    try:
        int(user_id)
    except ValueError:
        message.reply("L\'<b>ID utente</b> specificato ({0}) non è valido".format(str(user_id)))
        return

    c.execute('''DELETE FROM ban WHERE user_id=?''', (user_id,))
    conn.commit()

    try:
        bot.chat(user_id).send("Sei stato <b>sbannato</b> da questo bot da un <b>admin IATA</b>\n"
        "<b>Motivo</b>: {0}".format(motivazione)
        )
    except Exception as e:
        pass

    message.reply("Utente {0} rimosso nei database <b>bannati</b> con motivazione {1}"
                "\nSe hai sbagliato puoi ri-bannarlo facendo <code>/ban {0}</code>".format(str(user_id), motivazione)
            )

@bot.command("admin")
def admin(chat, message):
    IATA_admins = [26170256, 195973896, 41600129, 39156973, 187120083, 127354414, 138388750, 40955937, 68797644, 36536108]
    if message.sender.id not in IATA_admins:
        message.reply("<b>Non puoi accedere a questo comando del bot, non hai i permessi.</b>"
                    "\nSe credi che questo sia un <b>errore</b> o sei un <b>nuovo admin IATA</b>, contatta @MarcoBuster o @lollofra"
                    )
        return

    text = (
        "<b>Benvenuto nel pannello admin del bot</b>"
    )
    bot.api.call("sendMessage", {
        "chat_id":chat.id, "text":text, "parse_mode":"HTML", "reply_markup":
            '{"inline_keyboard":[[{"text":"❓Aiuto admins", "callback_data":"adminhelp"}],'+
            '[{"text":"🔨Bannati", "callback_data":"bans"}, {"text":"⏰Chiama il dev", "callback_data":"wakeup"}]'+
        ']}'
    })

@bot.command("r")
def reply(chat, message, args):
    IATA_admins = [26170256, 195973896, 41600129, 39156973, 187120083, 127354414, 138388750, 40955937, 68797644, 36536108]
    if len(args) < 2:
        message.reply("<b>Errore di formato!</b>\nIl formato giusto è: <code>/r user_id risposta con Markdown</code>")
        return

    user_id = args[0]
    text = ' '.join(args[1:]) + "\n\n✍️*Gli admins di IATA*"

    try:
        int(user_id)
    except ValueError:
        message.reply("L\'<b>ID utente</b> specificato ({0}) non è valido".format(str(user_id)))
        return

    bot.api.call("sendMessage", {
        "chat_id":user_id, "text":text, "parse_mode":"Markdown", "reply_markup":
            '{"inline_keyboard":[[{"text":"🗣Rispondi", "callback_data":"contact"}]]}'
    })


if __name__ == "__main__":
    bot.run()
