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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

airlines = ['ALK', 'AVH', 'AZUL', 'CEA', 'ZNH', 'VLRS', 'DAL', 'GOL', 'LTM', 'LUV', 'SAVE']
al_data = yf.download("ALK AVH AZUL CEA ZNH VLRS DAL GOL LTM LUV SAVE", start="2017-01-01", end="2021-05-03")
df = pd.DataFrame(data=al_data)
acdf = df['Adj Close']
fig = go.Figure()

def add_lines(strategy):
    for company in strategy:
        fig.add_trace(go.Scatter(x=acdf.index,y=acdf[company], mode='lines', name=company))

add_lines(airlines)

def plot_event(strategy, event_date):
    change_list = []
    for company in strategy:
        last_close = acdf[company].last('1D')[0]
        us_case_close = acdf[company][(acdf.index == event_date)][0]
        percent_change = ((last_close - us_case_close)/(us_case_close))*100
        change_list.append(percent_change)
    print('Change List = {}'.format(change_list))
    return {
        'data': [
            {'x': strategy, 'y':change_list, 'type':'bar'}
        ]
    } 

us_fig = plot_event(airlines, '2020-01-21')
ch_block = plot_event(airlines, '2020-01-31')
com_spread = plot_event(airlines, '2020-02-26')
em_bill = plot_event(airlines, '2020-03-04')
eur_ban = plot_event(airlines, '2020-03-11')
nat_em = plot_event(airlines, '2020-03-11')
sp_bill = plot_event(airlines, '2020-03-27')
tot_auth = plot_event(airlines, '2020-04-13')



app.layout = html.Div([
    html.H1('Airline Ticker Tracker'),
    html.H4('Airline stocks on the NYSE closing price since 2017'),
    dcc.Graph(
        id='airline-graph',
        figure = fig
    ),
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
    ], value='2020-01-01'
),
    html.H2('Stock percent change since event occured:'),
    html.Div(id='event_title'),
    html.Div(id='event_graph'),
])

@app.callback(
    [Output('event_title', 'children'),
    Output('event_graph', 'children')],
    [Input('select_event', 'value')])
def callback_a(selected_event):
    if selected_event == '2020-01-21':
        return 'Percentage change since {}'.format(selected_event), dcc.Graph(figure=us_fig)
    elif selected_event == '2020-01-31':
        return 'Percentage change since {}'.format(selected_event), dcc.Graph(figure=ch_block)
    elif selected_event == '2020-02-26':
        return 'Percentage change since {}'.format(selected_event), dcc.Graph(figure=com_spread)
    elif selected_event == '2020-03-04':
        return 'Percentage change since {}'.format(selected_event), dcc.Graph(figure=em_bill)
    elif selected_event == '2020-03-11':
        return 'Percentage change since {}'.format(selected_event), dcc.Graph(figure=eur_ban)
    elif selected_event == '2020-03-13':
        return 'Percentage change since {}'.format(selected_event), dcc.Graph(figure=nat_em)
    elif selected_event == '2020-03-27':
        return 'Percentage change since {}'.format(selected_event), dcc.Graph(figure=ch_block)
    elif selected_event == '2020-04-13':
        return 'Percentage change since {}'.format(selected_event), dcc.Graph(figure=tot_auth)
    else:
        return 'Percentage change since {}'.format(selected_event), dcc.Graph(figure=us_fig)


if __name__ == '__main__':
    app.run_server(debug=True)
