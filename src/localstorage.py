import survprop
import datehelper

class LocalStorage:
    def __init__(self):
          myProps = survprop.SurvProp()
          self.local_path = myProps.local_alarm_path

    def current_dir(self):
        dh = datehelper.DateHelper()
        dir = self.local_path + '/' + dh.localdir() + '/images'
        return dir
        
        

if __name__ == '__main__':
  myLs = LocalStorage()
  print(myLs.current_dir())
