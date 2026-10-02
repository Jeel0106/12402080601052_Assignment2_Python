import os
import pandas as pd
import matplotlib.pyplot as plt

def clean(name):
    d=pd.read_csv(name)
    for c in d.columns[2:]:
        d[c]=pd.to_numeric(d[c],errors="coerce"); d[c]=d[c].fillna(d[c].mean())
    return d

def main():
    try:
        name= input().strip(); folder=input().strip(); os.makedirs(folder,exist_ok=True); d=clean(name)
        d.to_csv(os.path.join(folder,"cleaned_marks.csv"),index=False)
        subjects=d.columns[2:]; rows=[]
        for s in subjects: rows.append({"subject":s,"average":d[s].mean(),"minimum":d[s].min(),"maximum":d[s].max()})
        pd.DataFrame(rows).to_csv(os.path.join(folder,"summary.csv"),index=False)
        marks=[x for s in subjects for x in d[s]]; grades={"A":0,"B":0,"C":0,"D":0,"F":0}
        for x in marks:
            g="A" if x>=90 else "B" if x>=80 else "C" if x>=70 else "D" if x>=60 else "F"; grades[g]+=1
        plt.figure(); plt.bar(grades.keys(),grades.values()); plt.savefig(os.path.join(folder,"grade_distribution.png")); plt.close()
        plt.figure(); plt.bar(subjects,[d[s].mean() for s in subjects]); plt.savefig(os.path.join(folder,"subject_average.png")); plt.close()
        d["total"]=d[subjects].sum(axis=1); top=d.sort_values("total",ascending=False).head(10); plt.figure(); plt.bar(top["name"],top["total"]); plt.xticks(rotation=45); plt.tight_layout(); plt.savefig(os.path.join(folder,"top_performers.png")); plt.close()
        print("cleaned_marks.csv"); print("summary.csv"); print("grade_distribution.png"); print("subject_average.png"); print("top_performers.png")
    except Exception as e: print("ERROR:",e)

if __name__=="__main__": main()
