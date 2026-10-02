import json

cols={"student.id":"s.id","student.name":"s.name","student.spi":"s.spi","course.id":"c.id","course.name":"c.name","registration.student_id":"r.student_id","registration.course_id":"r.course_id"}

def main():
    try:
        d=json.loads(input()); limit=int(d.get("limit",10))
        if not 1<=limit<=1000: print("INVALID_LIMIT"); return
        selected=[]
        for c in d["columns"]:
            if c not in cols: print("INVALID_COLUMN"); return
            selected.append(cols[c])
        sql="SELECT "+", ".join(selected)+" FROM Student s JOIN CourseRegistration r ON s.id=r.student_id JOIN Course c ON r.course_id=c.id"
        params=[]; where=[]
        for item in d.get("where",[]):
            c=item["column"]; op=item["operator"]
            if c not in cols: print("INVALID_COLUMN"); return
            if op not in ["=",">","<",">=","<=","LIKE"]: print("INVALID_OPERATOR"); return
            where.append(cols[c]+" "+op+" %s"); params.append(item["value"])
        if where: sql+=" WHERE "+" AND ".join(where)
        order=d.get("order","")
        if order:
            x=order.split(); c=x[0]; direction=x[1] if len(x)>1 else "ASC"
            if c not in cols: print("INVALID_COLUMN"); return
            if direction not in ["ASC","DESC"]: print("INVALID_ORDER"); return
            sql+=" ORDER BY "+cols[c]+" "+direction
        sql+=" LIMIT %s"; params.append(limit)
        print("SQL_OK"); print(sql); print("PARAMETERS",params)
    except Exception: print("INVALID")

if __name__=="__main__": main()
