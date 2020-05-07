import pandas as pd
import math
import yfinance as yf
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import os
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

airlines = ['ALK', 'AVH', 'AZUL', 'CEA', 'ZNH', 'VLRS', 'DAL', 'GOL', 'LTM', 'LUV', 'SAVE']
al_data = yf.download("ALK AVH AZUL CEA ZNH VLRS DAL GOL LTM LUV SAVE", start="2017-01-01", end="2021-05-03")
df = pd.DataFrame(data=al_data)
acdf = df['Adj Close']
fig = go.Figure()

def add_lines(strategy):
    for company in strategy:
        fig.add_trace(go.Scatter(x=acdf.index,y=acdf[company], mode='lines', name=company))
        fig.update_layout(             
            xaxis=dict(title="NYSE Ticker"),
            yaxis=dict(title="Adj Close")
        )
add_lines(airlines)

def plot_event(event_date):
    change_list = []
    for company in airlines:
        last_close = acdf[company].last('1D')[0]
        us_case_close = acdf[company][(acdf.index == event_date)][0]
        percent_change = ((last_close - us_case_close)/(us_case_close))*100
        change_list.append(percent_change)
    return {
        'data': [
            {'x': airlines, 'y':change_list, 'type':'bar'}
        ],
        'layout': {
            'title': 'Percentage change since {}'.format(event_date),
            'xaxis': {'title':'NYSE Ticker'}, 
            'yaxis': {'title': 'Percent'}
            
        }
    } 

app.layout = html.Div([
    dbc.Navbar([
        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Airlines During Pandemic", className="ml-3")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="http://pandemair.herokuapp.com/",
        ),
    ], color="#4e455d", dark=True, fixed='top'),
    html.H4('Airline stocks on the NYSE closing price since 2017', style={'margin-top': '15vh', 'textAlign':'center'}),
    html.Div([
        html.P('Click on ticker on right side of graph to show/hide line'),
        html.P('Double-click to isolate line')
    ], style={'border': '2px solid #4e455d', 'text-align':'center','padding': '15px 10px 5px 10px', 'margin':'30px auto 0 auto', 'background-color':'#82d8d8', 'max-width':'30vw', 'border-radius': '10px'}),
    dcc.Graph(
        id='airline-graph',
        figure = fig
    ),
    html.H4('Stock change since event occured:', style={'margin-top': '15vh', 'textAlign':'center'}),
    dcc.Dropdown(id='select_event',
    options=[
        {'label': 'Jan 21: First US case of Coronavirus', 'value': '2020-01-21'},
        {'label': 'Jan 31: Travel blocked from China', 'value': '2020-01-31'},
        {'label': 'Feb 26: First community spread case documented', 'value': '2020-02-26'},
        {'label': 'Mar 4: House passes $8.3 billion emergency bill', 'value': '2020-03-04'},
        {'label': 'Mar 11: Travel banned from Europe', 'value': '2020-03-11'},
        {'label': 'Mar 13: National emergency declaration', 'value': '2020-03-13'},
        {'label': 'Mar 27: Trump signs $2.2 trillion emergency spending bill', 'value': '2020-03-27'},
        {'label': 'Apr 13: Trump claims "total" authority over governors on openings', 'value': '2020-04-13'},
        {'label': 'May 2: Buffet announces Berkshire Hathaway sold all airline stock', 'value': '2020-05-01'},
    ], value='2020-01-02', style = {'margin': '0 auto', 'max-width':'90%'}
),
    html.Div(id='event_graph'),
])

@app.callback(
    Output('event_graph', 'children'),
    [Input('select_event', 'value')])
def callback_a(selected_event):
    return dcc.Graph(figure=plot_event(selected_event))

if __name__ == '__main__':
    app.run_server(debug=True)
