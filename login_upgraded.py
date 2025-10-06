import os , tkinter.messagebox as tsmg
from cryptography.fernet import Fernet
from tkinter import *
import cv2
from PIL import Image ,ImageTk

if not(os.path.exists("login")):
        os.mkdir("login")
       
def masterkey():
    os.chdir("login")
    if not (os.path.exists("masterkey.key")):
        key = Fernet.generate_key()
        with open("masterkey.key" , "wb") as f:
            f.write(key)
    else:
        with open("masterkey.key" , "rb") as f:
            key = f.read()
    return key
        
clipher = Fernet(masterkey())

def add_user(user,pas):
    if f"{user}.key" in os.listdir():
          return False
    else:
          token = clipher.encrypt(pas.encode())
          with open(f"{user}.key","wb") as f :
               f.write(token)
    return True

def del_user(name):
    if f"{name}.key" in os.listdir():
        os.remove(f"{name}.key")
        return True
    else :
        return False

def check_pass(user,pas):
     if f"{user}.key" in os.listdir():
            with open(f"{user}.key","rb") as f:
                token = f.read()
            password =  clipher.decrypt(token).decode()
            if pas==password:
                 return True
            else : 
                 return False
        
root=Tk()

root.geometry("1000x600")
root.minsize(width=1000,height=600)
root.maxsize(width=1000,height=600)

os.chdir("..")
VIDEO_PATH = "background.mp4" 
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise FileNotFoundError("Video file not found or cannot be opened.")

video_label = Label(root)
video_label.pack(fill="both", expand=True)

def update_video():
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()

    frame = cv2.resize(frame, (1000, 600))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = ImageTk.PhotoImage(Image.fromarray(frame))
    video_label.config(image=img)
    video_label.image = img

    root.after(33, update_video)

update_video() 

frame1 = Frame(master=root , borderwidth=6, relief=SUNKEN, background="grey", width=500, height=100)
frame1.place(relx=0.5, rely=0.15, anchor="center")

frame2 = Frame(root , borderwidth=6, relief=SUNKEN, background="grey", width=500, height=200)
frame2.place(relx=0.5, rely=0.5, anchor="center")

username = StringVar()
password = StringVar()

signin=False
def sign():
     global signin
     signin=True
     lab.config(text="Sign In")
     btn1.destroy()
     btn.destroy()

login = "Sign in" if signin else "Login"

lab= Label(master=frame1,text=login,font=("patrickhand",60,"bold"),pady=5,padx=70,bg="grey")
lab.pack()

Label(frame2,text="Username : ",font=("patrickhand",32),pady=5,padx=20,bg="grey").grid(row=1,column=1)
Label(frame2,text="    ",pady=5,bg="grey").grid(row=1,column=3)
Entry(frame2,textvariable=username,bg="white",fg="black",font=("patrickhand",16,"bold")).grid(row=1,column=2)

Label(frame2,text="Password : ",font=("patrickhand",32),pady=5,padx=20,bg="grey").grid(row=2,column=1)
Label(frame2,text="    ",pady=5,bg="grey").grid(row=2,column=3)
Entry(frame2,textvariable=password,bg="white",fg="black",show="*",font=("patrickhand",16,"bold")).grid(row=2,column=2)

def login():
    user = username.get().strip()
    passw = password.get().strip()
    if not user or not passw:
        tsmg.showerror("Error", "Please enter both username and password.")
        return

    if check_pass(user, passw):
        frame1.destroy()
        frame2.destroy()
        btn.destroy()   
        btn1.destroy() 
        tsmg.showinfo("Success", f"Welcome, {user}!")
        root.quit()
    else:
        tsmg.showerror("Login Failed", "Incorrect username or password.")
        username.set("")
        password.set("")


btn1= Button(root,text="Login",font=("patrickhand",32),bg="grey",padx=20,command=login)
btn1.place(x=360,y=450)

def add():
    user = username.get().strip()
    passw = password.get().strip()
    if add_user(user,passw):
         frame1.destroy()
         frame2.destroy()
         btn.destroy()   
         btn1.destroy()      
         tsmg.showinfo("LOGIN","USER CREATED")  
         root.quit()
    else:
        tsmg.showerror("LOGIN","USERNAME EXIST .")
        username.set("")
        password.set("")

def create():
     btn = Button(root,text="Create",font=("patrickhand",32),bg="grey",padx=20,command=add)
     btn.place(x=420,y=450)

btn = Button(root,text="Sign",font=("patrickhand",32),bg="grey",padx=20,command=lambda:[sign(),create()])
btn.place(x=530,y=450)


root.mainloop()

cap.release()

 
