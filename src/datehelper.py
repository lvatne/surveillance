import datetime

class DateHelper:

    
    def year(self):
        x = datetime.datetime.now()
        return str(x.year)

    def month(self):
        x = datetime.datetime.now()
        return str(x.month) + '_' + x.strftime("%b")

    def day(self):
        x = datetime.datetime.now()
        return str(x.day) + '_' + x.strftime("%a")

        
if __name__ == '__main__':
    dh = DateHelper()
    print('Year ' + dh.year())
    print('Month ' + dh.month())
    print('Day ' + dh.day())
    
