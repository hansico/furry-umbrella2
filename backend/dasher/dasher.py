import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
from dasher.mongohandler import loadlatest
import datetime
import json

def init_dashapp(server):
  external_stylesheets = None
  dash_app = dash.Dash(
    server=server,
    routes_pathname_prefix='/plot/',
    external_stylesheets=external_stylesheets
    )

  colors = {
      'background': '#F5F5F5',
      'text': '#0A1A1E'
  }
  fig = px.line()
  fig.update_layout(
      plot_bgcolor=colors['background'],
      paper_bgcolor=colors['background'],
      font_color=colors['text']
  )

  dash_app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
      html.H1(
          children='Hello Dash',
          style={
              'textAlign': 'center',
              'color': colors['text']
          }
      ),

      html.Div(children='Dash: A web application framework for Python.', style={
          'textAlign': 'center',
          'color': colors['text']
      }),
      html.P(children=datetime.datetime.min,id='hackylatestepoch'),
      html.P(children="",id='dummy', style={
        'display' : 'none'
      }),
      html.Div(
        style={'display':'flex'},
        children = [
          dcc.Graph(
            id='example-graph-2',
            figure=fig,
            style={'flex':1}
          ),
          dcc.Graph(
            id='graph-2',
            figure=fig,
            style={'flex':1}
        )],
      ),
      dcc.Interval(
        id='interval-component',
        interval=1000, #(ms)
        n_intervals = 0,
      )
  ])
  init_callbacks(dash_app)
  return dash_app.server

def refo(datastring):
  rows = datastring.split('£')
  data = {}
  for row in rows:
    q = json.loads(row.replace("'",'"'))
    for key in q:
      if key in data:
        data[key].append(q[key])
      else:
        data[key] = [q[key]]
  return data

def ndjson_to_string(ndjson):
  return "£".join([str(x) for x in ndjson])

def init_callbacks(dash_app):

  @dash_app.callback(Output('example-graph-2','figure'),
                #Input('interval-component','n_intervals'))
                Input('dummy','children'))
  def updateGraph(datax):
    data = refo(datax)
    fig = px.line(data,x='epoch',y='accuracy')
    return fig
  
  @dash_app.callback(Output('graph-2','figure'),
                #Input('interval-component','n_intervals'))
                Input('dummy','children'))
  def updateGraph(datax):
    data = refo(datax)
    fig = px.line(data,x='epoch',y='loss')
    return fig

  @dash_app.callback(Output('hackylatestepoch','children'),
                Output('dummy','children'),
                [Input('interval-component','n_intervals')],
                [State('hackylatestepoch','children')],
                [State('dummy','children')])
  def lateststamp(n,text,whole):
    laststamp = loadlatest("test","tbob",text)
    if laststamp:
      if whole:
        strin = whole+"£"+ndjson_to_string(laststamp)
      else:
        strin = ndjson_to_string(laststamp)
      return laststamp[-1]['timestamp'], strin
    else:
      # prevent update
      raise dash.exceptions.PreventUpdate