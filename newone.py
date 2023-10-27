from tkinter import *
import os
from tkinter import filedialog
import pandas as pd
from tkinter import ttk
import tkinter as tk
import sqlite3
import os.path
from tkinter import messagebox
import datetime
import random
#main page
root=Tk()
root.title("WALLET PAYMENT")
root.geometry('400x300')
a=0
k=0
sql=sqlite3.connect('database4.db')
con=sql.cursor()

con.execute("""create table if not exists send_transaction4 (emailid,STID,Amount,datetime,phonenumber)""")      
con.execute("""CREATE TABLE if not exists logins4 (Fullname,SSN,orgphonenumber,emailid,password)""")
con.execute("""CREATE TABLE if not exists bankdetails6 (Emailid,bankId,banknum)""")
con.execute("""CREATE TABLE if not exists newphonenumber(Emailid,newphonenumber)""")
con.execute("""create table if not exists request_transaction4 (Emailid,RTID,Amount,datetime,phonenumber)""")
con.execute("""CREATE TABLE if not exists newemailaddress2 (Emailid,newemailid)""")

def register():
    sql=sqlite3.connect('database4.db')
    con=sql.cursor()

    con.execute("insert into logins4 values(:Fullname,:SSN,:orgphonenumber,:emailid,:password)",
        {
            'Fullname':fullname.get(),
            'SSN':SSN.get(),
            'orgphonenumber':PhoneNum.get(),
            'emailid':Email.get(),
            'password':password.get()
        })
    sql.commit()
    messagebox.showinfo(title="your account", message='your account has been created',)

def login():
    global emailid1
    sql=sqlite3.connect('database4.db')
    con=sql.cursor()
    con.execute('select emailid,password from logins4')

    records2=con.fetchall()
    for i in range(len(records2)):
        if Emailid.get()!="" and Password.get()!="" and Emailid.get() in records2[i][0] and Password.get() in records2[i][1] and records2[i][0].index(Emailid.get())==records2[i][1].index(Password.get()):
            global root2
            emailid1=Emailid.get()
            root2=Toplevel(root)
            root2.geometry('400x500')
            global clicked
            global clicked1
            global clicked2
            clicked=StringVar()
            clicked.set('Main Menu')
            clicked1=StringVar()
            clicked1.set('Account functions')
            clicked2=StringVar()
            clicked2.set('Statement Functions')
            drop=OptionMenu(root2,clicked,'Account Info','Send Money','Request money','Statements','Search transactions','Signout',command=selected)
            drop.pack(pady=10)
            drop=OptionMenu(root2,clicked1,'Modify personal details','Add/remove email address','Add/remove phonenumber','Add/remove bank account',command=selected1)
            drop.pack(pady=10)
            drop=OptionMenu(root2,clicked2,'Total amount based on dates','Total amount per month','Transaction with max amount per month','the best users',command=selected2)
            drop.pack(pady=10)
            root.withdraw()
            break
    sql.commit()
def Create():
    global root1
    root1=Toplevel(root)
    root1.geometry('400x500')
    global fullname
    global SSN
    global PhoneNum
    global Email 
    global password
    fullname=StringVar()
    SSN=StringVar()
    PhoneNum=StringVar()
    Email=StringVar()
    password=StringVar()
    Label(root1,text="FullName").grid(row=1,column=3)
    Entry(root1,textvariable=fullname).grid(row=1,column=5)
    Label(root1,text="SSN").grid(row=2,column=3)
    Entry(root1,textvariable=SSN).grid(row=2,column=5)
    Label(root1,text="PhoneNumber").grid(row=3,column=3)
    Entry(root1,textvariable=PhoneNum).grid(row=3,column=5)
    Label(root1,text="Emailid").grid(row=4,column=3)
    Entry(root1,textvariable=Email).grid(row=4,column=5)
    Label(root1,text="Password").grid(row=5,column=3)
    Entry(root1,textvariable=password).grid(row=5,column=5)
    Button(root1,text='Register',command=lambda:{register(),close1()}).grid(row=6,column=5)
    Button(root1,text='Close',command=close1).grid(row=7,column=5)
def selected2(event):
    global root4
    global root2
    if clicked2.get()=="Total amount based on dates":
        root4=Toplevel(root2)
        root4.title("Total amount")
        root4.geometry('800x800')
        root2.withdraw()
        global searchfromdate
        searchfromdate=StringVar()
        global searchtodate
        searchtodate=StringVar()
        global useremail
        useremail=StringVar()
        Label(root4,text="Give the email address").pack()
        Entry(root4,textvariable=useremail).pack()
        Label(root4,text="from date").pack()
        Entry(root4,textvariable=searchfromdate).pack()
        Label(root4,text="to date").pack()
        Entry(root4,textvariable=searchtodate).pack()
        Button(root4,text='Search',command=userdatesearch).pack()
        Button(root4,text='Exit',command=close).pack()
    elif clicked2.get()=="Total amount per month":
        root4=Toplevel(root2)
        root4.title("Total amount per month")
        root4.geometry('800x800')
        root2.withdraw()
        global useremail1
        useremail1=StringVar()
        Label(root4,text="Give the email address").pack()
        Entry(root4,textvariable=useremail1).pack()
        Button(root4,text='Search',command=monthsearch).pack()
        Button(root4,text='Exit',command=close).pack()
    elif clicked2.get()=="Transaction with max amount per month":
        root4=Toplevel(root2)
        root4.title("Total amount per month")
        root4.geometry('800x800')
        root2.withdraw()
        sql=sqlite3.connect('database4.db')
        con=sql.cursor()
        c=con.execute("SELECT substr(datetime,1,2) as month,STID,max(Amount) as Amount,datetime,orgphonenumber,SSN,l.emailid FROM send_transaction4 as se,logins4 as l where se.phonenumber=l.orgphonenumber  and  se.emailid=? group by month",(Emailid.get(),))
        records=c.fetchall()
        Label(root4,text='maximum send amount per month').pack()
        trv=ttk.Treeview(root4,selectmode='browse')
        trv.pack()
        trv["columns"]=("month","STID","Amount","datetime","orgphonenumber","SSN","emailid")
        trv['show']='headings'
        trv.column('month',width=100,anchor='c')
        trv.column('STID',width=100,anchor='c')
        trv.column('Amount',width=100,anchor='c')
        trv.column('datetime',width=100,anchor='c')
        trv.column('orgphonenumber',width=100,anchor='c')
        trv.column('SSN',width=100,anchor='c')
        trv.column('emailid',width=300,anchor='c')
        trv.heading('month',text='month')
        trv.heading('STID',text='STID')
        trv.heading('Amount',text='Amount')
        trv.heading('datetime',text='datetime')
        trv.heading('orgphonenumber',text='orgphonenumber')
        trv.heading('SSN',text='SSN')
        trv.heading('emailid',text='emailid')
        for i in records:
            trv.insert(parent='',index=0,values=i)
        d=con.execute("SELECT substr(datetime,1,2) as month,RTID,Amount,datetime,orgphonenumber,SSN,l.emailid FROM request_transaction4 as re,logins4 as l where re.phonenumber=l.orgphonenumber  and re.emailid=? group by month",(Emailid.get(),))
        records1=d.fetchall()
        Label(root4,text='maximum request amount per month').pack()
        trv=ttk.Treeview(root4,selectmode='browse')
        trv.pack()
        trv["columns"]=("month","RTID","Amount","datetime","orgphonenumber","SSN","emailid")
        trv['show']='headings'
        trv.column('month',width=100,anchor='c')
        trv.column('RTID',width=100,anchor='c')
        trv.column('Amount',width=100,anchor='c')
        trv.column('datetime',width=100,anchor='c')
        trv.column('orgphonenumber',width=100,anchor='c')
        trv.column('SSN',width=100,anchor='c')
        trv.column('emailid',width=300,anchor='c')
        trv.heading('month',text='month')
        trv.heading('RTID',text='RTID')
        trv.heading('Amount',text='Amount')
        trv.heading('datetime',text='datetime')
        trv.heading('orgphonenumber',text='orgphonenumber')
        trv.heading('SSN',text='SSN')
        trv.heading('emailid',text='emailid')
        for i in records1:
            trv.insert(parent='',index=0,values=i)
        Button(root4,text='Close',command=close).pack()
    elif clicked2.get()=="the best users":
        root4=Toplevel(root2)
        root4.title("Total amount per month")
        root4.geometry('800x800')
        root2.withdraw()
        sql=sqlite3.connect('database4.db')
        con=sql.cursor()
        c=con.execute("SELECT emailid,max(total_amount) as Maxtotalamount from (select l.emailid,sum(Amount) as total_amount FROM send_transaction4 as se,logins4 as l where se.phonenumber=l.orgphonenumber  and se.emailid=? group by l.emailid)",(Emailid.get(),))
        records=c.fetchall()
        Label(root4,text='Max total send amount').pack()
        trv=ttk.Treeview(root4,selectmode='browse')
        trv.pack()
        trv["columns"]=("emailid","Maxtotalamount")
        trv['show']='headings'
        trv.column('emailid',width=300,anchor='c')
        trv.column('Maxtotalamount',width=200,anchor='c')
        trv.heading('emailid',text='emailid')
        trv.heading('Maxtotalamount',text='Maxtotalamount')
        for i in records:
            trv.insert(parent='',index=0,values=i)
        d=con.execute("select emailid,max(amount) as Maxamount from (select l.emailid,sum(Amount) as amount FROM request_transaction4 as re,logins4 as l where re.phonenumber=l.orgphonenumber  and re.emailid=? group by l.emailid) ",(Emailid.get(),))
        records1=d.fetchall()
        Label(root4,text='total request amount').pack()
        trv=ttk.Treeview(root4,selectmode='browse')
        trv.pack()
        trv["columns"]=("emailid","Maxtotalamount")
        trv['show']='headings'
        trv.column('emailid',width=300,anchor='c')
        trv.column('Maxtotalamount',width=200,anchor='c')
        trv.heading('emailid',text='emailid')
        trv.heading('Maxtotalamount',text='Maxtotalamount')
        for i in records1:
            trv.insert(parent='',index=0,values=i)
        Button(root4,text='Close',command=close).pack()
    
def monthsearch():
    sql=sqlite3.connect('database4.db')
    con=sql.cursor()
    c=con.execute("SELECT substr(datetime,1,2) as month,sum(Amount) FROM send_transaction4 as se,logins4 as l where se.phonenumber=l.orgphonenumber  and l.emailid=? and se.emailid=? group by month",(useremail1.get(),Emailid.get(),))
    records=c.fetchall()
    Label(root4,text='total send amount per month').pack()
    trv=ttk.Treeview(root4,selectmode='browse')
    trv.pack()
    trv["columns"]=("Month","Total amount")
    trv['show']='headings'
    trv.column('Month',width=100,anchor='c')
    trv.column('Total amount',width=100,anchor='c')
    trv.heading('Month',text='Month')
    trv.heading('Total amount',text='Total amount')
    for i in records:
        trv.insert(parent='',index=0,values=i)   
    d=con.execute("SELECT substr(datetime,1,2) as month,sum(Amount) FROM request_transaction4 as re,logins4 as l where re.phonenumber=l.orgphonenumber  and l.emailid=? and re.emailid=? group by month",(useremail1.get(),Emailid.get(),))
    records1=d.fetchall()
    Label(root4,text='total request amount per month').pack()
    trv=ttk.Treeview(root4,selectmode='browse')
    trv.pack()
    trv["columns"]=("Month","Total amount")
    trv['show']='headings'
    trv.column('Month',width=100,anchor='c')
    trv.column('Total amount',width=100,anchor='c')
    trv.heading('Month',text='Month')
    trv.heading('Total amount',text='Total amount')
    for i in records1:
        trv.insert(parent='',index=0,values=i)  
def userdatesearch():
    sql=sqlite3.connect('database4.db')
    con=sql.cursor()
    c=con.execute("SELECT sum(Amount) as TotalAmount FROM send_transaction4 as se,logins4 as l where se.phonenumber=l.orgphonenumber and l.emailid=? and se.datetime>=? and se.datetime<=? and se.emailid=?",(useremail.get(),searchfromdate.get(),searchtodate.get(),Emailid.get(),))
    records=c.fetchall()
    Label(root4,text='total send amount').pack()
    trv=ttk.Treeview(root4,selectmode='browse')
    trv.pack()
    trv["columns"]=("TotalAmount")
    trv['show']='headings'
    trv.column('TotalAmount',width=100,anchor='c')
    trv.heading('TotalAmount',text='TotalAmount')
    for i in records:
        trv.insert(parent='',index=0,values=i) 
    d=con.execute("select sum(Amount) as TotalAmount FROM request_transaction4 as re,logins4 as l where re.phonenumber=l.orgphonenumber and l.emailid=? and re.datetime>=? and re.datetime<=? and re.emailid=?",(useremail.get(),searchfromdate.get(),searchtodate.get(),Emailid.get(),))
    records1=d.fetchall()
    Label(root4,text='Total request amount').pack()
    trv=ttk.Treeview(root4,selectmode='browse')
    trv.pack()
    trv["columns"]=("TotalAmount")
    trv['show']='headings'
    trv.column('TotalAmount',width=100,anchor='c')
    trv.heading('TotalAmount',text='TotalAmount')
    for i in records1:
        trv.insert(parent='',index=0,values=i) 
def selected(event):
    global root4
    global root2
    global Amountentry
    global Amountentry1
    if clicked.get()=='Account Info':
        root4=Toplevel(root2)
        root4.title("Account Info")
        root4.geometry('1200x1200')
        root2.withdraw()
        global s
        global q
        global r
        global h
        global f
        global k
        sql=sqlite3.connect('database4.db')
        con=sql.cursor()
        y=con.execute("select * from logins4 where emailid=?",(Emailid.get(),))
        records3=y.fetchall()
        f=[]
        for i in records3:
            f.append(i)
        Label(root4,text='Fullname').pack()
        a1=Entry(root4)
        a1.insert(0,f[0][0])
        a1.pack()
        Label(root4,text='Emailid').pack()
        a2=Entry(root4)
        a2.insert(0,f[0][3])
        a2.pack()
        Label(root4,text='SSN').pack()
        a3=Entry(root4)
        a3.insert(0,f[0][1])
        a3.pack()
        Label(root4,text='Phonenumber').pack()
        a4=Entry(root4)
        a4.insert(0,f[0][2])
        a4.pack()
        c=con.execute("SELECT bankId,banknum FROM `bankdetails6` WHERE `emailid` = ?", (Emailid.get(),))
        records=c.fetchall()
        Label(root4,text='All Bank details:-').pack()
        trv=ttk.Treeview(root4,selectmode='browse')
        trv.pack()
        trv["columns"]=("BANKID","AccNumber")
        trv['show']='headings'
        trv.column('BANKID',width=100,anchor='c')
        trv.column('AccNumber',width=100,anchor='c')
        trv.heading('BANKID',text='BANKID')
        trv.heading('AccNumber',text='AccNumber')
        for i in records:
            trv.insert(parent='',index=0,values=i)
    
        d=con.execute("select newemailid from newemailaddress2 where Emailid=? ",(Emailid.get(),))
        records8=d.fetchall()
        Label(root4,text='Additional Emails:-').pack(side=LEFT,anchor=W)
        trv=ttk.Treeview(root4,selectmode='browse')
        trv.pack(side=LEFT,anchor=W)
        trv["columns"]=("NEWEMAILS")
        trv['show']='headings'
        trv.column('NEWEMAILS',width=200,anchor='c')
        trv.heading('NEWEMAILS',text='NEWEMAILS')
        for i in records8:
            trv.insert(parent='',index=0,values=i)
        t=con.execute("select newphonenumber from newphonenumber where Emailid=? ",(Emailid.get(),))
        records9=t.fetchall()
        trv=ttk.Treeview(root4,selectmode='browse')
        trv.pack(side=RIGHT,anchor=E)
        trv["columns"]=("NEWPHONENUMBERS")
        trv['show']='headings'
        trv.column('NEWPHONENUMBERS',width=150,anchor='c')
        trv.heading('NEWPHONENUMBERS',text='NEWPHONENUMBERS')
        for i in records9:
            trv.insert(parent='',index=0,values=i)
        Label(root4,text='Additional phonenumbers:-').pack(side=RIGHT,anchor=E)
        Button(root4,text='Close',command=close,fg='red').pack()
        sql.commit()
    elif clicked.get()=='Send Money':
        root4=Toplevel(root2)
        root4.geometry('400x500')
        root2.withdraw()
        global ephone
        ephone=StringVar()
        Amount=int()
        Phonenumber=Label(root4,text='phonenumber')
        Phonenumber.pack()
        Phonenumberentry=Entry(root4,textvariable=ephone)
        Phonenumberentry.pack()
        Amount=Label(root4,text='Amount')
        Amount.pack()
        Amountentry=Entry(root4,textvariable=Amount)
        Amountentry.pack()
        Button(root4,text='Send Money',command=send).pack()
        Button(root4,text='Exit',command=close).pack()
    elif clicked.get()=='Request money':
        root4=Toplevel(root2)
        root4.geometry('400x500')
        root2.withdraw()
        global ephone1
        ephone1=StringVar()
        Amount1=int()
        Phonenumber1=Label(root4,text='phonenumber')
        Phonenumber1.pack()
        Phonenumberentry1=Entry(root4,textvariable=ephone1)
        Phonenumberentry1.pack()
        Amount1=Label(root4,text='Amount')
        Amount1.pack()
        Amountentry1=Entry(root4,textvariable=Amount1)
        Amountentry1.pack()
        Button(root4,text='Request Money',command=request).pack()
        Button(root4,text='Exit',command=close).pack()
    elif clicked.get()=='Statements':
        root4=Toplevel(root2)
        root4.geometry('800x800')
        root2.withdraw()
        sql=sqlite3.connect('database4.db')
        con=sql.cursor()
        c=con.execute("SELECT STID,Amount,datetime,orgphonenumber,SSN,l.emailid FROM send_transaction4 as se,logins4 as l where se.phonenumber=l.orgphonenumber and se.emailid=?",(Emailid.get(),))
        records=c.fetchall()
        trv=ttk.Treeview(root4,selectmode='browse')
        trv.pack()
        trv["columns"]=("STID","Amount","datetime","orgphonenumber","SSN","emailid")
        trv['show']='headings'
        trv.column('STID',width=100,anchor='c')
        trv.column('Amount',width=100,anchor='c')
        trv.column('datetime',width=100,anchor='c')
        trv.column('orgphonenumber',width=100,anchor='c')
        trv.column('SSN',width=100,anchor='c')
        trv.column('emailid',width=300,anchor='c')
        trv.heading('STID',text='STID')
        trv.heading('Amount',text='Amount')
        trv.heading('datetime',text='datetime')
        trv.heading('orgphonenumber',text='orgphonenumber')
        trv.heading('SSN',text='SSN')
        trv.heading('emailid',text='emailid')
        for i in records:
            trv.insert(parent='',index=0,values=i)
        c=con.execute("SELECT RTID,Amount,datetime,orgphonenumber,SSN,l.emailid FROM request_transaction4 as re,logins4 as l where re.phonenumber=l.orgphonenumber and re.emailid=?",(Emailid.get(),))
        records1=c.fetchall()
        trv=ttk.Treeview(root4,selectmode='browse')
        trv.pack()
        trv["columns"]=("RTID","Amount","datetime","orgphonenumber","SSN","emailid")
        trv['show']='headings'
        trv.column('RTID',width=100,anchor='c')
        trv.column('Amount',width=100,anchor='c')
        trv.column('datetime',width=100,anchor='c')
        trv.column('orgphonenumber',width=100,anchor='c')
        trv.column('SSN',width=100,anchor='c')
        trv.column('emailid',width=300,anchor='c')
        trv.heading('RTID',text='RTID')
        trv.heading('Amount',text='Amount')
        trv.heading('datetime',text='datetime')
        trv.heading('orgphonenumber',text='orgphonenumber')
        trv.heading('SSN',text='SSN')
        trv.heading('emailid',text='emailid')
        for i in records1:
            trv.insert(parent='',index=0,values=i)
        Button(root4,text='Exit',command=close).pack()
        sql.commit()
    elif clicked.get()=='Search transactions':
        root4=Toplevel(root2)
        root4.geometry('400x400')
        root2.withdraw()
        global searchclicked
        searchclicked=StringVar()
        searchclicked.set('search')
        drop=OptionMenu(root4,searchclicked,'Based on SSN','Based on Emailid','Based on phonenumber','Based on date',command=searchselected)
        drop.pack()
        Button(root4,text='Exit',command=close).pack()
        
    elif clicked.get()=='Signout':
        if messagebox.askyesno('signout','are you sure, you want to signout?')==True: 
            Password.set("")
            Emailid.set("")
            root2.withdraw()
            root.deiconify()
def searchselected(event):
    global root5
    if searchclicked.get()=='Based on SSN':
        root5=Toplevel(root4)
        root5.geometry('800x800')
        root4.withdraw()
        global searchSSN
        searchSSN=StringVar()
        Label(root5,text="Give the SSN").pack()
        Entry(root5,textvariable=searchSSN).pack()
        Button(root5,text='Search',command=SSNbasedsearch).pack()
        Button(root5,text='<-Back',command=close3).pack()  
        Button(root5,text='Exit',command=close2).pack()   
    elif searchclicked.get()=='Based on Emailid':
        root5=Toplevel(root4)
        root5.geometry('800x800')
        root4.withdraw()
        global searchemail
        searchemail=StringVar()
        Label(root5,text="Give the email address").pack()
        Entry(root5,textvariable=searchemail).pack()
        Button(root5,text='Search',command=emailbasedsearch).pack()
        Button(root5,text='<-Back',command=close3).pack() 
        Button(root5,text='Exit',command=close2).pack()   
    elif searchclicked.get()=='Based on phonenumber':
        root5=Toplevel(root4)
        root5.geometry('800x800')
        root4.withdraw()
        global searchphonenumber
        searchphonenumber=StringVar()
        Label(root5,text="Give the phonenumber").pack()
        Entry(root5,textvariable=searchphonenumber).pack()
        Button(root5,text='Search',command=phonenumberbasedsearch).pack()
        Button(root5,text='<-Back',command=close3).pack() 
        Button(root5,text='Exit',command=close2).pack()
    elif searchclicked.get()=='Based on date':
        root5=Toplevel(root4)
        root5.geometry('800x800')
        root4.withdraw()
        global searchfromdate
        searchfromdate=StringVar()
        global searchtodate
        searchtodate=StringVar()
        Label(root5,text="from date").pack()
        Entry(root5,textvariable=searchfromdate).pack()
        Label(root5,text="to date").pack()
        Entry(root5,textvariable=searchtodate).pack()
        Button(root5,text='Search',command=datebasedsearch).pack()
        Button(root5,text='<-Back',command=close3).pack() 
        Button(root5,text='Exit',command=close2).pack()
def datebasedsearch():
    sql=sqlite3.connect('database4.db')
    con=sql.cursor()
    c=con.execute("SELECT STID,Amount,datetime,orgphonenumber,SSN,l.emailid FROM send_transaction4 as se,logins4 as l where se.phonenumber=l.orgphonenumber and se.datetime>=? and se.datetime<=? and se.emailid=?",(searchfromdate.get(),searchtodate.get(),Emailid.get(),))
    records=c.fetchall()
    trv=ttk.Treeview(root5,selectmode='browse')
    trv.pack()
    trv["columns"]=("STID","Amount","datetime","orgphonenumber","SSN","emailid")
    trv['show']='headings'
    trv.column('STID',width=100,anchor='c')
    trv.column('Amount',width=100,anchor='c')
    trv.column('datetime',width=100,anchor='c')
    trv.column('orgphonenumber',width=100,anchor='c')
    trv.column('SSN',width=100,anchor='c')
    trv.column('emailid',width=300,anchor='c')
    trv.heading('STID',text='STID')
    trv.heading('Amount',text='Amount')
    trv.heading('datetime',text='datetime')
    trv.heading('orgphonenumber',text='orgphonenumber')
    trv.heading('SSN',text='SSN')
    trv.heading('emailid',text='emailid')
    for i in records:
        trv.insert(parent='',index=0,values=i)
    d=con.execute("SELECT RTID,Amount,datetime,orgphonenumber,SSN,l.emailid FROM request_transaction4 as re,logins4 as l where re.phonenumber=l.orgphonenumber and re.datetime>=? and re.datetime<=? and re.emailid=?",(searchfromdate.get(),searchtodate.get(),Emailid.get(),))
    records1=d.fetchall()
    trv=ttk.Treeview(root5,selectmode='browse')
    trv.pack()
    trv["columns"]=("RTID","Amount","datetime","orgphonenumber","SSN","emailid")
    trv['show']='headings'
    trv.column('RTID',width=100,anchor='c')
    trv.column('Amount',width=100,anchor='c')
    trv.column('datetime',width=100,anchor='c')
    trv.column('orgphonenumber',width=100,anchor='c')
    trv.column('SSN',width=100,anchor='c')
    trv.column('emailid',width=300,anchor='c')
    trv.heading('RTID',text='RTID')
    trv.heading('Amount',text='Amount')
    trv.heading('datetime',text='datetime')
    trv.heading('orgphonenumber',text='orgphonenumber')
    trv.heading('SSN',text='SSN')
    trv.heading('emailid',text='emailid')
    for i in records1:
        trv.insert(parent='',index=0,values=i)
    sql.commit()
    sql.close()

def phonenumberbasedsearch():
    sql=sqlite3.connect('database4.db')
    con=sql.cursor()
    c=con.execute("SELECT STID,Amount,datetime,orgphonenumber,SSN,l.emailid FROM send_transaction4 as se,logins4 as l where se.phonenumber=l.orgphonenumber and l.orgphonenumber=? and se.emailid=?",(searchphonenumber.get(),Emailid.get(),))
    records=c.fetchall()
    trv=ttk.Treeview(root5,selectmode='browse')
    trv.pack()
    trv["columns"]=("STID","Amount","datetime","orgphonenumber","SSN","emailid")
    trv['show']='headings'
    trv.column('STID',width=100,anchor='c')
    trv.column('Amount',width=100,anchor='c')
    trv.column('datetime',width=100,anchor='c')
    trv.column('orgphonenumber',width=100,anchor='c')
    trv.column('SSN',width=100,anchor='c')
    trv.column('emailid',width=300,anchor='c')
    trv.heading('STID',text='STID')
    trv.heading('Amount',text='Amount')
    trv.heading('datetime',text='datetime')
    trv.heading('orgphonenumber',text='orgphonenumber')
    trv.heading('SSN',text='SSN')
    trv.heading('emailid',text='emailid')
    for i in records:
        trv.insert(parent='',index=0,values=i)
    d=con.execute("SELECT RTID,Amount,datetime,orgphonenumber,SSN,l.emailid FROM request_transaction4 as re,logins4 as l where re.phonenumber=l.orgphonenumber and l.orgphonenumber=? and re.emailid=?",(searchphonenumber.get(),Emailid.get(),))
    records1=d.fetchall()
    trv=ttk.Treeview(root5,selectmode='browse')
    trv.pack()
    trv["columns"]=("RTID","Amount","datetime","orgphonenumber","SSN","emailid")
    trv['show']='headings'
    trv.column('RTID',width=100,anchor='c')
    trv.column('Amount',width=100,anchor='c')
    trv.column('datetime',width=100,anchor='c')
    trv.column('orgphonenumber',width=100,anchor='c')
    trv.column('SSN',width=100,anchor='c')
    trv.column('emailid',width=300,anchor='c')
    trv.heading('RTID',text='RTID')
    trv.heading('Amount',text='Amount')
    trv.heading('datetime',text='datetime')
    trv.heading('orgphonenumber',text='orgphonenumber')
    trv.heading('SSN',text='SSN')
    trv.heading('emailid',text='emailid')
    for i in records1:
        trv.insert(parent='',index=0,values=i)
    
def emailbasedsearch():
    sql=sqlite3.connect('database4.db')
    con=sql.cursor()
    c=con.execute("SELECT STID,Amount,datetime,orgphonenumber,SSN,l.emailid FROM send_transaction4 as se,logins4 as l where se.phonenumber=l.orgphonenumber and l.emailid=? and se.emailid=?",(searchemail.get(),Emailid.get(),))
    records=c.fetchall()
    trv=ttk.Treeview(root5,selectmode='browse')
    trv.pack()
    trv["columns"]=("STID","Amount","datetime","orgphonenumber","SSN","emailid")
    trv['show']='headings'
    trv.column('STID',width=100,anchor='c')
    trv.column('Amount',width=100,anchor='c')
    trv.column('datetime',width=100,anchor='c')
    trv.column('orgphonenumber',width=100,anchor='c')
    trv.column('SSN',width=100,anchor='c')
    trv.column('emailid',width=300,anchor='c')
    trv.heading('STID',text='STID')
    trv.heading('Amount',text='Amount')
    trv.heading('datetime',text='datetime')
    trv.heading('orgphonenumber',text='orgphonenumber')
    trv.heading('SSN',text='SSN')
    trv.heading('emailid',text='emailid')
    for i in records:
        trv.insert(parent='',index=0,values=i)
    d=con.execute("SELECT RTID,Amount,datetime,orgphonenumber,SSN,l.emailid FROM request_transaction4 as re,logins4 as l where re.phonenumber=l.orgphonenumber and l.emailid=? and re.emailid=?",(searchemail.get(),Emailid.get(),))
    records1=d.fetchall()
    trv=ttk.Treeview(root5,selectmode='browse')
    trv.pack()
    trv["columns"]=("RTID","Amount","datetime","orgphonenumber","SSN","emailid")
    trv['show']='headings'
    trv.column('RTID',width=100,anchor='c')
    trv.column('Amount',width=100,anchor='c')
    trv.column('datetime',width=100,anchor='c')
    trv.column('orgphonenumber',width=100,anchor='c')
    trv.column('SSN',width=100,anchor='c')
    trv.column('emailid',width=300,anchor='c')
    trv.heading('RTID',text='RTID')
    trv.heading('Amount',text='Amount')
    trv.heading('datetime',text='datetime')
    trv.heading('orgphonenumber',text='orgphonenumber')
    trv.heading('SSN',text='SSN')
    trv.heading('emailid',text='emailid')
    for i in records1:
        trv.insert(parent='',index=0,values=i)
def SSNbasedsearch():
    sql=sqlite3.connect('database4.db')
    con=sql.cursor()
    c=con.execute("SELECT STID,Amount,datetime,orgphonenumber,SSN,l.emailid FROM send_transaction4 as se,logins4 as l where se.phonenumber=l.orgphonenumber and l.SSN=? and se.emailid=?",(searchSSN.get(),Emailid.get(),))
    records=c.fetchall()
    trv=ttk.Treeview(root5,selectmode='browse')
    trv.pack()
    trv["columns"]=("STID","Amount","datetime","orgphonenumber","SSN","emailid")
    trv['show']='headings'
    trv.column('STID',width=100,anchor='c')
    trv.column('Amount',width=100,anchor='c')
    trv.column('datetime',width=100,anchor='c')
    trv.column('orgphonenumber',width=100,anchor='c')
    trv.column('SSN',width=100,anchor='c')
    trv.column('emailid',width=300,anchor='c')
    trv.heading('STID',text='STID')
    trv.heading('Amount',text='Amount')
    trv.heading('datetime',text='datetime')
    trv.heading('orgphonenumber',text='orgphonenumber')
    trv.heading('SSN',text='SSN')
    trv.heading('emailid',text='emailid')
    for i in records:
        trv.insert(parent='',index=0,values=i)
    d=con.execute("SELECT RTID,Amount,datetime,orgphonenumber,SSN,l.emailid FROM request_transaction4 as re,logins4 as l where re.phonenumber=l.orgphonenumber and l.SSN=? and re.emailid=?",(searchSSN.get(),Emailid.get(),))
    records1=d.fetchall()
    trv=ttk.Treeview(root5,selectmode='browse')
    trv.pack()
    trv["columns"]=("RTID","Amount","datetime","orgphonenumber","SSN","emailid")
    trv['show']='headings'
    trv.column('RTID',width=100,anchor='c')
    trv.column('Amount',width=100,anchor='c')
    trv.column('datetime',width=100,anchor='c')
    trv.column('orgphonenumber',width=100,anchor='c')
    trv.column('SSN',width=100,anchor='c')
    trv.column('emailid',width=300,anchor='c')
    trv.heading('RTID',text='RTID')
    trv.heading('Amount',text='Amount')
    trv.heading('datetime',text='datetime')
    trv.heading('orgphonenumber',text='orgphonenumber')
    trv.heading('SSN',text='SSN')
    trv.heading('emailid',text='emailid')
    for i in records1:
        trv.insert(parent='',index=0,values=i)

def send():
    b=[]
    sql=sqlite3.connect('database4.db')
    con=sql.cursor()
    con=sql.cursor()
    a=con.execute("select orgphonenumber from logins4")
    records6=a.fetchall()
    for i in records6:
        b.append(i[0])
    if ephone.get() in b:
        f=random.randint(1,100000000000)
        date=datetime.datetime.now()
        g=date.strftime("%m-%d-%y")      

        m=con.execute("insert into send_transaction4 values(:emailid,:STID,:Amount,:datetime,:phonenumber)",
        {
            'emailid':Emailid.get(),
            'STID':f,
            'Amount':Amountentry.get(),
            'datetime':g,
            'phonenumber':ephone.get()
        })
        messagebox.showinfo(title="Transaction",message="Money sent successfully")
        close()
    else:
        messagebox.showerror(message="The phone is not registered with Wallet payment")
    
    sql.commit()
def request():
    b=[]
    sql=sqlite3.connect('database4.db')
    con=sql.cursor()
    con=sql.cursor()
    a=con.execute("select orgphonenumber from logins4")
    records6=a.fetchall()
    for i in records6:
        b.append(i[0])
    
    if ephone1.get() in b:
        f=random.randint(1,100000000000)
        date=datetime.datetime.now()
        g=date.strftime("%m-%d-%y")
        m=con.execute("insert into request_transaction4 values(:Emailid,:RTID,:Amount,:datetime,:phonenumber)",
        {
            'Emailid':Emailid.get(),
            'RTID':f,
            'Amount':Amountentry1.get(),
            'datetime':g,
            'phonenumber':ephone1.get()
        })
        messagebox.showinfo(title="Transaction",message="Requesting money complete")
        close()
    else:
        messagebox.showerror(message="The phone is not registered with Wallet payment")
    
    sql.commit()
def selected1(event):
    global root3
    root3=Toplevel(root2)
    root3.geometry('400x500')

    if clicked1.get()=='Add/remove bank account':
        Button(root3,text='Add New Account',command=add).pack()
        Button(root3,text='Remove Account',command=remove).pack()
        Button(root3,text='<-Back',command=goback).pack()
        root2.withdraw()
    elif clicked1.get()=='Add/remove email address': 
        Button(root3,text='Add New Email Address',command=add1).pack()
        Button(root3,text='Remove Email Address',command=remove1).pack()
        Button(root3,text='goback',command=goback).pack()
        root2.withdraw()
    elif clicked1.get()=='Add/remove phonenumber':
        Button(root3,text='Add New Phonenumber',command=add2).pack()
        Button(root3,text='Remove Phonenumber',command=remove2).pack()
        Button(root3,text='<-Back',command=goback).pack()
        root2.withdraw()
    elif clicked1.get()=='Modify personal details':
        global b1
        global b2
        global b3
        global b4
        Label(root3,text='Fullname').grid(row=1,column=3)
        b1=Entry(root3)
        b1.insert(0,f[0][0])
        b1.grid(row=1,column=5)
        Label(root3,text='SSN').grid(row=2,column=3)
        b3=Entry(root3)
        b3.insert(0,f[0][1])
        b3.grid(row=2,column=5)
        Label(root3,text='Phonenumber').grid(row=3,column=3)
        b4=Entry(root3)
        b4.insert(0,f[0][2])
        b4.grid(row=3,column=5)
        Button(root3,text='Modify',command=modify).grid(row=4,column=5)
        Button(root3,text='<-Back',command=goback).grid(row=5,column=5)
        root2.withdraw()
def modify():
    root3.withdraw()
    root2.deiconify()
    sql=sqlite3.connect('database4.db')
    con=sql.cursor()
    con=sql.cursor()
    con.execute("Update logins4 set fullname=? where emailid=?",(b1.get(),Emailid.get(),))
    con.execute("Update logins4 set SSN=? where emailid=?",(b3.get(),Emailid.get(),))
    con.execute("Update logins4 set orgphonenumber=? where emailid=?",(b4.get(),Emailid.get(),))
    sql.commit()
        
    
def add1():
    global root4
    root4=Toplevel(root)
    root4.title('Adding Email address')
    root4.geometry('400x500')
    root3.withdraw()
    global newemail
    newemail=StringVar()
    Label(root4,text="Email Address").grid(row=1,column=3)
    Entry(root4,textvariable=newemail).grid(row=1,column=5)
    Button(root4,text='Add New Email Address',command=lambda:{adding1(),quiting()}).grid(row=3,column=3)
    Button(root4,text='<-Back',command=close).grid(row=4,column=3)

def remove1():
    global root4
    global emailidrem
    root4=Toplevel(root)
    root4.title('Removing Email Address')
    root4.geometry('400x500')
    root3.withdraw()
    emailidrem=StringVar()
    sql=sqlite3.connect('database4.db')
    con=sql.cursor()
        
    d=con.execute("select newemailid from newemailaddress2 where Emailid=? ",(Emailid.get(),))
    records8=d.fetchall()
    trv=ttk.Treeview(root4,selectmode='browse')
    trv.pack()
    trv["columns"]=("EMAILS")
    trv['show']='headings'
    trv.column('EMAILS',width=200,anchor='c')
    trv.heading('EMAILS',text='EMAILS')
    for i in records8:
        trv.insert(parent='',index=0,values=i)
    Label(root4,text="emailaddress").pack()
    Entry(root4,textvariable=emailidrem).pack()
    Button(root4,text='Remove Email address',command=lambda:{removing1(),quiting()}).pack()
    Button(root4,text='<-Back',command=close).pack()
def removing1():
    sql=sqlite3.connect('database4.db')
    con=sql.cursor()
    con.execute("delete from 'newemailaddress2' where newemailid= ?",(emailidrem.get(),))
    messagebox.showinfo(message="Email address has been removed")
    sql.commit()
def add2():
    global root4
    root4=Toplevel(root)
    root4.title('Adding phonenumber')
    root4.geometry('400x500')
    root3.withdraw()
    global newphonenumber
    newphonenumber=StringVar()
    Label(root4,text="phone number").grid(row=1,column=3)
    Entry(root4,textvariable=newphonenumber).grid(row=1,column=5)
    Button(root4,text='Add New Phonenumber',command=lambda:{adding2(),quiting()}).grid(row=3,column=3)
    Button(root4,text='<-Back',command=close).grid(row=4,column=3)

def remove2():
    global root4
    global phonenumrem
    root4=Toplevel(root)
    root4.title('Removing phonenumber')
    root4.geometry('400x500')
    root3.withdraw()
    phonenumrem=StringVar()
    sql=sqlite3.connect('database4.db')
    con=sql.cursor()
        
    t=con.execute("select newphonenumber from newphonenumber where Emailid=? ",(Emailid.get(),))
    records9=t.fetchall()
    trv=ttk.Treeview(root4,selectmode='browse')
    trv.pack()
    trv["columns"]=("PHONENUMBERS")
    trv['show']='headings'
    trv.column('PHONENUMBERS',width=150,anchor='c')
    trv.heading('PHONENUMBERS',text='PHONENUMBERS')
    for i in records9:
        trv.insert(parent='',index=0,values=i)
    Label(root4,text="phonenumber").pack()
    Entry(root4,textvariable=phonenumrem).pack()
    Button(root4,text='Remove Phonenumber',command=lambda:{removing2(),quiting()}).pack()
    Button(root4,text='<-Back',command=close).pack() 
def removing2():
    sql=sqlite3.connect('database4.db')
    con=sql.cursor()
    con.execute("delete from 'newphonenumber' where newphonenumber= ?",(phonenumrem.get(),))
    messagebox.showinfo(message="phonenumber has been removed")
    sql.commit()
def add():
    global root4
    root4=Toplevel(root)
    root4.title('Adding Account')
    root4.geometry('400x500')
    root3.withdraw()
    global bankid
    global accountnum
    bankid=StringVar()
    accountnum=IntVar()
    Label(root4,text="BankID").grid(row=1,column=3)
    Entry(root4,textvariable=bankid).grid(row=1,column=5)
    Label(root4,text="Account number").grid(row=2,column=3)
    Entry(root4,textvariable=accountnum).grid(row=2,column=5)
    Button(root4,text='Add New Account',command=lambda:{adding(),quiting()}).grid(row=3,column=3)
    Button(root4,text='Close',command=close).grid(row=4,column=3)
def adding():
    sql=sqlite3.connect('database4.db')
    con=sql.cursor()
    con.execute("""CREATE TABLE if not exists bankdetails6 (Emailid,bankId,banknum)""")

    con.execute("INSERT INTO bankdetails6 VALUES(:Emailid,:bankId,:banknum)",
        {   
            'Emailid':emailid1,
            'bankId':bankid.get(),
            'banknum':accountnum.get()
        })
    records=con.fetchall()
    messagebox.showinfo(message="Bank details has been added")
    sql.commit()
    sql.close()
def remove():
    global root4
    global bankidrem
    global accountnumrem
    root4=Toplevel(root)
    root4.title('Removing Account')
    root4.geometry('400x500')
    root3.withdraw()
    bankidrem=StringVar()
    accountnumrem=IntVar()
    sql=sqlite3.connect('database4.db')
    con=sql.cursor()
        
    c=con.execute("SELECT bankId,banknum FROM `bankdetails6` WHERE `emailid` = ?", (Emailid.get(),))
    records=c.fetchall()
    Label(root4,text='All Bank details:-').pack()
    trv=ttk.Treeview(root4,selectmode='browse')
    trv.pack()
    trv["columns"]=("BANKID","AccNumber")
    trv['show']='headings'
    trv.column('BANKID',width=100,anchor='c')
    trv.column('AccNumber',width=100,anchor='c')
    trv.heading('BANKID',text='BANKID')
    trv.heading('AccNumber',text='AccNumber')
    for i in records:
        trv.insert(parent='',index=0,values=i)
    Label(root4,text="BankID").pack()
    Entry(root4,textvariable=bankidrem).pack()
    Label(root4,text="Account number").pack()
    Entry(root4,textvariable=accountnumrem).pack()
    Button(root4,text='Remove Account',command=lambda:{removing(),quiting()}).pack()
    Button(root4,text='<-Back',command=close).pack()
def removing():
    sql=sqlite3.connect('database4.db')
    con=sql.cursor()
    con.execute("delete from 'bankdetails6' where bankId=? and banknum=?",(bankidrem.get(),accountnumrem.get(),))
    messagebox.showinfo(message="Bank details has been removed")
    sql.commit()
def adding1():
    global q
    sql=sqlite3.connect('database4.db')
    con=sql.cursor()

    con.execute("INSERT INTO newemailaddress2 VALUES(:Emailid,:newemailid)",
        {   
            'Emailid':emailid1,
            'newemailid':newemail.get()
        })
    messagebox.showinfo(message="new email address has been added")
    sql.commit()
    sql.close()
def adding2():
    global r
    sql=sqlite3.connect('database4.db')
    con=sql.cursor()

    con.execute("INSERT INTO newphonenumber VALUES(:Emailid,:newphonenumber)",
        {   
            'Emailid':emailid1,
            'newphonenumber':newphonenumber.get()
        })
    messagebox.showinfo(message="new phonenumber has been added")
    sql.commit()
    sql.close()
def quiting():
    root4.withdraw()
    root2.deiconify()
def close():
    root4.withdraw()
    root2.deiconify()
def close1():
    root1.withdraw()
def close2():
    root4.withdraw()
    root5.withdraw()
    root2.deiconify()
def close3():
    root5.withdraw()
    root4.deiconify()
def goback():
    root3.withdraw()
    root2.deiconify()

#buttons
global Password
global Emailid
Emailid=StringVar()
Password=StringVar()
Label(root,text="Enter Emailid").grid(row=1,column=3)
Entry(root,textvariable=Emailid).grid(row=1,column=5)
Label(root,text="Password").grid(row=2,column=3)
Entry(root,textvariable=Password).grid(row=2,column=5)
Button(root,text="Create an Account",command=lambda: [Create()]).grid(row=10,column=5)
Button(root,text='Login->',command=login).grid(row=5,column=5)
sql.commit()
root.mainloop()