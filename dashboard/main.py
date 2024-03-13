import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from statistics import mode

from dash import Dash, html, dcc, callback, Output, Input, dash_table
from component import get_card_component, get_student_score_list
from utils import get_total_page

PAGE_SIZE = 10

# dash_table set up column 

# load and process the data
df = pd.read_csv('data/guess.csv', sep=";")
#df = pd.read_csv('data/data.csv')

# set average score and row id
df['ID'] = df.index
avg_guess = round(df['Guess'].mean(), 2)
moda_guess = mode(list(df['Guess']))

#top_100_scores = df.sort_values(by='avg_score', ascending=False).head(100).to_dict('records')


#initialize app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# create color palette
color_discrete_sequence = ['#0a9396','#94d2bd','#e9d8a6','#ee9b00', '#ca6702', '#bb3e03', '#ae2012']


app.layout = html.Div([
    html.H1(children='La Saggezza della Folla', style={'textAlign':'center', 'padding-bottom': '20px'}),
    dbc.Row([
        get_card_component('Risposte Totali', '{:,}'.format(len(df.index))),
        get_card_component('Media', str(avg_guess)),
        get_card_component('Moda', str(moda_guess)),
        
    ]),
    dbc.Row(
        dbc.Col([
            html.H4("Distribuzione risposte"),
            html.Div(
                dcc.Slider(0, 100, 2,
                    value=100,
                    id='my-slider'
                ),
                className ="radio-group",
                style = {'margin-top': '20px'}
            ),
            dcc.Graph(figure={}, id='slider-output-container')
        ])
    ),
    
    
    
], style= {"margin": "50px 50px 50px 50px"})


@callback(
    Output('slider-output-container', 'figure'),
    Input('my-slider', 'value'))

def update_output(value):
    df = pd.read_csv('data/guess.csv', sep=";")
    filtered_df = df[df["ID"]<value]
    return px.histogram(filtered_df, x="Guess", color_discrete_sequence=['#0a9396'])


if __name__ == '__main__':
    app.run(debug=True)