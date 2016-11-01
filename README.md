# IATA bot
##### Il bot ufficiale di IATA
Questo è un bot di supporto all'*[Italian Telegram Admin Alliance](www.iata.ovh)* (**IATA**).
Permette di *inviare segnalazioni di utenti molesti*, *proporre il proprio gruppo per l'iscrizione in IATA* e *contattare il team di IATA*, tutto questo da un **bot per Telegram**

### Crediti
Il bot è programmato in **Python** da [MarcoBuster](www.github.com/MarcoBuster) utilizzando il framework [botogram](www.github.com/botogram). 

### Installazione
Per installare questo bot sulla propria **VPS Linux**, bisogna:

    $ python3 -m pip install botogram
    $ git clone www.github.com/IATA-dev/IATA-bot.git && cd IATA-bot
    $ nano "Bot.py"
> Nota: Bisogna modificare il file "Bot.py" sostituendo:
> Il TOKEN del bot,
> la variabile IATA_admins con gli ID degli admins del bot,
> l'ID del gruppo personale IATA.

    $ python3 "Bot.py"
