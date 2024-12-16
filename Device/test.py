import json
from datetime import datetime


scetuals = []
dd = '["2024-12-16T17:45", [2, "2"], [1, "2"]]'

data = json.loads(dd)
print(data)
if type(data[0]) is str:
    date = data.pop(0)
    date = date.replace("T", " ")
    
    target_datetime = datetime.strptime(date, "%Y-%m-%d %H:%M")
    log = {
        "time":target_datetime,
        "piller":data
        }
    scetuals.append(log)
    print(target_datetime)

while True:
    now = datetime.now()
    i=0
    for scetual in scetuals:
        if now >= scetual["time"]:
            scetuals.pop(i)
            print(scetual["piller"])
        i += 1