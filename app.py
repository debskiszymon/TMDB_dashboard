import pandas as pd
import datetime as dt
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# import dash_auth
import plotly.graph_objects as go
# import tab1
# import tab2
# import tab3
# import dash_auth

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df_genre = pd.read_csv('df_movies_genre.csv')
df_dash = pd.read_csv('df_movies_dash.csv')

pull = []
for _ in df_genre.groupby('genre'):
    pull.append(0.1)

for index, element in enumerate(pull):
    if index % 2 == 0:
        pull[index] = element * 3

colors = ['rgb(190, 219, 57)',
'rgb(157, 213, 67)',
'rgb(123, 207, 78)',
'rgb(85, 199, 90)',
'rgb(30, 191, 101)',
'rgb(0, 182, 112)',
'rgb(0, 173, 123)',
'rgb(0, 163, 132)',
'rgb(0, 153, 139)',
'rgb(0, 142, 145)',
'rgb(0, 132, 149)',
'rgb(0, 121, 150)',
'rgb(0, 110, 149)',
'rgb(0, 99, 145)',
'rgb(0, 88, 140)',
'rgb(0, 77, 132)',
'rgb(0, 66, 122)',
'rgb(0, 55, 110)',
'rgb(0, 45, 97)',
'rgb(0, 34, 83)']


grouped = df_genre.groupby('genre').vote_average.mean()
fig1 = go.Figure(data=[go.Pie(labels=grouped.index, 
                              values=grouped.values, 
                              texttemplate = "%{label}: %{value:.1f}", 
                              pull=pull)])


fig1.update_traces(marker=dict(colors=colors, 
                           line=dict(color='rgb(0,0,0)', 
                           width=1)), 
                           hoverinfo='label+percent', 
                           textfont_size=11, 
                           textposition='inside')
fig1.update_layout(
    autosize=False,
    width=1000,
    height=800,
title='Average votes by Genre')

fig2 = go.Figure([go.Bar(x=df_dash.nlargest(10, 'vote_count').original_title, 
                        y=df_dash.nlargest(10, 'vote_count').vote_count)])

fig2.update_traces(marker_color=colors, 
                  marker_line_color='rgb(0,0,0)',
                  marker_line_width=1)

fig2.update_layout(
    autosize=False,
    width=1000,
    height=600,
title='Highest vote count')

app.layout = html.Div(children=[
    html.H1(children='TMDB Movies',style={'text-align':'center'}),
    html.Div(children=[
        dcc.Graph(
        id='fig1',
        figure=fig1,
        style={'width':'50%'}
    ),
        dcc.Graph(
        id='fig2',
        figure=fig2,
        style={'width':'50%'}
        )
    ], style={'display':'flex'}),
    html.Div([
    dcc.Slider(
        id='slider-updatemode',
        # marks={i: '{}'.format(10 ** i) for i in range(4)},
        min = df_genre.release_year.min(), 
        max= df_genre.release_year.max(),
        value=[df_genre.release_year.min(), df_genre.release_year.max()],
        step=1,
        # updatemode='drag'
    ),
    html.Div(id='updatemode-output-container', style={'margin-top': 20})
])
    ])




if __name__ == '__main__':
    app.run_server()

