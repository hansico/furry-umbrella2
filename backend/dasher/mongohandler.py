from pymongo import MongoClient
import datetime 

dbclient = MongoClient()
db = dbclient.dash_test

def save_metrics_to_db(dbmetrics):
  projectname = dbmetrics['projectname']
  modelname = dbmetrics['modelname']
  metrics = dbmetrics['metrics']
  #print(projectname,modelname,metrics)
  coll = db.get_collection(projectname+'.'+modelname) # mongo collection
  metrics['timestamp'] = str(datetime.datetime.utcnow())
  id = coll.insert_one(metrics).inserted_id
  return id

def save_model_params_to_db(projectname, modelname, params):
  coll = db.get_collection(projectname+'.models') # mongo collection
  f = coll.find_one({'name':modelname})
  if f != None:
    # TODO
    print("WARNING! Model with that name already exists. Parameters will not be overwritten")
    return 0
  if "name" not in params:
    params["name"] = modelname
  elif params["name"] != modelname:
    # TODO
    print("WARNING! Given modelname does not match the name in params")
  g = coll.insert_one(params).inserted_id
  return g

def loadlatest(projectname, modelname,last_stamp):
  coll = db.get_collection(projectname+'.'+modelname)
  query = coll.find({'timestamp':{'$gt':last_stamp}},{'_id': 0})
  data = []
  for x in query:
    data.append(x)
  print("QUERY  RETURNED :",len(data))
  return data

if __name__ == '__main__':
  pass