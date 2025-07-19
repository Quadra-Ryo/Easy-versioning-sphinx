# Guida all’Installazione e all’Uso del Tool

## Installazione

Il tool è disponibile su [PyPI](https://pypi.org/project/Easy-versioning/) e può essere installato facilmente utilizzando il comando `pip install easy-versioning`.  
Durante l’installazione, verranno automaticamente scaricati anche i pacchetti elencati nel file `requirements.txt`, essenziali per il corretto funzionamento del tool.

## Utilizzo

Per iniziare, è necessario organizzare le cartelle del progetto di documentazione nel seguente modo:

📦 Easy_versioning_Sphinx/  
├── 📂 data/  
│   └── 📄 Footer.md  
├── 📂 src/  
│   ├── 📁 V. X.XX/  
│   │   ├── 🌐 Language 1/  
│   │   │   └── 📘 Language 1 Sphinx Project/  
│   │   └── 🌐 Language 2/  
│   │       └── 📘 Language 2 Sphinx Project/  
│   ├── 📁 V. Y.YY/  
│   ├── 📁 V. Z.ZZ/

Dopodiché, aprire una console e posizionarsi nella directory principale del progetto (`Easy_versioning_Sphinx/` nel nostro esempio), quindi eseguire il comando: `Easy_versioning_build`

Il comando `Easy_versioning_build` accetta fino a due parametri opzionali:

1. **Lingua principale del progetto** (stringa): necessaria per garantire un corretto reindirizzamento nel caso in cui una versione della documentazione non sia disponibile in tutte le lingue. La lingua specificata deve essere presente in ogni versione del progetto.

2. **Gestione dei file sorgente** (intero): se impostato a `0`, i file `.md` di origine **non** verranno eliminati dal progetto finale; altrimenti verranno rimossi per rendere il progetto più leggero e facile da distribuire.

Se questi parametri non vengono specificati, il tool imposterà automaticamente la lingua predefinita su **inglese** ed eliminerà i file sorgente dalla build finale.

I file all’interno della cartella `src/` **non verranno mai modificati o sovrascritti**: le impostazioni influenzano esclusivamente l’output finale del progetto.

## Form di cambio lingua

Se, oltre alla cartella `src/`, viene aggiunta anche una directory `data/` contenente un file `footer.md`, sarà possibile personalizzare il footer della documentazione includendo un modulo per il cambio di versione e lingua.

Un esempio funzionante di `footer.md` è disponibile qui: [GitHub](https://github.com/Quadra-Ryo/Easy-versioning-sphinx/blob/main/Easy_versioning/footer.md).  
In assenza del file `data/footer.md`, verrà utilizzato il template predefinito reperibile al link indicato sopra.

Esempi:  
- `easy_versioning_build` — Utilizza l'inglese come lingua predefinita ed elimina la cartella `_source`.  
- `easy_versioning_build Italiano 0` — Imposta "Italiano" come lingua predefinita (quindi lo strumento cercherà la cartella "Italiano" all'interno della cartella delle versioni) e mantiene intatta la cartella `_source`.  
- `easy_versioning_build Deutsch` — Imposta "Deutsch" come lingua predefinita ed elimina la cartella `_source`.