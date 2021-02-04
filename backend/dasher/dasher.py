import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from dasher.mongohandler import db_testdump


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

      dcc.Graph(
          id='example-graph-2',
          figure=fig
      ),
      dcc.Interval(
        id='interval-component',
        interval=1000, #(ms)
        n_intervals = 0 
      )
  ])
  init_callbacks(dash_app)
  return dash_app.server

def reformatdata(data,newdata):
  for row in newdata:
    for key in row:
      if key in data:
        print(key)
        if isinstance(data[key],list):
          data[key].append(row[key])
  return data

def init_callbacks(dash_app):
  import random
  @dash_app.callback(Output('example-graph-2','figure'),
                Input('interval-component','n_intervals'))
  def updateGraph(n):
    dump = db_testdump()
    data = {
      'epoch':[],
      'accuracy':[],
      #'loss':[]
    }
    data = reformatdata(data,dump)
    print(data)
    fig = px.line(data,x='epoch',y='accuracy')
    #fig.update_traces(mode='lines+markers')
    return fig
