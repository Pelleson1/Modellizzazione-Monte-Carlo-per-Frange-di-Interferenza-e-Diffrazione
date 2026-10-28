# Simulazione Monte Carlo e Fit di Frange di Interferenza e Diffrazione

Questo progetto contiene un esperimento virtuale sviluppato in Python il cui obiettivo è simulare l'acquisizione di un segnale luminoso caratterizzato da frange di interferenza modulate da un inviluppo di diffrazione, studiando il comportamento statistico del sistema attraverso il metodo Monte Carlo ed eseguendo un fit pesato ai minimi quadrati per la stima dei parametri fisici e la diagnostica del modello.



## Descrizione del Modello Fisico

L'intensità luminosa del pattern di frange di interferenza e diffrazione, modulata da un fondo uniforme, è descritta dalla seguente relazione:

$$f(x; B, I_0, \alpha, \delta) = B + I_0 \left[ \frac{\sin(\alpha x)}{\alpha x} \right]^2 \cos^2(\delta x)$$

Dove:
- **$B$**: Fondo uniforme di conteggi.
- **$I_0$**: Scala dell'intensità del segnale.
- **$\alpha$**: Parametro legato alla larghezza dell'inviluppo di diffrazione ($\alpha = k a$).
- **$\delta$**: Frequenza spaziale delle frange di interferenza ($\delta = k d$).



## Struttura dell' esperimento virtuale

L'esperimento virtuale è suddiviso in due parti principali:

### 1. Simulazione Monte Carlo (Prova 1)
- **Controllo del Modello Teorico:** Verifica della non-negatività, della simmetria e della continuità in $x=0$.
- **Simulazione di una Singola Acquisizione:** Generazione di un conteggio poissoniano $n_i \sim \text{Poisson}(\mu_i)$ ed estrazione dei conteggi centrali $N_c$.
- **Studio dello Stimatore:** Esecuzione di 2000 pseudo-esperimenti per studiare la distribuzione statistica di $N_c$, verificando la deviazione standard e l'accordo con il valore atteso.
- **Generazione del Dataset:** Salvataggio della media dei 2000 esperimenti con l'opportuno riscalamento dell'errore statistico ($\sigma_{\bar{y}} = \bar{y} / \sqrt{N\_experiments}$) nel file `data.csv`.

(Questa parte è contentuta nella cartella "simulazione_mc")

### 2. Fit e Diagnostica (Prova 2)
- **Caricamento e Controllo Dati:** Verifica dell'integrità del dataset `data.csv` e analisi degli intervalli di misura.
- **Stime Iniziali e Bounds:** Definizione ragionevole dei parametri di partenza $p_0 = (B_0, I_0, \alpha_0, \delta_0)$ ricavati geometricamente dai dati grafici e impostazione di vincoli fisici (bounds).
- **Fit Pesato ai Minimi Quadrati:** Utilizzo di `scipy.optimize.curve_fit` con `absolute_sigma=True` per l'estrazione ottima dei parametri e il calcolo della matrice di covarianza e correlazione.
- **Diagnostica e Validazione Statistica:** Analisi dei residui normalizzati (Pull), calcolo del $\chi^2$ ridotto e del $p$-value associato (`scipy.stats.chi2.sf`) per verificare la bontà del fit.

(Questa parte è contentuta nella cartella "fit")



## Strumenti e Librerie Utilizzate

- **Python 3.12.3**
- **Jupyter Notebook**
- **NumPy**: Per la generazione degli array, il calcolo vettoriale e il campionamento statistico.
- **SciPy**: Per l'ottimizzazione e il fit dei dati (`curve_fit`) e per la valutazione delle distribuzioni statistiche (`chi2`).
- **Matplotlib**: Per la visualizzazione grafica delle curve teoriche, delle barre di errore e degli istogrammi.

## Autori
**Pellè Andrea**, **Ricciotti Luca**, **Rimodini Diego** (2026)