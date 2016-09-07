import Bot

import botogram

import sqlite3
conn = sqlite3.connect('IATA-bot.db')
c = conn.cursor()

class db:
    '''Database management'''

    def createTables():
        '''Creates all tables'''
        conn = sqlite3.connect('IATA-bot.db')
        c = conn.cursor()

        try:
            c.execute('''CREATE TABLE state(chat_id INTEGER, state TEXT, temp INTEGER)''')
        except sqlite3.OperationalError as e:
            pass
        try:
            c.execute('''CREATE TABLE report(chat_id INTEGER, reported_info TEXT, reported_evidence TEXT)''')
        except sqlite3.OperationalError as e:
            pass
        try:
            c.execute('''CREATE TABLE submit(chat_id INTEGER, name TEXT, link TEXT, admins TEXT, description TEXT)''')
        except sqlite3.OperationalError as e:
            pass
        conn.commit()

    def updateState(chat_id, new_state, temp):
        '''Update the state'''
        c.execute('''DELETE FROM state WHERE chat_id=?''',(chat_id,))
        c.execute('''INSERT INTO state VALUES(?,?,?)''',(chat_id, new_state, temp,))
        conn.commit()

    def getState(chat_id):
        '''Returns the state'''
        c.execute('''SELECT * FROM state WHERE chat_id=?''', (chat_id,))
        items = c.fetchall()
        for res in items:
            return res[1], res[2]
