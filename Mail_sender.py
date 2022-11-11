import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import *
import mysql.connector as myconn
from tkinter import messagebox
import threading

l1 = []


####################     STARTER FUNCTION    ###################

def starter():
    global cur
    global conn
    global data
    conn = myconn.connect(
        host = "localhost",
        username = "root", 
        password = "",
        database = "email")
    
    quary = "select * from user_info"
    cur = conn.cursor()
    cur.execute(quary)
    data = cur.fetchall()
    if data == []:
        frame2.pack(fill=BOTH,expand=YES)
    else:
        frame1.pack(fill=BOTH,expand=YES)  



################################################################


def show_password():
    if pass_entry.cget('show') == "*":
        pass_entry.config(show='')
    else:
        pass_entry.config(show="*")


####################    SIGH IN FUNCTION    ##################


def sign_in():
    global conn
    global cur
    global info

    sign_in_button.config(command=threading.Thread(target=sign_in).start)

    user = user_entry.get()
    if user == "":
        messagebox.showerror("error","Please fill the gmail Section")
        
    elif "gmail.com" not in user :
        messagebox.showerror("Error","Please fill the gmail correctly")
    
    elif pass_entry.get() == "":
        messagebox.showerror("Error","Please fill the password section")

    else:
        query = "INSERT INTO user_info (username,passwd) values (%s,%s)"
        info = (user_entry.get(),pass_entry.get())

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(user_entry.get(), pass_entry.get())
        
        except:
            messagebox.showerror("Wrong Info","Check The Username or Password or The Internet Connection")
            return False

        cursor = conn.cursor()
        cursor.execute(query,info)
        conn.commit()

        user_entry.delete(0,END)
        pass_entry.delete(0,END)

        conn.close()

        frame2.pack_forget()
        frame1.pack(fill=BOTH,expand=YES)


###################    MESSAGE SENDER FUNCTION    ###############

def send_message():
    global data
    global info

    if "@gmail.com" not in address_entry.get():
        messagebox.showerror("Error","Please Fill The Sender Address Correctly")
        return False


    try:
        mail_content = email_body_entry.get()
        print(1)

        #The mail addresses and password

        sender_address = info[0][0]
        print(2)
        print(sender_address)

        sender_pass = data[0][1]
        print(3)

        receiver_address = str(address_entry.get())
        print(4)

        #Setup the MIME

        message = MIMEMultipart()
        print(5)

        message['From'] = sender_address

        message['To'] = receiver_address

        message['Subject'] = 'A test mail sent by Python. It has an attachment.'   #The subject line

        #The body and the attachments for the mail

        message.attach(MIMEText(mail_content, 'plain'))

        #Create SMTP session for sending the mail

        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port

        session.starttls() #enable security

        session.login(sender_address, sender_pass) #login with mail_id and password

        text = message.as_string()

        session.sendmail(sender_address, receiver_address, text)

        session.quit()

        success = Label(frame1,text="Sending Successfully")

        success.place(x=15,y=280)

    except:

        loss = Label(frame1,text = "Failed")

        loss.place(x=15,y=280)
        
    address_entry.delete(0,END)

    email_body_entry.delete(0,END)
    

##################   LOG OUT FUNCTION   ###############


def log_out():
    mess = messagebox.askyesno("Are You Sure","Are you sure you want to log out")
    if mess == True:
        quary = "delete from user_info"
        cur = conn.cursor()
        cur.execute(quary)
        conn.commit()
        print("done")
        frame1.pack_forget()
        frame2.pack(fill=BOTH,expand=YES)


root = Tk()

root.geometry("500x500")

root.title("Python Mail Sender App")

root.resizable(False,False)

frame1 = Frame(root)

frame2 = Frame(root,bg="pink")

starting = threading.Thread(target=starter).start()

############################    Frame1     ################################

heading = Label(frame1,text="Gmail Sending App",bg="yellow",fg="black",font="10",width="500",height="3")

heading.pack()

address_field = Label(frame1,text="Recipient Address :")
email_body_field = Label(frame1,text="Message :")

address_field.place(x=15,y=70)
email_body_field.place(x=15,y=140)

address = StringVar()
email_body = StringVar()


address_entry = Entry(frame1,textvariable=address,width="30")
email_body_entry = Entry(frame1,textvariable=email_body,width="30")

address_entry.place(x=15,y=100)
email_body_entry.place(x=15,y=180)

button = Button(frame1,text="Send Message",command=threading.Thread(target=send_message).start,width="30",height="2",bg="grey")

button.place(x=15,y=220)

button = Button(frame1,text="Log out",command=log_out,width="10",height="2",bg="grey")

button.place(x=420,y=60)

####################################################################################


################################  Frame2  ##########################################

heading = Label(frame2,text="Login First To Continue",bg="yellow",fg="black",width="500",height="2",font=("Candara Light",15,"bold"))

heading.pack()

address_field = Label(frame2,text="User Name :",bg="pink",font=("Ebrima",10))
email_body_field = Label(frame2,text="Password :",bg="pink",font=("Ebrima",10))

address_field.place(x=15,y=70)
email_body_field.place(x=15,y=140)



user_entry = Entry(frame2,width="30")
pass_entry = Entry(frame2,width="30",show="*")
checkbox = Checkbutton(frame2,text= "show password",command=show_password,bg="pink",activebackground="pink")

user_entry.place(x=15,y=100)
pass_entry.place(x=15,y=180)
checkbox.place(x=200,y=180)

sign_in_button = Button(frame2,text="Sign in",command=threading.Thread(target=sign_in).start,width="30",height="2",bg="grey",activeforeground="gray")

sign_in_button.place(x=15,y=220)

root.mainloop()