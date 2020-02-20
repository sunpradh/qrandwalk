#==============================
#     Quantum Random Walk
#==============================
import math 
import numpy as np
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from   plotly.subplots   import make_subplots
from   dash.dependencies import Output, Input, State
from   dash.exceptions   import PreventUpdate
from   qrandwalk         import *

#----------------------------------------
# 3: Creazione dell'interfaccia
#----------------------------------------

Psi      = InitState( np.int(L/2), [[1,0],[0,0]] )
CDistr   = InitCWalk( np.int(L/2) )

# Crea l'app, l'oggetto principale che conterrà tutta l'applicazione
app = dash.Dash(__name__)

# Definisci le caselle di testo e bottoni
ButtonToggle = html.Button( id='toggle-button', children='Start', className="button")
ButtonReset  = html.Button( id='reset-button',  children='Reset', className="button")

InputUpReal  = dcc.Input( id="input-upreal", type="number", step=1,   value=1. )
InputUpImag  = dcc.Input( id="input-upimag", type="number", step=1,   value=0. )
InputDwReal  = dcc.Input( id="input-dwreal", type="number", step=1,   value=0. )
InputDwImag  = dcc.Input( id="input-dwimag", type="number", step=1,   value=0. )
InputPos     = dcc.Input( id="input-pos", type="number",    step=1,   value=np.int(L/2), max=L-1, min=0)


#----------------------------------------
# Corpo principale dell'application
#----------------------------------------
app.layout = html.Div(children=[
    html.Div([
        html.H1("Quantum Random Walk"),
        # Start/stop button
        ButtonToggle,
        ButtonReset,
        # Caselle di testo in cui impostare le condizioni iniziali
        html.Div([
            html.Table([
                html.Tr([
                    html.Td(html.Label("Ψ↑"), colSpan=2),
                    html.Td(html.Label("Ψ↓"), colSpan=2),
                    html.Td(html.Label("Position")),
                    ], className="theader"),
                html.Tr([
                    html.Td(["Re:", InputUpReal]),
                    html.Td(["Im:", InputUpImag]),
                    html.Td(["Re:", InputDwReal]),
                    html.Td(["Im:", InputDwImag]),
                    html.Td(InputPos)
                    ])
                ], style={'margin': 'auto'}), 
            ], className="inputs"),
        ], className="header"),
    # GRAFICI
    dcc.Graph( id='qrandwalk', animate=True, figure=qrandwalk_figure(Psi,CDistr)),
    # Timer
    dcc.Interval( id='timer', interval=700, disabled=True),
    ], style={ 'margin': '0px 0px'})

#----------------------------------------
# Callbacks
#----------------------------------------
reset_clicks = 0 # numero di click del pulsante reset
# Aggiorna `qrandwalk` in base a `timer`
@app.callback(
        # Genera i plot in output
        Output('qrandwalk', 'figure'), 
        [ 
            # stato del timer e pulsante di reset
            Input('timer','n_intervals'), 
            Input('timer','disabled'),
            Input('reset-button','n_clicks')
            ],
        [
            # condizioni iniziali da leggere in caso di reset
            State('input-pos',    'value'),
            State('input-upreal', 'value'),
            State('input-upimag', 'value'),
            State('input-dwreal', 'value'),
            State('input-dwimag', 'value'),
            ]
        )
# Questa funzione viene chiamata ogni volta che
# 1) scorre il timer 2) il timer viene attivato/disattivato 3) viene premuto reset
def update_graph(n, is_dis, n_reset, pos, upreal, upimag, dwreal, dwimag):
    # Accedi al vettore di stato globale e alla distribuzione classica
    # che sono definiti in ambito globale
    global Psi
    global CDistr
    # accedi anche al numero di click del pulsante reset
    global reset_clicks

    # Se il timer non è disabilitato e il pulsante reset non 
    if not is_dis and (n_reset == reset_clicks or n_reset is None):
        # Esegui due step del quantum random walk
        Psi = Walk(Walk(Psi, H), H)
        # Esegui due step del classic random walk
        CDistr = CWalk(CWalk(CDistr))
    if n_reset is not None and n_reset > reset_clicks:
        # Q-Random Walk reset
        reset_clicks = reset_clicks + 1
        Psi = InitState(pos, [[upreal,upimag],[dwreal,dwimag]])
        # C-Random Walk reset
        CDistr = InitCWalk(pos)
    return qrandwalk_figure(Psi,CDistr)

# Inizia o ferma l'animazione
@app.callback(
        [
            Output('timer', 'disabled'), 
            Output('toggle-button', 'children')
            ],
        [ Input('toggle-button', 'n_clicks'), ],
        [ State('toggle-button', 'children') ]
        )
def toggle_timer(n, state):
    if n is None:
        raise PreventUpdate
    if state == 'Start':
        return False, 'Stop'
    else: 
        if state == 'Stop':
            return True, 'Start'



if __name__ == '__main__':
    app.run_server(debug=False)
