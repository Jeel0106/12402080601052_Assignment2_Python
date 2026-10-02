import re
from collections import defaultdict

def main():
    try:
        file_name=input().strip()
        pattern=r"[A-Za-z0-9+._-]+@[A-Za-z0-9.-]+\.(?:com|edu|org)\b"
        emails=set()
        with open(file_name,"r",encoding="utf-8",errors="ignore") as file:
            for line in file:
                for email in re.findall(pattern,line,re.I):
                    if email.count("@")==1:
                        emails.add(email.lower())
        domains=defaultdict(list)
        for email in emails: domains[email.split("@")[1]].append(email)
        for domain in sorted(domains):
            print(domain,len(domains[domain]),min(domains[domain]))
    except Exception:
        print("ERROR")

if __name__=="__main__": main()
