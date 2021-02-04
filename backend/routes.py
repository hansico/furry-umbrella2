from flask import render_template, request 
from flask import current_app as app 
from dasher import mongohandler

@app.route('/')
def index():
  return "Replace with index page"

@app.route('/api/post', methods=['POST'])
def add_to_db():
  #print(request.json)
  print(mongohandler.insert_to_db(request.json))
  return "Success",200
