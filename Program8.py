MOD=1000000007
INF=-10**30

def main():
    try:
        n,m=map(int,input().split()); ps=[INF]*m; pc=[0]*m
        for i in range(n):
            row=input().split(); cs=[INF]*m; cc=[0]*m
            for j in range(m):
                if row[j]=="X": continue
                value=int(row[j])
                if i==0 and j==0: cs[j]=value; cc[j]=1; continue
                best=INF; count=0
                for score,num in ([cs[j-1],cc[j-1]] if j>0 else [INF,0],[ps[j],pc[j]],[ps[j-1],pc[j-1]] if j>0 else [INF,0]):
                    if score>best: best=score; count=num
                    elif score==best and score!=INF: count=(count+num)%MOD
                if best!=INF: cs[j]=best+value; cc[j]=count
            ps,pc=cs,cc
        print("IMPOSSIBLE" if ps[m-1]==INF else str(ps[m-1])+" "+str(pc[m-1]))
    except Exception: print("ERROR")

if __name__=="__main__": main()
