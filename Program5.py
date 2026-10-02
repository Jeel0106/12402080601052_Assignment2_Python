import re
import tkinter as tk
from tkinter import ttk,messagebox
import mysql.connector

class ContactManager:
    def __init__(self,root):
        self.root=root; root.title("Contact Manager"); root.geometry("900x600")
        self.db=mysql.connector.connect(host="localhost",user="root",password="",database="contacts")
        c=self.db.cursor(); c.execute("CREATE TABLE IF NOT EXISTS Contact(id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(100),email VARCHAR(150) UNIQUE,phone VARCHAR(30),category VARCHAR(50),notes TEXT)"); self.db.commit(); c.close()
        self.make_widgets(); self.show()
    def make_widgets(self):
        f=ttk.Frame(self.root); f.pack(pady=10)
        labels=["Name","Email","Phone","Category","Notes"]; self.entries=[]
        for i,label in enumerate(labels):
            ttk.Label(f,text=label).grid(row=i//2,column=(i%2)*2,padx=5,pady=5)
            if label=="Category": e=ttk.Combobox(f,values=["Faculty","Student","Friend","Other"])
            else: e=ttk.Entry(f)
            e.grid(row=i//2,column=(i%2)*2+1,padx=5,pady=5); self.entries.append(e)
        for i,(text,fun) in enumerate([("Add",self.add),("Update",self.update),("Delete",self.delete),("Search",self.search)]): ttk.Button(f,text=text,command=fun).grid(row=3,column=i,pady=10)
        self.search_box=ttk.Entry(self.root); self.search_box.pack()
        self.table=ttk.Treeview(self.root,columns=("id","name","email","phone","category","notes"),show="headings"); self.table.pack(fill="both",expand=True)
        for c in self.table["columns"]: self.table.heading(c,text=c.title())
        self.table.bind("<<TreeviewSelect>>",self.select)
    def valid(self,email): return re.fullmatch(r"^[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",email) is not None
    def values(self): return tuple(x.get().strip() for x in self.entries)
    def add(self):
        try:
            v=self.values()
            if not v[0] or not self.valid(v[1]): raise Exception("Invalid name or email")
            c=self.db.cursor(); c.execute("INSERT INTO Contact(name,email,phone,category,notes) VALUES(%s,%s,%s,%s,%s)",v); self.db.commit(); c.close(); self.show(); messagebox.showinfo("Success","Record inserted")
        except Exception as e: messagebox.showerror("Error",str(e))
    def selected(self):
        s=self.table.selection()
        if not s: raise Exception("Select a contact")
        return self.table.item(s[0],"values")[0]
    def update(self):
        try:
            v=self.values()
            if not self.valid(v[1]): raise Exception("Invalid email")
            c=self.db.cursor(); c.execute("UPDATE Contact SET name=%s,email=%s,phone=%s,category=%s,notes=%s WHERE id=%s",v+(self.selected(),)); self.db.commit(); c.close(); self.show()
        except Exception as e: messagebox.showerror("Error",str(e))
    def delete(self):
        try:
            c=self.db.cursor(); c.execute("DELETE FROM Contact WHERE id=%s",(self.selected(),)); self.db.commit(); c.close(); self.show()
        except Exception as e: messagebox.showerror("Error",str(e))
    def search(self):
        q="%"+self.search_box.get().strip()+"%"; c=self.db.cursor(); c.execute("SELECT id,name,email,phone,category,notes FROM Contact WHERE name LIKE %s OR email LIKE %s OR phone LIKE %s ORDER BY name",(q,q,q)); self.rows(c.fetchall()); c.close()
    def show(self):
        c=self.db.cursor(); c.execute("SELECT id,name,email,phone,category,notes FROM Contact ORDER BY name"); self.rows(c.fetchall()); c.close()
    def rows(self,rows):
        for x in self.table.get_children(): self.table.delete(x)
        for r in rows: self.table.insert("","end",values=r)
    def select(self,event):
        s=self.table.selection()
        if not s: return
        v=self.table.item(s[0],"values")
        for e,value in zip(self.entries,v[1:]):
            e.delete(0,tk.END); e.insert(0,value)

try:
    root=tk.Tk(); app=ContactManager(root); root.mainloop()
except Exception as e: print("Database error:",e)
