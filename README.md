# Quantum Random Walk

Questo progetto permetta di visualizzare l'evoluzione temporale del *Quantum Random Walk* e confrontarlo con l'evoluzione temporale della distribuzione di probabilità del random walk classico.
Utilizza [Python](https://www.python.org/) e le librerie [Numpy](https://numpy.org/) (per la manipolazione algebrica), [Plotly](https://github.com/plotly/plotly.py) e [Dash](https://github.com/plotly/dash) (per l'aspetto grafico e la parte interattiva).

## Struttura
Il progetto è costituito dal file `qrandwalk.py` che contiene la parte di algoritmo del random walk classico e quantistico e dal file `app.py` che invece contiene il resto dell'applicazione.
Nella cartella `assets` è contenuto un file ausiliare che cura l'aspetto della applicazione.

## Requisiti e installazione
Gli unici requisiti sono Python e le librerie prima citate.
Consultare i relativi siti per avere più info al riguardo.
Se Python è già presente allora è sufficiente dare da terminale
```
pip install numpy plotly dash
```

## Avvio e utilizzo
Per avviare l'applicazione, da terminale è sufficiente spostarsi nella cartella del progetto ed eseguire
```
python app.py
```
Se tutto va bene ci si aspetta un output del tipo
```
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:8050/ (Press CTRL+C to quit)
```

Successivamente, dal proprio browser andare all'indirizzo (http://127.0.0.1:8050/) per poter usare l'applicazione.
L'interfaccia è abbastanza semplice, sono presenti due pulsantia:
 * Il primo `Start` serve per avviare o fermare l'animazione
 * Il secondo `Reset` serve per resettare il sistema alle condizioni iniziali specificate nelle caselle a fianco
Le caselle di testo a lato servono per specificare le condizioni iniziali, in particolare:
 * Parte reale e immaginaria della componente di spin ↑
 * Parte reale e immaginaria della componente di spin ↓
 * Posizione iniziale
Inoltre sul plot sono presente anche vari pulsanti per poter interagire con i grafici.

Per terminare l'applicazione è sufficiente dal terminale dare `CTRL-C`
