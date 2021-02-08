from pymongo import MongoClient
import datetime 

dbclient = MongoClient('mongodb://localhost:27001/')

def get_projects():
  exclude = set(['admin','local','config'])
  dbs = set(dbclient.list_database_names())
  return list(dbs-exclude)

def get_collections(projectname):
  db = dbclient.get_database(name=projectname)
  colls = db.list_collection_names()
  return [coll.split('.')[0] for coll in colls] 

def save_metrics_to_db(dbmetrics):
  projectname = dbmetrics['projectname']
  modelname = dbmetrics['modelname']
  metrics = dbmetrics['metrics']

  db = dbclient.get_database(name=projectname)
  coll = db.get_collection(modelname+'.metrics') # mongo collection
  metrics['timestamp'] = str(datetime.datetime.utcnow())
  id = coll.insert_one(metrics).inserted_id
  print(id)
  if id:
    return True
  else:
    return False

def loadlatest(projectname, modelname,last_stamp):
  db = dbclient.get_database(name=projectname)
  coll = db.get_collection(modelname+'.metrics')
  query = coll.find({'timestamp':{'$gt':str(last_stamp)}},{'_id': 0})
  data = []
  for x in query:
    data.append(x)
  print("QUERY  RETURNED :",len(data))
  return data

if __name__ == '__main__':
  print(get_projects())
  print(get_collections('test'))