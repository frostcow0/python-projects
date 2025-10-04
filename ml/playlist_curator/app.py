import json
import logging
import requests
import pandas as pd
import dash_bootstrap_components as dbc
from sys import stdout
from datetime import date
from dash import Dash, html, callback, Input, Output, State, dash_table, dcc


logger = logging.getLogger("Dash_Frontend")
sh = logging.StreamHandler(stdout)
fh = logging.FileHandler(f"./logs/frontend_errors_{date.today()}.log")
sh.setLevel(logging.INFO)
fh.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(sh)

external_stylesheets = [dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Playlist Curator v0.9', style={
        'textAlign': 'center',
    }),

    html.Div(children='''
    An app that, using your recently played songs,
     creates a playlist of 20 songs tailored to you.
    ''', style={
        'textAlign': 'center',
    }),

    html.Br(),
    html.Div([
        html.Button('Get Recommended Playlist', id='get-recommended'),
        html.Br(),
        html.Br(),
        dcc.Loading(id="loading", children=[html.Div(id='recommended-output')], type="default"),
        ], style={
            'textAlign': 'center', 'width': '600px', 'justify': 'center', 'align': 'center',
            'marginLeft': 'auto', 'marginRight': 'auto'
        }
    ),
    html.Footer(style={
        'backgroundColor': 'grey', 'height': '60px', 'position': 'fixed', 'left': '0',
        'bottom': '0', 'width': '100%', 'color': 'white', 'textAlign': 'center'
        }
    )
])

@callback(
    Output('recommended-output', 'children'),
    Input('get-recommended', 'n_clicks'),
    State('recommended-output', 'children'))
def get_recommended_songs(n_clicks, existing_state):
    logger = logging.getLogger("Dash_Frontend")
    # this function is called on page load, so make sure someone actually clicked the button lol
    if n_clicks == None:
        return existing_state

    # maybe check out storage so we can cache this
    user_data = requests.get("http://127.0.0.1:8000/user_data")
    
    if user_data.status_code != 200:
        logger.error("Non-200 status code for user data API request: %s", user_data)
        return dbc.Alert("There was an error trying to retrieve your recently played & liked songs, please try again later.", color="danger")
    else:
        user_data = user_data.json()

    response = requests.post(
        "http://127.0.0.1:8000/minkowski_recommend",
        data = json.dumps(user_data),
        headers = {'Content-Type': 'application/json'}
    )

    if response.status_code != 200:
        logger.error("Non-200 status code for minkowski recommend API request: %s", response)
        return dbc.Alert("There was an error trying to recommend you new songs, please try again later.", color="danger")
    else:
        response = response.json()

    formatted = pd.DataFrame().from_dict(response["formatted"])
    table = dash_table.DataTable(
        data=formatted.to_dict('records'),
        columns=[{"name": x, "id": x} for x in formatted.columns],
        style_cell={'textAlign': 'left'},
        style_as_list_view=True
    )
    button = html.Button('Save Playlist', id='save-recommended')
    return (table, html.Br(), button)

# @callback(
#     Output('recommended-output', 'children'),
#     Input('get-recommended', 'n_clicks'),
#     State('recommended-output', 'children'))
# def save_to_playlist(n_clicks, existing_state):
#     logger = logging.getLogger("Dash_Frontend")
#     # this function is called on page load, so make sure someone actually clicked the button lol
#     # if n_clicks == None:
#     #     return existing_state
#     return existing_state

#     response = requests.post(
#         "http://127.0.0.1:8000/save_playlist",
#         data = json.dumps(user_data),
#         headers = {'Content-Type': 'application/json'}
#     )

#     if response.status_code != 200:
#         logger.error("Non-200 status code for minkowski recommend API request: %s", response)
#         return dbc.Alert("There was an error trying to recommend you new songs, please try again later.", color="danger")
#     else:
#         response = response.json()

#     formatted = pd.DataFrame().from_dict(response["formatted"])
#     table = dash_table.DataTable(
#         data=formatted.to_dict('records'),
#         columns=[{"name": x, "id": x} for x in formatted.columns],
#         style_cell={'textAlign': 'left'},
#         style_as_list_view=True
#     )
#     return table

if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run(dev_tools_hot_reload=False)
