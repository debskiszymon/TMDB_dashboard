from dash_html_components.Div import Div
import pandas as pd
import datetime as dt
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objects as go


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, 
    external_stylesheets=external_stylesheets, 
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
    )
server = app.server

df_genre = pd.read_csv('df_movies_genre.csv')
df_dash = pd.read_csv('df_movies_dash.csv')

def graph_pull(df):
    pull = []
    for _ in df.groupby('genre'):
        pull.append(0.1)

    for index, element in enumerate(pull):
        if index % 2 == 0:
            pull[index] = element * 3

    return pull

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

def year_list(df):
    year = list(df['release_year'].unique())
    return year


def mark_values(df):
    year_list = list(df['release_year'].unique())
    marks = []
    for _ in range(0, (year_list[0] - year_list[-1]) // 10 + 1 ):
        marks.append(year_list[-1] + (10 * _))
    marks.append(year_list[0])
    return marks

app.layout = html.Div([
    html.Div([
    html.H1('TMDB Movies dashboard',style={'text-align':'center'})],
    className='row'),
    html.Div([
        html.Div([dcc.Graph(
            id='fig1')],
            className='six columns'),
        html.Div([dcc.Graph(
            id='fig2')],
            className='six columns')],
            style={'padding-bottom':'5%'},
            className='row'),
    html.Div([
        dcc.RangeSlider(
            id='the_year',
            min = year_list(df_genre)[-1], 
            max= year_list(df_genre)[0],
            value=[year_list(df_genre)[-1], year_list(df_genre)[0]],
            marks={int(i) : {"label": str(i), "style": {"transform": "rotate(45deg)", 'font-size':'14px', 'opacity':'0.9'}} for i in mark_values(df_genre)},
            tooltip={'always_visible':'True', 'placement':'top'})], 
        className='row')], 
    className='ten columns offset-by-one')


# ------------------------
@app.callback(
    Output('fig1', 'figure'),
    [Input('the_year', 'value')]
)

def update_fig1(year_chosen):
    dff_genre = df_genre[(df_genre['release_year']>=year_chosen[0])&(df_genre['release_year']<=year_chosen[1])]

    grouped = dff_genre.groupby('genre').vote_average.mean()
    fig1 = go.Figure(data=[go.Pie(labels=grouped.index, 
                              values=grouped.values, 
                              texttemplate = "%{label} %{value:.1f}", 
                              pull=graph_pull(df_genre))])


    fig1.update_traces(marker=dict(colors=colors, 
                            line=dict(color='rgb(0,0,0)', 
                            width=1)), 
                            hoverinfo='label+percent', 
                            textfont_size=11, 
                            textposition='inside')
    fig1.update_layout(
        height=600,
    title='Average vote score by Genre')

    return fig1

    # ------------------------

@app.callback(
    Output('fig2', 'figure'),
    [Input('the_year', 'value')]
)

def update_fig2(year_chosen):
    dff_dash = df_dash[(df_dash['release_year']>=year_chosen[0])&(df_dash['release_year']<=year_chosen[1])]

    fig2 = go.Figure([go.Bar(x=dff_dash.nlargest(10, 'vote_count').original_title, 
                            y=dff_dash.nlargest(10, 'vote_count').vote_count)])

    fig2.update_traces(marker_color=colors, 
                    marker_line_color='rgb(0,0,0)',
                    marker_line_width=1)

    fig2.update_layout(
        height=600,
    title='Top 10 Movies with highest vote count',
    showlegend=False)

    return fig2

@app.callback(
    dash.dependencies.Output('year_selected', 'children'),
    [dash.dependencies.Input('the_year', 'value')])

def update_output(year_chosen):
    return 'Years selected {year1} to {year2}'.format(year1= year_chosen[0], year2=year_chosen[1])

if __name__ == '__main__':
    app.run_server()

