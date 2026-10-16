# Simulazione Monte Carlo: Interferenza e Diffrazione

Questo progetto contiene un esperimento virtuale sviluppato in Python il cui obiettivo è simulare l'acquisizione di un segnale luminoso caratterizzato da frange di interferenza modulate da un inviluppo di diffrazione, studiando il comportamento statistico del sistema attraverso il metodo Monte Carlo.

## Descrizione del progetto

Il numero medio atteso di conteggi è espressa dalla seguente relazione fisica:

$$\mu(x) = B + I_0 \left[ \frac{\sin(\alpha x)}{\alpha x} \right]^2 \cos^2(\delta x)$$

Dove:
* **$B$**: Fondo uniforme.
* **$I_0$**: Scala del segnale.
* **$\alpha$**: Larghezza dell’inviluppo.
* **$\delta$**: Frequenza spaziale delle frange.

## Obiettivi dell'esperimento virtuale

Il notebook è strutturato in tre fasi principali:
1. **Costruzione e controllo del modello teorico:** Verifica delle proprietà matematiche della funzione (non negatività, simmetria, rimozione della singolarità in $x=0$).
2. **Simulazione di una singola acquisizione:** Generazione di un campionamento casuale estratto da una distribuzione Poissoniana e confronto dei conteggi nella regione centrale con le fluttuazioni statistiche attese ($\sqrt{\mu_c}$).
3. **Distribuzione dello stimatore:** Ripetizione dell'esperimento per 2000 volte per estrarre la distribuzione di probabilità dei conteggi, calcolando media e deviazione standard campionaria.

## Strumenti e librerie utilizzate

* **Python 3.x**
* **Jupyter Notebook**
* **NumPy**: Per la generazione degli array, il calcolo vettoriale e il campionamento statistico.
* **Matplotlib**: Per la visualizzazione grafica delle curve teoriche, delle barre di errore e degli istogrammi.
