# Domande Frequenti e Problemi Comuni

## Problemi con il Toctree

Se durante la stesura dei file `.md` si verificano errori nel `toctree`, potrebbe comparire una riga anomala come:

`<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">`

immediatamente dopo l’ultimo elemento del `toctree`. Questo errore è solitamente causato dalla mancata chiusura corretta del blocco `toctree`.

Assicurarsi di chiudere il `toctree` utilizzando i simboli "```".  
Se il blocco termina con un nome di file `.md` non seguito dalla chiusura corretta, l’errore continuerà a presentarsi.

## Problemi Durante la Build

Se durante la fase di build viene restituito l’errore:

`[WinError 32] Impossibile accedere al file. Il file è utilizzato da un altro processo`

verificare che il prompt dei comandi di Windows non stia ancora eseguendo un server Python o hostando il sito.

Chiudere la finestra del prompt dei comandi prima di lanciare nuovamente il comando di build.  
Il tool richiede accesso esclusivo a determinate directory durante l’esecuzione.