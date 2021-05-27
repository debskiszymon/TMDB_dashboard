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
# year_list = list(year)
# year_keys = [int(i) for i in list(year)[::3]]
# year_values = [str(i) for i in list(year)[::3]]
# zip_iterator = zip(year_keys, year_values)
# year_dict = dict(zip_iterator)

# mark_values = year_dict

# grouped = df_genre.groupby('genre').vote_average.mean()
# fig1 = go.Figure(data=[go.Pie(labels=grouped.index, 
#                               values=grouped.values, 
#                               texttemplate = "%{label}: %{value:.1f}", 
#                               pull=pull)])


# fig1.update_traces(marker=dict(colors=colors, 
#                            line=dict(color='rgb(0,0,0)', 
#                            width=1)), 
#                            hoverinfo='label+percent', 
#                            textfont_size=11, 
#                            textposition='inside')
# fig1.update_layout(
#     autosize=False,
#     width=1000,
#     height=800,
# title='Average votes by Genre')

# fig2 = go.Figure([go.Bar(x=df_dash.nlargest(10, 'vote_count').original_title, 
#                         y=df_dash.nlargest(10, 'vote_count').vote_count)])

# fig2.update_traces(marker_color=colors, 
#                   marker_line_color='rgb(0,0,0)',
#                   marker_line_width=1)

# fig2.update_layout(
#     autosize=False,
#     width=1000,
#     height=600,
# title='Highest vote count')



app.layout = html.Div(children=[
    html.H1(children='TMDB Movies',style={'text-align':'center'}),
    html.Div(children=[
        dcc.Graph(
        id='fig1',
        # figure=fig1,
        style={'width':'40%'}
    ),
        dcc.Graph(
        id='fig2',
        # figure=fig2,
        style={'width':'40%', "margin-left": "80px"}
        )
    ], style={'display':'flex'}),
    # html.Div(id='year_selected', style={'padding-left': '5%'}),
    html.Div([
        dcc.RangeSlider(
            id='the_year',
            # marks={i: '{}'.format(10 ** i) for i in range(4)},
            min = year_list(df_genre)[-1], 
            max= year_list(df_genre)[0],
            value=[year_list(df_genre)[-1], year_list(df_genre)[0]],
            # dots=True,
            # marks= mark_values,
            # marks={i : {'label' : str(year_list[i]), 'style':{'transform':'rotate(-90deg)'}} for i in range(0, len(year_list)-1)},
            # marks={each : {'label': year, 'style': {'transform': 'rotate(45deg)'}} for each, year in enumerate(year_dict)},
            marks={int(i) : {"label": str(i), "style": {"transform": "rotate(45deg)", 'font-size':'11px', 'opacity':'0.8'}} for i in year_list(df_genre)[::2]},
            tooltip={'always_visible':'True', 'placement':'top'}
            # step=1
        )], 
        style={'width': '90%','padding-left':'5%', 'padding-right':'5%'})
        # html.Div(id='year_selected')
    ])


# ------------------------
@app.callback(
    Output('fig1', 'figure'),
    [Input('the_year', 'value')]
)

def update_fig1(year_chosen):
    # print(year_chosen)
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
        autosize=False,
        width=1000,
        height=800,
    title='Average votes by Genre')

    return fig1

    # ------------------------

@app.callback(
    Output('fig2', 'figure'),
    [Input('the_year', 'value')]
)

def update_fig2(year_chosen):
    # print(year_chosen)
    dff_dash = df_dash[(df_dash['release_year']>=year_chosen[0])&(df_dash['release_year']<=year_chosen[1])]

    fig2 = go.Figure([go.Bar(x=dff_dash.nlargest(10, 'vote_count').original_title, 
                            y=dff_dash.nlargest(10, 'vote_count').vote_count)])

    fig2.update_traces(marker_color=colors, 
                    marker_line_color='rgb(0,0,0)',
                    marker_line_width=1)

    fig2.update_layout(
        autosize=False,
        width=1000,
        height=600,
    title='Highest vote count')

    return fig2

@app.callback(
#     Output('years_selected', 'figure'),
#     [Input('the_year', 'value')]
# )
    dash.dependencies.Output('year_selected', 'children'),
    [dash.dependencies.Input('the_year', 'value')])

def update_output(year_chosen):
    return 'Years selected {year1} to {year2}'.format(year1= year_chosen[0], year2=year_chosen[1])

if __name__ == '__main__':
    app.run_server()

