from pymongo import MongoClient

dbclient = MongoClient()
db = dbclient.dash_test

def save_metrics_to_db(projectname, modelname, metrics):
  coll = db.get_collection(projectname+'.'+modelname) # mongo collection
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

def push_dummydata():
  print(save_metrics_to_db("testproject","testcol",{'epoch':1,'accuracy':0.3}))
  print(save_metrics_to_db("testproject","testcol",{'epoch':2,'accuracy':0.56}))
  print(save_metrics_to_db("testproject","testcol",{'epoch':3,'accuracy':0.76}))
  print(save_metrics_to_db("testproject","testcol",{'epoch':4,'accuracy':0.84}))
  print(save_metrics_to_db("testproject","testcol",{'epoch':5,'accuracy':0.89}))

def db_testdump():
  dump = []
  #'Epoch':{'$gte':4}
  for x in db.testproject.testcol.find({},{'_id':0}):
    dump.append(x)
    #print(x)
  return dump

if __name__ == '__main__':
  #db_dump()
  #save_model_params_to_db("super","JANK",{'pid':9})
  #push_dummydata()
  pass