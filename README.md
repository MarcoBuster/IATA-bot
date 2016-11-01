# IATA bot
##### Il bot ufficiale di IATA
Questo è un bot di supporto all'*[Italian Telegram Admin Alliance](www.iata.ovh)* (**IATA**).
Permette di *inviare segnalazioni di utenti molesti*, *proporre il proprio gruppo per l'iscrizione in IATA* e *contattare il team di IATA*, tutto questo da un **bot per Telegram**

### Crediti
Il bot è programmato in **Python** da [MarcoBuster](https://www.github.com/MarcoBuster) utilizzando il framework [botogram](https://www.github.com/botogram). 

### Installazione
Per installare questo bot sulla propria **VPS Linux**, bisogna:

    $ python3 -m pip install botogram
    $ git clone https://www.github.com/IATA-dev/IATA-bot.git && cd IATA-bot
    $ nano CONFIG.py
> Nota: Bisogna modificare il file "CONFIG.py" inserendo:
> Il TOKEN del bot,
> ID degli admins del bot nell'array ADMINS,
> l'ID del gruppo admin nella variabile ADMIN_GROUP.
> Facoltativo: Modificare a piacimento i messaggi inviati all'utente

    $ python3 Bot.py
