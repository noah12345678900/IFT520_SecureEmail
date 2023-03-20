from datetime import date
from operator import ne
import tkinter as tk
from getpass import getpass
from tkinter.tix import IMAGETEXT
from tkinter import ttk
from mysql.connector import connect, Error
from tkinter import *
from tkinter import ttk
import psycopg2
import os
import rsa
from datetime import date

today = date.today()

DATABASE_URL = "postgresql://default:LDsRLnPMUBGGypgc3nZncA@ift520-9628.7tt.cockroachlabs.cloud:26257/asymmetric?sslmode=verify-full"

conn = psycopg2.connect(DATABASE_URL)

class main:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Secure Email")
        self.root.geometry('300x300')
        self.root.resizable(width=False, height=False)
        self.main()

    def main(self):
        usr_login = tk.Label(self.root, text="Username")
        usr_login.grid(row=0, column=0)
        self.usernameText = tk.Entry(self.root)
        self.usernameText.grid(row=0, column=1) 

        pwd_login = tk.Label(self.root, text="Password")
        pwd_login.grid(row=1, column=0)
        self.passwordText = tk.Entry(self.root, show='*')  
        self.passwordText.grid(row=1, column=1) 

        #remember me check box saves the login credentials for next time
        usr_pwd_button = tk.Label(self.root, text="Remember me.")
        usr_pwd_button.grid(row=2, column=1)
        rembr = tk.Checkbutton(self.root)
        rembr.grid(row=2, column=2)
        usr_logn_button = tk.Button(self.root, text="Login", command=self.login)
        usr_logn_button.grid(row=3, column=1)

        #signup button
        lable = tk.Label(self.root, text="Not registered ?")
        lable.grid(row=4, column=1)
        rememberMe = tk.StringVar()
        signupButton = tk.Button(self.root,  text="Sign up.", command=self.signup)
        signupButton.grid(row=4, column=2)

        self.root.mainloop()

    def login(self):
        a = self.usernameText.get()
        b = self.passwordText.get()
        usrCheck = 0
        passCheck = 0
        #with conn.cursor() as cur:
            #cur.execute("CREATE TABLE IF NOT EXISTS login (username STRING PRIMARY KEY, password STRING)")
            #cur.execute("INSERT INTO login (username, password) VALUES (1234234, 123456789)")
            #cur.execute("SELECT username FROM login")
            #username = cur.fetchall()
            #cur.execute("SELECT password FROM login")
            #password = cur.fetchall()

        conn.commit()
        self.root.destroy()
        application()
        for x in username:
            if x[0] == a:
                usrCheck = 1
        for y in password:
            if y[0] == b:
                passCheck = 1
        if usrCheck == 1 & passCheck == 1:
            self.root.destroy()
            application()
        else:
            pass
    def signup(self):
        self.root.destroy()
        signup()

class signup:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("Sign Up")
        self.app.geometry('400x400')
        self.app.resizable(width=False, height=False)
        self.app['background']='#187dd8'
        self.app.attributes('-alpha',0.97)
        self.main()
    def main(self):
        
        usernamex = Label(self.app, text ='username: ', bg='#187dd8', font=("Arial", 10))
        usernamex.grid(row=0,column=0, pady=20, sticky=E)
        self.username = Entry(self.app, width=23)
        self.username.grid(row=0, column=1,pady=20, sticky=E)

        password = Label(self.app, text ='password: ', bg='#187dd8', font=("Arial", 10))
        password.grid(row=1,column=0, pady=20, sticky=E)
        self.password = Entry(self.app, width=23)
        self.password.grid(row=1, column=1,pady=20, sticky=E)

        reenterp = Label(self.app, text ='re-enter password: ', bg='#187dd8', font=("Arial", 10))
        reenterp.grid(row=2,column=0, padx=10, pady=20, sticky=E)
        self.password = Entry(self.app, width=23)
        self.password.grid(row=2, column=1,pady=20, sticky=E)

        email = Label(self.app, text ='Email: ', bg='#187dd8', font=("Arial", 10))
        email.grid(row=3,column=0, pady=20, sticky=E)
        self.email = Entry(self.app, width=23)
        self.email.grid(row=3, column=1,pady=20, sticky=E)

        SignUp = tk.Button(self.app, text="Sign-Up", height=1, width=20, fg="black", highlightbackground = "black", highlightthickness = 5, font=("Arial", 10), 
        bg='#187dd8', bd=3, relief="solid", activebackground='#187dd8', command=self.makekey)
        SignUp.grid(row=4, column=1, padx=0, pady=100, sticky=tk.NS)
        
    def makekey(self):
         #CREATE PUBLIC AND PRIVATE KEY
        username = self.username.get()
        password = self.password.get()
        email = self.email.get()
        public_key, private_key = rsa.newkeys(1024)
        
        #CREATE PUBLIC AND PRIVATE KEY
        public_key, private_key = rsa.newkeys(1024)

        with open("public.pem", "wb") as f:
            f.write(public_key.save_pkcs1("PEM"))
        with open("private.pem", "wb") as f:
            f.write(private_key.save_pkcs1("PEM"))

        with open("public.pem", "rb") as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read())
        with open("private.pem", "rb") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())
            
            #SEND TO dB AND ATTACH USER TO PRIMARY KEY
        time = today.strftime("%m/%d/%y")

        with conn.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS login (username STRING PRIMARY KEY, password STRING, email STRING, accountCreationDate DATE)")
            cur.execute("CREATE TABLE IF NOT EXISTS keys (username STRING PRIMARY KEY, privatekeys STRING, publickeys STRING)")
            cur.execute("CREATE TABLE IF NOT EXISTS usersession (username STRING PRIMARY KEY, status STRING)")

            cur.execute("SELECT username FROM login")
            allusernames = cur.fetchall()

            for x in allusernames:
                if username == x[0]:
                    with conn.cursor() as cur:
                        encryptPass = rsa.encrypt(password, public_key)
                        cur.execute('INSERT INTO login VALUES(%s, %s, %s)', (username, encryptPass, email))
                        cur.execute('INSERT INTO keys VALUES(%s, %s, %s)', (username, public_key, private_key))
                        cur.execute('INSERT INTO userSession VALUES(%s, %s, %s)', (username, time))
                    conn.commit()
                else:
                    pass
            conn.commit()
        self.app.destroy()
        main()
        

        
class application:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("Secure Email")
        self.app.geometry('1070x900')
        self.app.resizable(width=False, height=False)
        self.app['background']='#187dd8'
        self.app.attributes('-alpha',0.97)
        self.main()
    def main(self):

        refresh = tk.Button(self.app, text="Refresh", bg='#187dd8', height=15, width=12, font=("Arial", 12), relief="solid", activebackground='#187dd8', command=self.inbox)
        refresh.grid(row=1, column=0, padx=60, pady=5, sticky=tk.NW)

        welcomeLabel = Label(self.app, text ='Welcome to the IFT 520 Secure Email Application', bg='#187dd8', font=("Arial", 20))
        welcomeLabel.grid(row=1,column=1, pady=60, sticky=E)
        compose = tk.Button(self.app, text="Compose", bg='#187dd8', height=4, width=12, font=("Arial", 12), relief="solid", activebackground='#187dd8', command=self.compose)
        compose.grid(row=1, column=1, padx=60, pady=5, sticky=tk.S)

        trash = tk.Button(self.app, text="Trash", bg='#187dd8', height=15, width=12, font=("Arial", 12), relief="solid", activebackground='#187dd8', command=self.trash)
        trash.grid(row=1, column=2, padx=60, pady=5, sticky=tk.SW)

        #CreateCxButton = tk.Button(self.app, text="Create Customer Profile", height=1, width=20, fg="black", highlightbackground = "black", highlightthickness = 5, font=("Arial", 10), 
        #bg='#187dd8', bd=3, relief="solid", activebackground='#187dd8', command=self.createProfile)
        #CreateCxButton.grid(row=11, column=1, padx=0, pady=100, sticky=tk.NS)

        #createcart = tk.Button(self.app, text="Create Cart", height=1, width=15, fg="black", highlightbackground = "black", highlightthickness = 5,
        #font=("Arial", 10), bg='#187dd8', bd=3, relief="solid", activebackground='#187dd8', command=self.cart)
        #createcart.grid(row=13, column=1, padx=0, pady=100, sticky=tk.S)

        #refresh = tk.Button(self.app, text="Refresh Results", height=1, width=15, fg="black", highlightbackground = "black", highlightthickness = 5,
        #font=("Arial", 10), bg='#187dd8', bd=3, relief="solid", activebackground='#187dd8', command=self.Refresh)
        #refresh.grid(row=12, column=1, padx=0, pady=100, sticky=tk.S)

        self.tree = ttk.Treeview(self.app)
        self.tree.place(relx=0.17, rely=0.35, width=720, height=540)
        self.scrollbary = Scrollbar(orient=VERTICAL)
        self.scrollbary.place(relx=0.82, rely=0.351, width=22, height=538)

        self.tree.configure(columns=("Sender", "Message Content"))

        self.tree.heading("Sender", text="Sender", anchor=W)
        self.tree.heading("Message Content", text="Message Content", anchor=W)


        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        self.tree.column("#1", stretch=NO, minwidth=0, width=190)



        with conn.cursor() as cur:
            #cur.execute("CREATE TABLE IF NOT EXISTS Invoice (invoiceId INT8 NOT NULL, customerName STRING NOT NULL, contactNumber INT8 NOT NULL, customerAddress STRING NOT NULL, purchaseDate DATE NOT NULL, CONSTRAINT Invoice_pkey PRIMARY KEY (invoiceId ASC))")
            #cur.execute("INSERT INTO Invoice (invoiceId, customerName, contactNumber, customerAddress, purchaseDate) VALUES (10000001, 'Diana Miel', '4809456325', '98432 N Deer Dr', '10-27-22')")
            cur.execute("SELECT * FROM emails")
            x = cur.fetchall()
            for dt in x:
                self.tree.insert("", 'end', iid=dt[0], text=dt[0], values =(dt[0],dt[1],dt[2],dt[4],dt[3]))

        conn.commit()

        self.app.mainloop()

    def logout(self):
        self.app.destroy()
        main()
    def inbox(self):
        pass
    def trash(self):
        pass
    def compose(self):
        compose()
    

class compose:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("New Message")
        self.app.geometry('400x400')
        self.app.resizable(width=False, height=False)
        self.app['background']='#187dd8'
        self.app.attributes('-alpha',0.97)
        self.main()
    def main(self):

        pass
main()