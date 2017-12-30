
from datetime import datetime as dt
from datetime import timedelta

class Record:
    
    def __init__(self, record):
        print(record)
        self.tag = record['tag']
        self.value = record['val']
        self.time = record['time']
        try:
            self.tdatetime = dt.strptime(self.time, '%Y.%m.%d %H:%M:%S')
        except:
            self.tdatetime = None

    def __str__(self):
        res = "record -> "
        res += "time:" + self.time
        res += ", tag:" + self.tag 
        res += ", value:" + self.value
        return res

    def is_head(self):
        return self.tag == "start"

    def is_scenario(self):
        return self.tag == "sce"

    def is_location(self):
        return self.tag == "loc"

    def is_care(self):
        return self.tag == "Care"

    def is_tail(self):
        return self.tag == "end"

