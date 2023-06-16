import datetime

class DateHelper:

    def __init__(self):
        self.x = datetime.datetime.now()
    
    def year(self):
        return str(self.x.year)

    def month(self):
        return str(self.x.month) + '_' + self.x.strftime("%b")

    def day(self):
        return str(self.x.day) + '_' + self.x.strftime("%a")

    def localdir(self):
        dir = self.x.strftime("%Y%m%d")
        return dir

    def expirydate(self, retention_time):
        exp_date = self.x - datetime.timedelta(days=retention_time)
        return exp_date.strftime('%Y-%m-%dT%H:%M:%S')
        
if __name__ == '__main__':
    dh = DateHelper()
    print('Local dir ' + dh.localdir())
    print('Year ' + dh.year())
    print('Month ' + dh.month())
    print('Day ' + dh.day())
    
