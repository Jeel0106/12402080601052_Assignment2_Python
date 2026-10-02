class Product:
    def __init__(self,pid,name,stock,purchase,selling): self.product_id=pid; self.name=name; self.stock=stock; self.purchase=purchase; self.selling=selling
    def value(self): return self.stock*self.purchase

class Inventory:
    def __init__(self): self.products={}
    def add(self,p): self.products[p.product_id]=p
    def delete(self,pid):
        if pid in self.products: del self.products[pid]; print("DELETED",pid)
        else: print("NOT_FOUND",pid)
    def update(self,pid,stock):
        if pid in self.products: self.products[pid].stock=stock; print("UPDATED",pid)
        else: print("NOT_FOUND",pid)
    def total(self): return sum(p.value() for p in self.products.values())
    def __add__(self,other):
        r=Inventory()
        for p in list(self.products.values())+list(other.products.values()):
            if p.product_id not in r.products: r.add(Product(p.product_id,p.name,p.stock,p.purchase,p.selling))
            else:
                q=r.products[p.product_id]; q.stock+=p.stock; q.purchase=min(q.purchase,p.purchase); q.selling=max(q.selling,p.selling)
        return r
    def __lt__(self,other): return self.total()<other.total()

def load(name):
    inv=Inventory()
    with open(name) as f:
        for line in f:
            a=line.split()
            if len(a)==5: inv.add(Product(a[0],a[1],int(a[2]),float(a[3]),float(a[4])))
    return inv

def main():
    try:
        a=load(input().strip()); b=load(input().strip()); q=int(input())
        for _ in range(q):
            c=input().split()
            if c[0]=="ADD": (a if c[1]=="A" else b).add(Product(c[2],c[3],int(c[4]),float(c[5]),float(c[6]))); print("ADDED",c[2])
            elif c[0]=="DELETE": (a if c[1]=="A" else b).delete(c[2])
            elif c[0]=="UPDATE": (a if c[1]=="A" else b).update(c[2],int(c[3]))
            elif c[0]=="MERGE":
                for pid,p in sorted((a+b).products.items()): print(pid,p.name,"stock="+str(p.stock),"purchase="+format(p.purchase,".2f"),"selling="+format(p.selling,".2f"))
            elif c[0]=="COMPARE": print("A_LESS" if a<b else "A_GREATER" if b<a else "EQUAL")
    except Exception: print("ERROR")

if __name__=="__main__": main()
