import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk,Image
from tkinterdnd2 import DND_FILES, TkinterDnD
import check
import crypto
import os
import linecache


currentusername='2'
currentpwd='2'
class App(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        page = tk.Frame(self)
        page.pack()
        ##

        ##
        page.grid_rowconfigure(0,minsize=600)
        page.grid_columnconfigure(0,minsize=900)
        self.frame = {}
        for i in(Loginpage,Homepage,Downloadpage,Deletepage,Decryptionpage):
            frame = i(page,self)
            self.frame[i]=frame
            self.resizable(False,False)
            frame.grid(row =0,column=0,sticky="nsew")
        self.show(Loginpage)


    def show(self,c):
        frame = self.frame[c]
        frame.tkraise()

        self.title("iSAFE")


class Loginpage(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        imageopen = Image.open("b444.jpg")
        background = ImageTk.PhotoImage(imageopen)
        background_label = tk.Label(self,image=background)
        background_label.image=background
        background_label.place(x=0,y=0,relwidth=1, relheight=1)


        Label = tk.Label(self,text="iSAFE",font=("Impact",30),bg="white").place(x=120,y=50)

        username_label=tk.Label(self,text="Username",font=("Goudy old style",20),bg="gray").place(x=60,y=120)
        username_entry=tk.Entry(self,width=30,bd=2)
        username_entry.place(x=60,y=160)

        pwd_label=tk.Label(self,text="Password",font=("Goudy old style",20),bg="gray").place(x=60,y=200)
        pwd_entry=tk.Entry(self,width=30,show="*",bd=2)
        pwd_entry.place(x=60,y=240)

        global currentusername
        currentusername= username_entry.get()
        global currentpwd
        currentpwd = pwd_entry.get()

        def login_check():
            if (check.login(username_entry.get(),pwd_entry.get())):
               controller.show(Homepage)
            else:
                messagebox.showinfo("Error","Username or Password is wrong!")
        def register_check():
            if len(username_entry.get())==0 or len(pwd_entry.get())==0:
                messagebox.showinfo("Error", "username or password can not be empty!")
            else:
                check.register(username_entry.get(),pwd_entry.get())
                messagebox.showinfo("Success", "registration compelte")

        loginButton = tk.Button(self,text=" Login ",font=("Impact",20),command=login_check).place(x=60,y=300)
        registerButton = tk.Button(self,text="Register",font=("Impact",20),command=register_check).place(x=160,y=300)
        #questionimage = ImageTk.PhotoImage(Image.open("questionmark.png"))
        #questionButton = tk.Button(self,image=questionimage)
        #questionButton.place(x=120,y=120,relwidth=0.5, relheight=0.5)




class Homepage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #set background

        imageopen = Image.open("b6.jpg")
        background = ImageTk.PhotoImage(imageopen)
        background_label = tk.Label(self, image=background)
        background_label.image = background
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        Label = tk.Label(self, text="Home", font=("Impact", 35),bg="lightgray").place(x=375, y=50)
        title = tk.Label(self, text="Welcome to iSAFE", font=("Impact", 18, "bold"), fg="black", bg="white").place(x=420,                                                                                                          y=200)
        title2 = tk.Label(self, text="We give the best security to you", font=("Arial", 10, "bold"), fg="black").place(
            x=380, y=260)
        def logout_check():
            answer = tk.messagebox.askyesno(title='logout confirmation',message='Are you sure you want to log out?')
            if answer:
               controller.show(Loginpage)

        SignoutButton = tk.Button(self, text="sign out", font=("Impact", 10),
                                  command=logout_check).place(x=830, y=20)

        def uploadpage():
            ##open a new window for drag event
            root = TkinterDnD.Tk()
            root.geometry("900x600")
            #drag file method
            def drop_file(event):
                listb.insert("end", event.data)
                print(event.data)
                global  filename
                filename=event.data
                #fname = open("filenamesent.txt", "a+")
                #fname.write(filename + "\n")
                print(filename)

##keep track of the current user
            def upload():
                file = open("current.txt","r")
                count=0
                for line in file:
                    if line != "\n":
                        count+=1
                last_line=linecache.getline("current.txt",count)
                n, p = last_line.split(",")
                p = p.strip()
                file.close()
                #call upload methond in crypto
                crypto.uploadmain(filename,n,p)
                messagebox.showinfo("Success", "File uploaded")
##drag window set
            listb = tk.Listbox(root, selectmode=tk.SINGLE, background="lightgray")
            listb.pack(fill=tk.X)
            listb.drop_target_register(DND_FILES)
            listb.dnd_bind("<<Drop>>", drop_file)
            upload = tk.Button(root,text="upload",font=("Impact",20),command=upload).place(x=500,y=500)

        Button = tk.Button(self, text="Upload File", font=("Impact", 20),
                           command=uploadpage).place(x=140, y=180)

        ######download
        def downloadpage():
            controller.show(Downloadpage)
        def deletefilepage():
            controller.show(Deletepage)

        Button2 = tk.Button(self, text="Download File", font=("Impact", 20),
                           command=downloadpage).place(x=140, y=260)
        Button3 = tk.Button(self, text="Delete File", font=("Impact", 20),
                           command=deletefilepage).place(x=140, y=340)
        DecryptionButton = tk.Button(self, text="Decrypt file", font=("Impact", 20),
                                     command=lambda: controller.show(Decryptionpage)).place(x=140, y=420)


class Downloadpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        imageopen = Image.open("b6.jpg")
        background = ImageTk.PhotoImage(imageopen)
        background_label = tk.Label(self, image=background)
        background_label.image = background
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        listbox = tk.Listbox(self,width=45,height=10)
        listbox.place(x=380,y=200)
        listbox2 = tk.Listbox(self,width=15,height=10)
        listbox2.place(x=680,y=200)
        def logout_check():
            answer = tk.messagebox.askyesno(title='logout confirmation',message='Are you sure you want to log out?')
            if answer:
               controller.show(Loginpage)

        #load the list box with file name in the storage
        def ref():
            file = open("current.txt", "r")
            countl = 0
            for cline in file:
                if cline != "\n":
                    countl += 1
            last_line = linecache.getline("current.txt", countl)
            n, p = last_line.split(",")
            p = p.strip()
            ##get filelist from serverlist
            countfile =0
            flist=crypto.getlist(n,p)
            for i in flist:
                countfile+=1
            print(n, p)
            listbox.delete(0, tk.END)
            print(countfile)
            #insert all item into listbox from serverlist
            for i in range(0,countfile):
                listbox.insert(i,flist[i])
            print("listbox:")
            print(listbox.get(0, tk.END))

        def plaintnameEvent():
            listbox2.delete(0, tk.END)
            for i in range(len(listbox.get(0, tk.END))):
                listbox2.insert(i,crypto.macfile_exist(listbox.get(0, tk.END)[i]))



## get selected file and send request download file
        def selected():
            selectedfilename = listbox.get(tk.ACTIVE)
            print(selectedfilename)
            file = open("current.txt", "r")
            countl=0
            for cline in file:
                if cline != "\n":
                    countl += 1
            last_line = linecache.getline("current.txt", countl)
            n, p = last_line.split(",")
            p = p.strip()
            checking=False
            crypto.download(selectedfilename, n, p,checking)
            messagebox.showinfo("Success", "File downloaded")

            file.close()



        SelectButton = tk.Button(self,text="download",font=("Impact",20),command=selected).place(x=450,y=400)
        refreshButton = tk.Button(self,text="refresh",font=("Impact",10),command=ref).place(x=595,y=170)
        plaintnameButton = tk.Button(self,text="plaint",font=("Impact",10),command=plaintnameEvent).place(x=700,y=170)


        Label = tk.Label(self, text="Downloadfile", font=("Impact", 30)).place(x=350, y=40)

        UploadButton = tk.Button(self, text="Upload file", font=("Impact", 20),
                           command=lambda: controller.show(Homepage)).place(x=125, y=220)
        HomeButton = tk.Button(self, text="Home", font=("Impact", 20),
                           command=lambda: controller.show(Homepage)).place(x=150, y=150)
        SignoutButton = tk.Button(self, text="sign out", font=("Impact", 10),
                           command=logout_check).place(x=830, y=20)
        DeletepageButton = tk.Button(self, text="Delete file", font=("Impact", 20),
                                  command=lambda: controller.show(Deletepage)).place(x=125, y=290)
        DecryptionButton = tk.Button(self, text="Decrypt file", font=("Impact", 20),
                                     command=lambda: controller.show(Decryptionpage)).place(x=125, y=360)

class Deletepage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        imageopen = Image.open("b6.jpg")
        background = ImageTk.PhotoImage(imageopen)
        background_label = tk.Label(self, image=background)
        background_label.image = background
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        listbox = tk.Listbox(self, width=45, height=10)
        listbox.place(x=380, y=200)
       # listbox.pack()
        # load the list box with file name in the storage
        listbox2 = tk.Listbox(self, width=15, height=10)
        listbox2.place(x=680, y=200)
        def logout_check():
            answer = tk.messagebox.askyesno(title='logout confirmation',message='Are you sure you want to log out?')
            if answer:
               controller.show(Loginpage)
        # load the list box with file name in the storage
        def ref():
            file = open("current.txt", "r")
            countl = 0
            for cline in file:
                if cline != "\n":
                    countl += 1
            last_line = linecache.getline("current.txt", countl)
            n, p = last_line.split(",")
            p = p.strip()
            ##get filelist from serverlist
            countfile = 0
            flist = crypto.getlist(n, p)
            for i in flist:
                countfile += 1
            print(n, p)
            listbox.delete(0, tk.END)
            print(countfile)
            # insert all item into listbox from serverlist
            for i in range(0, countfile):
                listbox.insert(i, flist[i])
            print("listbox:")
            print(listbox.get(0, tk.END))

        def plaintnameEvent():
            listbox2.delete(0, tk.END)
            for i in range(len(listbox.get(0, tk.END))):
                listbox2.insert(i, crypto.macfile_exist(listbox.get(0, tk.END)[i]))

        ## get selected file and send request download file
        def deletefile():
            selectedfilename = listbox.get(tk.ACTIVE)
            selectedindex = listbox.curselection()
            if len(selectedindex)==0:
                messagebox.showerror("Error", "File not exist")
            else:
                dindex = selectedindex[0]
                file = open("current.txt", "r")
                count=0
                checking=False
                for line in file:
                    if line != "\n":
                        count += 1
                last_line = linecache.getline("current.txt", count)
                n, p = last_line.split(",")
                p = p.strip()
                print(dindex)
                print(selectedfilename)
                ##alert for delete behaviour
                answer = tk.messagebox.askyesno(title='delete confirmation',message='There is no recover after delete, are you sure you want to delete?')
                if answer:
                    crypto.delete(selectedfilename,n,p)
                    listbox.delete(dindex,checking)
                    messagebox.showinfo("Success", "File deleted")


                file.close()

        SelectButton = tk.Button(self,text="delete",font=("Impact",20),command=deletefile).place(x=450,y=400)
        refreshButton = tk.Button(self,text="refresh",font=("Impact",10),command=ref).place(x=595,y=170)
        plaintnameButton = tk.Button(self, text="filename refresh", font=("Impact", 10), command=plaintnameEvent).place(x=680,
                                                                                                              y=170)

        Label = tk.Label(self, text="Deletefile", font=("Impact", 30)).place(x=350, y=40)

        HomeButton = tk.Button(self, text="Home", font=("Impact", 20),
                           command=lambda: controller.show(Homepage)).place(x=150, y=150)
        UploadButton = tk.Button(self, text="Upload file", font=("Impact", 20),
                           command=lambda: controller.show(Homepage)).place(x=125, y=220)
        DownloadButton = tk.Button(self, text="Download file", font=("Impact", 20),
                                 command=lambda: controller.show(Downloadpage)).place(x=125, y=290)
        DecryptionButton = tk.Button(self, text="Decrypt file", font=("Impact", 20),
                                   command=lambda: controller.show(Decryptionpage)).place(x=125, y=360)
        SignoutButton = tk.Button(self, text="sign out", font=("Impact", 10),
                           command=logout_check).place(x=830, y=20)

class Decryptionpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        imageopen = Image.open("b6.jpg")
        background = ImageTk.PhotoImage(imageopen)
        background_label = tk.Label(self, image=background)
        background_label.image = background
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        listbox = tk.Listbox(self, width=45, height=10)
        listbox.place(x=380, y=200)
       # listbox.pack()
        # load the list box with file name in the storage
        listbox2 = tk.Listbox(self, width=15, height=10)
        listbox2.place(x=680, y=200)

        # load the list box with file name in the storage
        def decryption():
            selectedfilename = listbox.get(tk.ACTIVE)
            crypto.AES_GCM_Decrypt(selectedfilename)
            messagebox.showinfo("Success", "File decryption compelted")

        def plaintnameEvent():
            listbox2.delete(0, tk.END)
            for i in range(len(listbox.get(0, tk.END))):
                listbox2.insert(i, crypto.macfile_exist(listbox.get(0, tk.END)[i]))
        def logout_check():
            answer = tk.messagebox.askyesno(title='logout confirmation',message='Are you sure you want to log out?')
            if answer:
               controller.show(Loginpage)
        def ref():
            file = open("current.txt", "r")
            countl = 0
            for cline in file:
                if cline != "\n":
                    countl += 1
            last_line = linecache.getline("current.txt", countl)
            n, p = last_line.split(",")
            p = p.strip()
            ##get filelist from serverlist
            countfile =0
            flist=crypto.getlist(n,p)
            for i in flist:
                countfile+=1
            print(n, p)
            listbox.delete(0, tk.END)
            print(countfile)
            #insert all item into listbox from serverlist
            for i in range(0,countfile):
                listbox.insert(i,flist[i])
            print("listbox:")
            print(listbox.get(0, tk.END))
        SelectButton = tk.Button(self,text="Decrypt",font=("Impact",20),command=decryption).place(x=450,y=400)


        Label = tk.Label(self, text="Decrypt file", font=("Impact", 30)).place(x=350, y=40)

        HomeButton = tk.Button(self, text="Home", font=("Impact", 20),
                           command=lambda: controller.show(Homepage)).place(x=150, y=150)
        UploadButton = tk.Button(self, text="Upload file", font=("Impact", 20),
                           command=lambda: controller.show(Homepage)).place(x=125, y=220)
        DownloadButton = tk.Button(self, text="Download file", font=("Impact", 20),
                                 command=lambda: controller.show(Downloadpage)).place(x=125, y=290)
        DeletepageButton = tk.Button(self, text="Delete file", font=("Impact", 20),
                                     command=lambda: controller.show(Deletepage)).place(x=125, y=360)
        refreshButton = tk.Button(self,text="refresh",font=("Impact",10),command=ref).place(x=595,y=170)
        plaintnameButton = tk.Button(self, text="filename refresh", font=("Impact", 10), command=plaintnameEvent).place(
            x=680,
            y=170)

        SignoutButton = tk.Button(self, text="sign out", font=("Impact", 10),
                           command=logout_check).place(x=830, y=20)

app=App()
app.mainloop()
