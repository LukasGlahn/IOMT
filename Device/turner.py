from motor import Motore
import json
from datetime import datetime
moter = Motore()
#print("begin")


scetuals = []
dd = '["2024-12-16T17:45", [2, "2"], [1, "2"]]'

data = json.loads(dd)
#print(data)
if type(data[0]) is str:
    date = data.pop(0)
    date = date.replace("T", " ")
    
    target_datetime = datetime.strptime(date, "%Y-%m-%d %H:%M")
    log = {
        "time":target_datetime,
        "piller":data
        }


def turn(pills):
    print(pills)
    


turn(log["piller"])