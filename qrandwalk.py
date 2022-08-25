#==============================
#     Quantum Random Walk
#------------------------------
# Autore: Sunny Pradhan
#==============================
import math
import numpy as np
import plotly.graph_objects as go
from   plotly.subplots   import make_subplots

#------------------------------
# 1: Quantum Random walk
#------------------------------

# Numero di siti
L = 500
def InitState(Pos, Spin):
    """
        Crea stato iniziale Il vettore di stato è una matrice Lx2 (gdl spaziali x gdl spin)
        Input:
            Pos:  posizione iniziale
            Spin: configurazione dello spin iniziale
                 deve essere una matrice 2x2 che deve contenere parte reale e immaginaria
                 delle componenti di spin ↑ e spin ↓
        Output:
            array L x 2 complesso che rappresenta lo stato |Pos, Spin> (normalizzato a 1)
        Esempio:
            InitState(0, [[1,0], [0,0]]) ---> |0,↑>
            InitState(0, [[1,0], [0,1]]) ---> ( |0,↑> + i|0,↓>) /sqrt(2)
    """
    state = np.zeros((L,2), dtype=complex)
    norm  = math.sqrt( Spin[0][0]**2 + Spin[0][1]**2 + Spin[1][0]**2 + Spin[1][1]**2)
    state[Pos,0] = (Spin[0][0] + Spin[0][1]*1j) / norm
    state[Pos,1] = (Spin[1][0] + Spin[1][1]*1j) / norm
    return state

# Varie Operazioni a 1 qubit:
#   Hadamard
H = np.array( [[1,1],   [1,-1]], dtype=complex ) * math.sqrt(0.5)
#   Gate X
X = np.array( [[0,1],   [1,0]],  dtype=complex )
#   Gate Y
Y = np.array( [[0,-1j], [1j,0]], dtype=complex )
#   Gate Z
Z = np.array( [[1,0],   [0,-1]], dtype=complex )

# Operatori di shift:
#   Shift in avanti
Splus  = np.zeros( (L,L), dtype=complex )
#   Shift indietro
Sminus = np.zeros( (L,L), dtype=complex )
for k in range(L-1):
    Splus[k,k+1]  = 1
    Sminus[k+1,k] = 1
# Splus e Sminus sono stati definiti di tipo complesso
# perchè lavoreranno su vettori complessi

def Walk(State, CoinFlip = H):
    """
        Esegui uno step del Quantum Random Walk
        Input:
           State: vettore di stato, di dimensione L x 2
           CoinFlip: operazione unitaria sullo spin (default: H)
        Output:
           nuovo vettore di stato
        Esempio:
           Psi = Walk(Psi, H) ---> Esegui il walk sullo stato Psi con la porta di Hadamard
    """
    # esegui il Coin flip per ogni sito
    for k in range(max(State.shape)):
        State[k,:] = State[k,:] @ CoinFlip
    # Trasla la componente di spin ↑ avanti
    # (l'operatore @ indica il prodotto tra matrici)
    State[:,0] = State[:,0] @ Splus
    # Trasla la componente di spin ↓ indietro
    State[:,1] = State[:,1] @ Sminus
    return State

# Calcola il modulo quadro della funzione d'onda
def Prob(State):
    return np.sqrt( abs(State[:,0])**2 + abs(State[:,1])**2)

#------------------------------
# 2: Classic Random Walk
#------------------------------

# Probabilità
# P[0]: probabilità per lo step in avanti
# P[1]: probabilità per lo step indietro
P = np.array([ 0.5, 0.5 ])

def InitCWalk(Pos):
    """
        Inizializza il vettore che rappresenta la distribuzione di probabilità
        del random walk classico
        Input:
            Pos: posizione iniziale di partenza
        Output:
            vettore reale lungo L di zeri, con un 1 nella posizione Pos
        Esempio:
            D = InitCWalk(10) ---> D = [0,...0,1,0,...,0] dove l'1 sta nella posizione 10
    """
    State = np.zeros(L)
    State[Pos] = 1
    return State

# Operatori di shift, analoghi agli operatori di shift del quantum random walk
# l'unica differenza: sono salvate come matrici reali
CSplus  = np.zeros((L,L))
CSminus = np.zeros((L,L))
for k in range(L-1):
    CSplus[k,k+1]  = 1
    CSminus[k+1,k] = 1

# Esegui il walk classico di 1 step
def CWalk(State):
    """
        Esegui uno step del random walk classico
        Input:
            State: vettore della distribuzione di probabilità
        Output:
            vettore della distribuzione di probabilità dopo uno step
        Esempio ( supponiamo L=5 e P = [0.5,0.5] ):
            D = InitCWalk(2)
            ---> D = [0,0,1,0,0]
            D = CWalk(D)
            ---> D = [0,0.5,0,0.5,0]
    """
    State = State @ ( P[0]*CSplus + P[1]*CSminus )
    return State

#------------------------------
# 3: Creazione dei plot
#------------------------------

def qrandwalk_figure(State, CState):
    """
        genera un i vari plot (modulo quadro, parti reali e immaginarie, distribuzione classica)
        usando la libreria Plotly
        Input:
            State: vettore di stato quantistico
            Cstate: distribuzione di probabilità classica
        Output:
            oggetto contenente in totale 6 subplot disposti su una griglia 4x2
    """
    # Conta il numero di siti
    N  = max(State.shape)
    # Genera un array che rappresenterà il dominio
    domain = 2 * np.arange(N)
    # Struttura dei subplots
    fig = make_subplots(
            rows=4,
            cols=2,
            specs= [[{'rowspan': 2}, {}],
                    [None,           {}],
                    [{'rowspan': 2}, {}],
                    [None,           {}]],
            column_widths=[0.7, 0.3],
            shared_xaxes=True,
            vertical_spacing=0.05,
            horizontal_spacing=0.02,
            subplot_titles=("|Ψ|²", "Re(Ψ↑)", "Im(Ψ↑)",  "Classic walk", "Re(Ψ↓)", "Im(Ψ↓)")
            )
    # Sei differenti subplot
    # NB: verranno plottati solo i siti pari per creare una buona animazione dell'evoluzione temporale
    # Plot principale, del modulo quaddro
    fig.add_trace(
            go.Scatter(name='|Ψ|²',   x=domain, y=Prob(State)[0:N:2]),
            row=1, col=1
        )
    # Secondo plot principale, della distribuzione classica
    fig.add_trace(
            go.Scatter(name='Cl. walk', x=domain, y=CState[0:N:2]),
            row=3, col=1 )
    # Plot delle parti reali e immaginarie delle componenti a spin ↑ e ↓
    fig.add_trace(
            go.Scatter(name="Re(Ψ↑)", x=domain, y=State[:,0].real[0:N:2]),
            row=1, col=2 )
    fig.add_trace(
            go.Scatter(name="Im(Ψ↑)", x=domain, y=State[:,0].imag[0:N:2]),
            row=2, col=2 )
    fig.add_trace(
            go.Scatter(name="Re(Ψ↓)", x=domain, y=State[:,1].real[0:N:2]),
            row=3, col=2 )
    fig.add_trace(
            go.Scatter(name="Im(Ψ↓)", x=domain, y=State[:,1].imag[0:N:2]),
            row=4, col=2 )

    # smooth lines su tutti i subplot e setta altezza
    fig.update_traces( line={ 'shape': 'spline', 'smoothing': 0.5 })
    fig.update_layout( height=700, margin={'t':50})
    return fig

