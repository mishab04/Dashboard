# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 10:57:51 2019

@author: Abhinav
"""

import os

os.chdir('C:/Users/Abhinav/Documents/My Code/us-oil-and-gas-production-june-2008-to-june-2018')

import pandas as pd
import numpy as np

df = pd.read_csv('U.S._crude_oil_production.csv')

mapbox_access_token

locstates = pd.read_html('https://www.latlong.net/category/states-236-14.html')

locstates = locstates[0]

locstates.columns = locstates.iloc[0]

locstates = locstates[1:]

locstates['Place Name'] = locstates['Place Name'].apply(lambda x: x.split(',')[0])

states = list(df.columns)

states.remove('U.S. Crude Oil ')

states_df = pd.DataFrame({'Place Name': states})

states_df[states_df['Place Name'] == 'Missouri'] = 'Missouri State'

states_final = pd.merge(states_df,locstates, how = 'left', on = ['Place Name'])

states_final.dropna(inplace = True)
site_lat = states_final.Latitude
site_lon = states_final.Longitude
locations_name = states_final['Place Name']

df['Month'] = pd.to_datetime(df['Month'], format = '%Y-%m-%d')
df['year'] = df['Month'].dt.year

yearlist = list(df['year'].unique())

yearstoremove = [2008,2018]

yrs = [ int(i) for i in yearlist if i not in [2008,2018]]

#Creating an app for visulaition
import plotly
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(external_stylesheets=external_stylesheets)

app.layout = html.Div([
        html.Div([html.H3('U.S. Crude Oil production Dashboard')],style = {'width':'100%','float':'left'}),
        html.Div([
        html.Header('Select the year',style={'width':'30%'}),
                html.Div([
                        dcc.RangeSlider(
                                id='page1_range',
                                min = 2009,
                                max = 2017,
                                marks={i:str(i) for i in yrs},
                                value=[2012,2016],
                                step = 1,
                                included=False,
                                allowCross=False
                                )
                        ], style={'width':'40%'}),
        html.Br(),               
        html.Header('Select the State',style={'width':'30%'}),
                html.Div([
                        dcc.Dropdown(
                                id='page1_states',
                                options=[{'label': str(i), 'value': i} for i in states],
                                value=['North Dakota','Texas'],
                                multi = True)
                        ], style={'width':'40%'}),
                        ], style = {'float':'left', 'width':'40%'}),
                html.Div([html.Div([dcc.Graph(id='page1_map',
                                            figure ={
                                                    'data' :[
                                                            go.Scattermapbox(
                                                                    lat=site_lat,
                                                                    lon=site_lon,
                                                                    mode='markers',
                                                                    marker=go.scattermapbox.Marker(
                                                                            size=17,
                                                                            color='rgb(255, 0, 0)',
                                                                            opacity=0.7
                                                                            ),
                                                                    text=locations_name,
                                                                    hoverinfo='text'
                                                                    ),
                                                            go.Scattermapbox(
                                                                    lat=site_lat,
                                                                    lon=site_lon,
                                                                    mode='markers',
                                                                    marker=go.scattermapbox.Marker(
                                                                            size=8,
                                                                            color='rgb(242, 177, 172)',
                                                                            opacity=0.7
                                                                            ),
                                                                            hoverinfo='none'
                                                                            )],
                                                    'layout' :  go.Layout(
                                                            title='US Oil Production States',
                                                            autosize=True,
                                                            hovermode='closest',
                                                            showlegend=False,
                                                            mapbox=go.layout.Mapbox(
                                                                    accesstoken=mapbox_access_token,
                                                                    bearing=0,
                                                                    center=go.layout.mapbox.Center(
                                                                            lat=38,
                                                                            lon=-94
                                                                            ),
                                                                            pitch=0,
                                                                            zoom=3,
                                                                            style='light'
                                                                            ),
                                                                            )
                                                                    }
                    )],style={'width':'35%'}),
            html.Div([dcc.Graph(id = 'mylinechart',
                                figure = {
                                        'data':[
                                                go.Scatter(
                                                        x = df['Month'],
                                                        y  = df['U.S. Crude Oil '],
                                                        mode = 'lines')
                                                ],
                                        'layout': go.Layout(
                                                title = 'U.S. Oil Production')
                                        })],style={'width':'35%'}),
            ],style={'width':'60%','float':'right'}),                                                
    ])


if __name__ == '__main__':
    app.run_server()
