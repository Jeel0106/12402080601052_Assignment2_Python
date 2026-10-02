import csv
import mysql.connector

def main():
    try:
        host=input("Host: "); user=input("User: "); password=input("Password: "); database=input("Database: ")
        db=mysql.connector.connect(host=host,user=user,password=password,database=database)
        cur=db.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Student(student_id VARCHAR(20) PRIMARY KEY,name VARCHAR(100),spi FLOAT)")
        cur.execute("CREATE TABLE IF NOT EXISTS CourseRegistration(student_id VARCHAR(20),course_id VARCHAR(20),FOREIGN KEY(student_id) REFERENCES Student(student_id))")
        with open(input("Student CSV: "),newline="") as f:
            for r in csv.DictReader(f):
                cur.execute("INSERT INTO Student(student_id,name,spi) VALUES(%s,%s,%s) ON DUPLICATE KEY UPDATE name=%s,spi=%s",(r["student_id"],r["name"],float(r["spi"]),r["name"],float(r["spi"])))
        with open(input("Registration CSV: "),newline="") as f:
            for r in csv.DictReader(f): cur.execute("INSERT INTO CourseRegistration(student_id,course_id) VALUES(%s,%s)",(r["student_id"],r["course_id"]))
        db.commit()
        course=input("Course ID: "); threshold=float(input("SPI threshold: "))
        cur.execute("SELECT s.student_id,s.name,s.spi,r.course_id FROM Student s JOIN CourseRegistration r ON s.student_id=r.student_id WHERE r.course_id=%s AND s.spi>%s ORDER BY s.spi DESC,s.student_id ASC",(course,threshold))
        for r in cur: print(*r)
        cur.close(); db.close()
    except Exception as e: print("Database error:",e)

if __name__=="__main__": main()
