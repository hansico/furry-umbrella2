import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
from dasher.mongohandler import loadlatest, get_projects, get_collections
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
  projects = get_projects()
  projects_options = [{"label":x,"value":x} for x in projects]
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
      html.P(children="",id='hackylatestepoch'),
      html.P(children="",id='dummy', style={
        'display' : 'none'
      }),
      dcc.Dropdown(
        id="projectselector",
        options=projects_options,
        multi=False,
      ),
      dcc.Dropdown(
        id="modelselector",
        options=[],
        multi=True,
      ),
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
        disabled=False,
      )
  ])
  init_callbacks(dash_app)
  return dash_app.server

def refo(models,datax):
  datax = json.loads(datax)
  data = {}
  for model in models:
    if model not in data:
      data[model] = {}
    for row in datax[model]:
      for key in row:
        if key not in data[model]:
          data[model][key] = []
        data[model][key].append(row[key])
  return data

def ndjson_to_string(ndjson):
  return "£".join([str(x) for x in ndjson])

def init_callbacks(dash_app):
  
  @dash_app.callback(Output('projectselector','options'),
                [Input('projectselector','value')],
                [State('projectselector','value')])
  def update_project_dropdown(search_value,value):
    projects = get_projects()
    projects = [{"label":x,"value":x} for x in projects]
    return projects
  
  @dash_app.callback(Output('modelselector','options'),
                Input('projectselector','value'))
  def update_model_selector(project):
    if project:
      models = get_collections(project)
      return [{"label":m,"value":m} for m in models]
    else:
      raise dash.exceptions.PreventUpdate

  @dash_app.callback(Output('example-graph-2','figure'),
                [Input('dummy','children')],
                [Input('modelselector','value')],
                )
  def updateGraph1(datax,models):
    if not models:
      return px.line()
    fig = px.line()
    data = refo(models,datax)
    for model in models:
      fig.append_trace({
        'x' : data[model]['epoch'],
        'y' : [float(y) for y in data[model]['accuracy']],
        'name': model+'_acc',
        },1,1)
    fig.update_layout(
      xaxis_title = 'Epoch',
      yaxis_title = 'Accuracy',
    )
    return fig
  
  @dash_app.callback(Output('graph-2','figure'),
                [Input('dummy','children')],
                [Input('modelselector','value')])
  def updateGraph2(datax,models):
    if not models:
      return px.line()
    fig = px.line()
    data = refo(models,datax)
    for model in models:
      fig.append_trace({
        'x' : data[model]['epoch'],
        'y' : [float(y) for y in data[model]['loss']],
        'name' : model+'_loss'
      },1,1)
    fig.update_layout(
      xaxis_title = 'Epoch',
      yaxis_title = 'Loss',
    )
    return fig
  
  @dash_app.callback(Output('hackylatestepoch','children'),
                Output('dummy','children'),
                [Input('interval-component','n_intervals')],
                [Input('modelselector','value')],
                [State('projectselector','value')],
                [State('hackylatestepoch','children')],
                [State('dummy','children')])
  def lateststamp(n,models,project,timestamps,storage):
    if not models:
      raise dash.exceptions.PreventUpdate
    
    updateflag = False

    if not timestamps:
      timestamps = {}
    else:
      timestamps = json.loads(timestamps)
    
    if not storage:
      storage = {}
    else:
      storage = json.loads(storage)
    
    for model in models:
      if model not in timestamps:
        timestamps[model] = str(datetime.datetime.min)
      updates = loadlatest(project,model,timestamps[model])
      
      if updates:
        timestamps[model] = str(updates[-1]['timestamp'])
        updateflag = True

      if model not in storage:
        storage[model] = []
      storage[model].extend(updates)

    if not updateflag:
      raise dash.exceptions.PreventUpdate
    
    return json.dumps(timestamps), json.dumps(storage)