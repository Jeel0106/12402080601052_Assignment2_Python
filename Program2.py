import re

def price(value):
    m=re.search(r"\d+(?:\.\d+)?",value.replace(",",""))
    if not m: return None
    x=float(m.group())
    return int(x) if x.is_integer() else x

def read_page(name):
    with open(name,"r",encoding="utf-8",errors="ignore") as f: text=f.read()
    blocks=re.findall(r'<div[^>]*class=["\']product["\'][^>]*>(.*?)</div>',text,re.I|re.S)
    result=[]
    for block in blocks:
        a=re.search(r'class=["\']name["\'][^>]*>(.*?)<',block,re.I|re.S)
        b=re.search(r'class=["\']price["\'][^>]*>(.*?)<',block,re.I|re.S)
        c=re.search(r'class=["\']rating["\'][^>]*>(.*?)<',block,re.I|re.S)
        if a and b and c:
            q=price(b.group(1)); r=re.search(r"\d+(?:\.\d+)?",c.group(1))
            if q is not None and r: result.append((re.sub(r'<.*?>','',a.group(1)).strip(),q,float(r.group())))
    return result

def main():
    try:
        p,k=map(int,input().split()); products={}
        for _ in range(p):
            for item in read_page(input().strip()):
                if item[0] not in products or item[2]>products[item[0]][2]: products[item[0]]=item
        result=sorted(products.values(),key=lambda x:(-x[2],x[1],x[0]))
        for x in result[:k]: print(x[0],x[1],x[2])
    except Exception: print("ERROR")

if __name__=="__main__": main()
