import os.path
import sys 

class LearningLogger():
  def __init__(self,logfile):
    self.logfile = self.check_existence(logfile)

  def write_seq(self,dic):
    with open(self.logfile,'a') as f:
      f.write("{")
      f.write(",".join(self.dict_format_iter(dic)))
      f.write("}\n")

  def enclose(self,stri):
    return '"'+str(stri)+'"'

  def dict_format_iter(self,dic):
    it = iter(dic)
    for key in it:
      if isinstance(dic[key],str):
        val = self.enclose(dic[key])
      else:
        val = str(dic[key])
      yield self.enclose(key)+":"+val

  def check_existence(self,logfile):
    """If logfile exists"""
    # TODO re-evaluate the logic
    if os.path.isfile(logfile):
      allowed = ['n','y','']
      uans = input("The logfile already exists. Do you wish to proceed? [y/N]")
      if uans not in allowed:
        print("Bad request.")
        self.check_existence(logfile)
      if uans == 'y':
        return logfile
      if uans == 'n':
        sys.exit("User terminated program: Logfile already exists.")
    return logfile

if __name__ == '__main__':
  llg = LearningLogger('./logfile.jsonl')
  llg.write_seq({'epoch':1,'acc':2,'dummy':6,'new':"cool"})
