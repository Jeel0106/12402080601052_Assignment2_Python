import json
from collections import defaultdict

def records(name):
    with open(name) as f:
        for line in f:
            try:
                d=json.loads(line)
                if "device_id" not in d or "temperature_c" not in d or "humidity" not in d: raise ValueError()
                yield d
            except Exception: yield None

def main():
    try:
        data=defaultdict(list); bad=defaultdict(int)
        for d in records(input().strip()):
            if d is None: bad["all"]+=1; continue
            try: data[d["device_id"]].append(float(d["temperature_c"]))
            except Exception: bad["all"]+=1
        for device in sorted(data):
            v=data[device]; print(device,"count="+str(len(v)),"min="+format(min(v),".2f"),"max="+format(max(v),".2f"),"avg="+format(sum(v)/len(v),".2f"),"corrupted="+str(bad[device]))
        if bad["all"]: print("corrupted_records="+str(bad["all"]))
    except Exception: print("ERROR")

if __name__=="__main__": main()
