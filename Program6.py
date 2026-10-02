import re
from collections import defaultdict,deque

def minutes(t):
    h,m=map(int,t.split(":")); return h*60+m

def main():
    try:
        x,t=map(int,input().split()); n=int(input()); failed=defaultdict(deque); found={}
        pattern=r"^\d{2}:\d{2}\s+\S+\s+\S+\s+(FAIL|SUCCESS)$"
        for _ in range(n):
            line=input().strip()
            if not re.fullmatch(pattern,line): continue
            time,user,ip,status=line.split(); now=minutes(time)
            while failed[user] and now-failed[user][0][0]>t: failed[user].popleft()
            if status=="FAIL": failed[user].append((now,ip))
            else:
                different=any(oldip!=ip for _,oldip in failed[user])
                if len(failed[user])>=x and different and user not in found: found[user]=time
                failed[user].clear()
        for user in sorted(found): print(user,found[user])
    except Exception: print("ERROR")

if __name__=="__main__": main()
