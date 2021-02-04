from pymongo import MongoClient

dbclient = MongoClient()
db = dbclient.dash_test

def insert_to_db(object):
  id = db.test.insert_one(object).inserted_id
  return id

def push_dummydata():
  print(insert_to_db({'Epoch':1,'Accuracy':0.3}))
  print(insert_to_db({'Epoch':2,'Accuracy':0.56}))
  print(insert_to_db({'Epoch':3,'Accuracy':0.78}))
  print(insert_to_db({'Epoch':4,'Accuracy':0.84}))
  print(insert_to_db({'Epoch':5,'Accuracy':0.88}))

def db_dump():
  dump = []
  #'Epoch':{'$gte':4}
  for x in db.test.find({},{'_id':0}):
    dump.append(x)
  return dump

if __name__ == '__main__':
  #db_dump()
  pass