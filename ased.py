from customtkinter import *
from PIL import Image
import tkinter.messagebox as mb
import mariadb
import csv
import re


try:
    connection = mariadb.connect(
        host='ased00.duckdns.org',
        database='tkiter',
        user='ased',
        password='ased',
        port=3306
    )
except mariadb.Error as e:
    error_app = CTk()
    error_app.geometry("450x300")
    error_label = CTkLabel(
        error_app,
        text="Server Error: \nCheck your INTERNET connection\n or try again later <3",
        fg_color='transparent',
        text_color="red",
        bg_color="transparent",   
        font=("Comic Sans MS",16, "bold"),
    ).place(x=100,y=90)
    ok_button = CTkButton(
        error_app,
        text="ok",
        width=100,
        height=25,
        fg_color="#FFD369",
        hover_color="#E6BF5E",
        text_color="#222831",
        corner_radius=5,
        font=("Comic Sans MS", 12,),
        cursor="hand2",
        command = exit
    ).place(x=180, y= 170)

    error_app.mainloop()
    exit()



SELECTED_NOTE = None
try:
    with open("selected_note.csv", "r", newline="") as file5:
        reader = csv.reader(file5)
        row = next(reader)
        selectednote = row[0]
        if selectednote == "":
            SELECTED_NOTE = None
        else:
            SELECTED_NOTE = selectednote
except:
    with open("selected_note.csv", "w", newline="") as file6:
        writer = csv.writer(file6)
        writer.writerow([""])


USER_ID = None
try:
    with open("login_state.csv", "r", newline="") as file0:
        reader = csv.reader(file0)
        row = next(reader)
        usrid = row[2]
        if usrid == "":
            USER_ID = None
        else:
            USER_ID = usrid
except:
    with open("login_state.csv", "w", newline="") as file3:
        writer = csv.writer(file3)
        writer.writerow(["0", "", ""])

USER_NAME = None
try:
    with open("login_state.csv", "r", newline="") as file1:
        reader = csv.reader(file1)
        row = next(reader)
        usrname = row[1]
        if usrname == "":
            USER_NAME = None
        else:
            USER_NAME = usrname
except:
    with open("login_state.csv", "w", newline="") as file2:
        writer = csv.writer(file2)
        writer.writerow(["0", "", ""])

img_user = Image.open("user.png")
img_password = Image.open("password.png")
user_image = CTkImage(light_image=img_user,dark_image=img_user)
password_image = CTkImage(light_image=img_password,dark_image=img_password)


class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x555")
        self.title("Custom Note App")
        self.current_frame = None


        try:
            with open("login_state.csv", "r", newline="") as file:
                reader = csv.reader(file)
                row = next(reader)
                if row[0] == "0":
                    self.switch_frame(LoginingFrame)
                else:
                    self.switch_frame(BaseMenu)
        except:
            self.switch_frame(LoginingFrame)


    def switch_frame(self, new_frame):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame(self)
        self.current_frame.pack(pady=20, padx=20, expand= True)


class LoginingFrame(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(width=335, height=240)

        self.lab1 = CTkLabel(self, text='', image=user_image).place(y=70,x=50)
        self.lab2 = CTkLabel(self, text='', image=password_image).place(y=110,x=50)

        self.title = CTkLabel(
            self,
            text="Log In",
            font=("Comic Sans MS", 20, "bold"),
            text_color="#FFD369"
        )
        self.title.place(x=135, y=20)

        self.usr_entry = CTkEntry(
            self,
            width=200,
            fg_color="#393e46",
            border_width=0,
            border_color="grey",
            text_color="#EEEEEE",
            placeholder_text="username",
            placeholder_text_color="grey",
            font=("Comic Sans MS", 17),
            corner_radius=5,
        )
        self.usr_entry.place(x=75,y=70)

        self.password_entry = CTkEntry(
            self,
            width=200,
            fg_color="#393e46",
            border_width=0,
            border_color="grey",
            text_color="#EEEEEE",
            placeholder_text="password",
            placeholder_text_color="grey",
            font=("Comic Sans MS", 17),
            corner_radius=5,
        )
        self.password_entry.place(x=75,y=110)

        self.phrase = CTkLabel(
            self,
            text="Don't have an account ?",
            text_color="grey",
            font=("Comic Sans MS",12, "bold"),
        )
        self.phrase.place(x=57, y=200)

        self.creat_button = CTkButton(
            self,
            width=1,
            height=1,
            fg_color='transparent',
            text="Creat account",
            text_color="#FFD369",
            bg_color="transparent",
            cursor="hand2",    
            hover=DISABLED,
            font=("Comic Sans MS",12, "bold"),
            command= lambda: self.parent.switch_frame(SignupFrame)
        )
        self.creat_button.place(x=202, y=202)

        
        self.error_lab = CTkLabel(
            self,
            text="",
            text_color="red",
            font=("Comic Sans MS",12, "bold"),
        )
        self.error_lab.place(x=100, y=140)

        self.sign_button = CTkButton( 
            self,
            text="Log In",
            width=100,
            height=25,
            fg_color="#FFD369",
            hover_color="#E6BF5E",
            text_color="#222831",
            corner_radius=5,
            font=("Comic Sans MS", 12,),
            cursor="hand2",
            command = self.signin_functions
        )
        self.sign_button.place(x=125, y= 170)


    
    def signin_functions(self):
        cursor = connection.cursor()
        usr = self.usr_entry.get()
        password = self.password_entry.get()
        cursor.execute("SELECT username, password, id FROM users")
        rows = cursor.fetchall()
        cursor.close()


        if not usr:
            self.error_lab.configure(text="* enter a user name")
            self.usr_entry.configure(border_width=1, border_color="red")
            return
        elif not any(row[0] == usr for row in rows):
            self.error_lab.configure(text="* User name not exist")
            self.usr_entry.configure(border_color="red", border_width=1)
            return
        #check if user name is existe in the database 

        for row in rows:
            if row[0] == usr:
                if row[1] != password:
                    self.error_lab.configure(text="* Incorrect password")
                    self.usr_entry.configure(border_width=1,border_color="green")
                    self.password_entry.configure(border_width=1,border_color="red")
                    return
            #after all checking go to base menu
        global USER_ID     
        for row in rows:
            if row[0] == usr:
                USER_ID = row[2]
        global USER_NAME
        USER_NAME = self.usr_entry.get()

        with open("login_state.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["1", USER_NAME, USER_ID])
        self.parent.switch_frame(BaseMenu)

class SignupFrame(LoginingFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(height=280)

        self.title.configure(text= "Sign Up")
        self.phrase.configure(text="Already have an Account ?")
        self.phrase.place(x=57 , y=240)

        self.creat_button.configure(text= "Login page", command= lambda: self.parent.switch_frame(LoginingFrame))
        self.creat_button.place(x=215, y=242)

        self.sign_button.configure(
            text="Sign Up",
            command= lambda: self.signup_functions(self.password_entry.get(), self.rewrite.get(), self.usr_entry.get())
        )
        self.sign_button.place(x=125,y=210)
        self.rewrite = CTkEntry(
            self,
            width=200,
            fg_color="#393e46",
            border_width=0,
            border_color="grey",
            text_color="#EEEEEE",
            placeholder_text="Rewrite password",
            placeholder_text_color="grey",
            font=("Comic Sans MS", 17),
            corner_radius=5,
        )
        self.rewrite.place(x=75,y=150)
    
        self.lab = CTkLabel(
            self,
            text="",
            image=password_image
        )
        self.lab.place(x=50,y=150)

        self.error_lab.place(x= 100, y= 180)


    def signup_functions(self, gaps1, gaps2, usr):
        usr_pattern = r"^[a-zA-Z][a-zA-Z0-9._]{2,19}$"     
        password_pattern = r"^[^\s]{8,}$"  
        cursor = connection.cursor()
        cursor.execute("SELECT username FROM users")
        rows = cursor.fetchall()
        cursor.close()
        

        if not re.match(usr_pattern, usr):
            self.error_lab.configure(text= "* enter valid user name")
            self.usr_entry.configure(border_color="red", border_width=1)
            return
        elif any(row[0] == usr for row in rows):
            self.error_lab.configure(text= "* User name taken")
            self.usr_entry.configure(border_color="red", border_width=1)
            return
        elif not re.match(password_pattern, gaps1):
            self.password_entry.configure(border_color="red", border_width=1)
            self.usr_entry.configure(border_color="green", border_width=1)
            self.error_lab.configure(text="* at least 8 chars for password (no spaces)")
            self.error_lab.place(x=50, y= 180)
            return
        elif gaps1 != gaps2:
            self.usr_entry.configure(border_color="green", border_width=1)
            self.password_entry.configure(border_color="green", border_width=1)
            self.rewrite.configure(border_color="red", border_width=1)
            self.error_lab.configure(text= "* Password doesn't match")
            return
        #check if user name is already taken in the database            
        
        #after all checking go to base menu
        cursor2 = connection.cursor()
        query= "INSERT INTO users (username, password) VALUES (%s, %s)"
        values = (usr, gaps1)
        cursor2.execute(query, values)
        connection.commit()
        cursor2.close()

        cursor3 = connection.cursor()
        cursor3.execute("SELECT username, id FROM users")
        rows = cursor3.fetchall()
        cursor3.close()
        global USER_ID     

        for row in rows:
            if row[0] == usr:
                USER_ID = row[1]
        global USER_NAME
        USER_NAME = usr

        with open("login_state.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["1", USER_NAME, USER_ID])

        self.parent.switch_frame(BaseMenu)


class BaseMenu(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.fg_color="transparent"
        self.configure(width=200, height=222)

        self.lab1 = CTkLabel(self, text='', image=user_image).place(y=5,x=5)

        self.username = CTkLabel(
            self,
            text=USER_NAME,
            text_color= "grey",
            font=("Comic Sans MS", 12, "bold"),
        )
        self.username.place(x=30,y=8)

        self.creat_note = CTkButton(
            self,
            text="Create Note",
            width=100,
            height=25,
            fg_color="#FFD369",
            hover_color="#E6BF5E",
            text_color="#222831",
            corner_radius=5,
            font=("Comic Sans MS", 12,),
            cursor="hand2",
            command= lambda: self.parent.switch_frame(NewNote)
        )
        self.creat_note.place(x= 50, y=70)

        self.mynotes = CTkButton(
            self,
            text="My Notes",
            width=100,
            height=25,
            fg_color="#FFD369",
            hover_color="#E6BF5E",
            text_color="#222831",
            corner_radius=5,
            font=("Comic Sans MS", 12,),
            cursor="hand2",
            command= lambda: self.parent.switch_frame(MyNotes)
        )
        self.mynotes.place(x= 50, y=110)

        self.logout = CTkButton(
            self,
            text="Log Out",
            width=50,
            height=25,
            fg_color="grey",
            hover_color="#E6BF5E",
            text_color="#222831",
            corner_radius=5,
            font=("Comic Sans MS", 12,),
            cursor="hand2",
            command= self.log_out
        )
        self.logout.place(x= 140, y=8)

        self.exit_button = CTkButton(
            self,
            text="Exit",
            width=100,
            height=25,
            fg_color="grey",
            hover_color="#E6BF5E",
            text_color="#222831",
            corner_radius=5,
            font=("Comic Sans MS", 12,),
            cursor="hand2",
            command= self.exit_fun
        )
        self.exit_button.place(x= 50, y=150)

        self.delete_account = CTkButton(
            self,
            fg_color="transparent",
            height=1,
            width=1,
            text="Delete my account !",
            text_color="red",
            font=("Comic Sans MS", 10,),
            hover=DISABLED,
            cursor= "hand2",
            command= self.delete_account_function
        )
        self.delete_account.place(x= 100, y= 200)
    

    def delete_account_function(self):
        answer = mb.askyesno("Delete Account", "Are you sure you want to delete your account ?")
        if not answer:
            return
        answer= mb.askyesno("Advertisment", "All your notes will be deleted, do you want to continue ?")
        if not answer:
            return
        
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE username = %s", (USER_NAME,))
        connection.commit()
        cursor.close()
        with open("login_state.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["0", "", ""])
        self.parent.switch_frame(LoginingFrame)


    def log_out(self):
        answer = mb.askyesno("Log Out", "Are you sure you want to Log Out ?")
        if answer:
            with open("login_state.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["0", "", ""])
            self.parent.switch_frame(LoginingFrame)
        else:
            return
        
    
    def exit_fun(self):
        answr = mb.askyesno("Exit", "Are you sure you want to Exit ?")
        if answr:
            sys.exit()
        else:
            return
    

class NewNote(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(height= 500, width= 460)

        self.notename_lbl = CTkLabel(
            self,
            text="Enter title for your note:",
            text_color="#FFD369",
            font=("Comic Sans MS",12, "bold"),
        )
        self.notename_lbl.place(x=30 , y= 10)

        self.notname_entry = CTkEntry(
            self,
            width=300,
            fg_color="#393e46",
            border_width=0,
            border_color="grey",
            text_color="#EEEEEE",
            placeholder_text="title",
            placeholder_text_color="grey",
            font=("Comic Sans MS", 17),
            corner_radius=5,
        )
        self.notname_entry.place(x=20,y=40)

        self.content_lbl = CTkLabel(
            self,
            text="Write some Content for your Note:",
            text_color="#FFD369",
            font=("Comic Sans MS",12, "bold"),
        )
        self.content_lbl.place(x=30 , y= 80)        
        
        self.content_box = CTkTextbox(
            self,
            height= 330,
            width= 420,
            fg_color="#3B3F45",
            text_color="#EEEEEE",
            font=("Comic Sans MS",16),            
        )
        self.content_box.place(x=20, y= 111)

        self.return_button = CTkButton(
            self,
            text="Return",
            width=130,
            height=25,
            fg_color="grey",
            hover_color="#E6BF5E",
            text_color="#222831",
            corner_radius=5,
            font=("Comic Sans MS", 14,),
            cursor="hand2",
            command= self.return_fun
        )
        self.return_button.place(x=80 , y=455)

        self.save_button = CTkButton(
            self,
            text="Save",
            width=130,
            height=25,
            fg_color="#FFD369",
            hover_color="#E6BF5E",
            text_color="#222831",
            corner_radius=5,
            font=("Comic Sans MS", 14,),
            cursor="hand2",
            command=self.save_fun
        )
        self.save_button.place(x=240, y= 455)

        self.error_lab = CTkLabel(
            self,
            text="",
            text_color="red",
            font=("Comic Sans MS",12, "bold"),
        )
        self.error_lab.place(x=190, y=10)


    def return_fun(self):
        answer = mb.askyesno("Return", "Are you sure you want to Return ?")
        if answer:
            self.parent.switch_frame(BaseMenu)
        else:
            return


    def save_fun(self):
        target = (int(USER_ID),)
        query1 = "SELECT note_title, user_id FROM notes WHERE user_id = %s"
        cursor = connection.cursor()
        cursor.execute(query1, target)
        rows = cursor.fetchall()
        cursor.close()

        if self.notname_entry.get() == "" :
            self.error_lab.place(x=190, y=10)
            self.error_lab.configure(text="* empty title")
            return
        elif any(row[0] == self.notname_entry.get() for row in rows):
            self.error_lab.place(x=190, y=10)
            self.error_lab.configure(text="* Already have Note with this Title")
            return
        elif self.content_box.get("0.0", "end-1c") == "" :
            self.error_lab.place(x= 245, y = 80)
            self.error_lab.configure(text="* empty content")
            return
        
        answer = mb.askyesno("Save", "Are you sure you want to Save ?")
        if answer:
            pass
        else :
            return

        query = '''
            INSERT INTO notes (note_title, note_content, user_id)
            VALUES (%s, %s, %s)
        '''
        values = (self.notname_entry.get(), self.content_box.get("1.0", "end-1c"), USER_ID)
        cursor2 = connection.cursor()
        cursor2.execute(query, values)
        connection.commit()
        cursor2.close()
        self.parent.switch_frame(BaseMenu)
            

class MyNotes(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(height=180 , width= 295)

        self.mynotes = CTkOptionMenu(
            self,
            fg_color="#FFD369",
            text_color="#222831",
            variable=StringVar(value="Select Note"),
            values= self.get_notes(),
            corner_radius=4,
            font=("Comic Sans MS", 14,),
            dropdown_font=("Comic Sans MS", 14,),
            button_hover_color="#3B3F45",
            button_color="grey",
            
        )
        self.mynotes.place(x=140, y=70)

        self.show_button = CTkButton(
            self,
            text="show",
            width=100,
            height=25,
            fg_color="#FFD369",
            hover_color="#E6BF5E",
            text_color="#222831",
            corner_radius=5,
            font=("Comic Sans MS", 14,),
            cursor="hand2",
            command= self.show_fun
        )
        self.show_button.place(x=20, y= 20)

        self.edit_button = CTkButton(
            self,
            text="Edit",
            width=100,
            height=25,
            fg_color="#FFD369",
            hover_color="#E6BF5E",
            text_color="#222831",
            corner_radius=5,
            font=("Comic Sans MS", 14,),
            cursor="hand2",
            command= self.edit_fun
        )
        self.edit_button.place(x=20, y=60)

        self.delete_button = CTkButton(
            self,
            text="Delete",
            width=100,
            height=25,
            fg_color="#FFD369",
            hover_color="#E6BF5E",
            text_color="#222831",
            corner_radius=5,
            font=("Comic Sans MS", 14,),
            cursor="hand2",
            command= self.delete_fun
        )
        self.delete_button.place(x=20, y= 100)

        self.return2_button = CTkButton(
            self,
            text="Return",
            width=100,
            height=25,
            fg_color="grey",
            hover_color="#E6BF5E",
            text_color="#222831",
            corner_radius=5,
            font=("Comic Sans MS", 14,),
            cursor="hand2",
            command= lambda: self.parent.switch_frame(BaseMenu)
        )
        self.return2_button.place(x=20,y=140)


    def get_notes(self):
        value= (int(USER_ID),)
        query= "SELECT note_title FROM notes WHERE user_id = %s"
        cursor = connection.cursor()
        cursor.execute(query, value)
        notes = cursor.fetchall()
        cursor.close()
        list_notes = [note[0] for note in notes]   
        return list_notes


    def show_fun(self):
        selected_note = self.mynotes.get()

        cursor = connection.cursor()
        cursor.execute("SELECT note_title FROM notes WHERE user_id = %s", (int(USER_ID),))
        rows = cursor.fetchall()
        cursor.close()
        if not any(selected_note == row[0] for row in rows):
            return

        global SELECTED_NOTE
        SELECTED_NOTE = selected_note
        with open("selected_note.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([SELECTED_NOTE,])

        self.parent.switch_frame(ShowFrame)            
    
        
    def edit_fun(self):
        selected_note = self.mynotes.get()
        cursor = connection.cursor()
        cursor.execute("SELECT note_title FROM notes WHERE user_id = %s", (int(USER_ID),))
        rows = cursor.fetchall()
        cursor.close()
        if not any(selected_note == row[0] for row in rows):
            return

        global SELECTED_NOTE
        SELECTED_NOTE = selected_note
        with open("selected_note.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([SELECTED_NOTE,])

        self.parent.switch_frame(EditFrame)       


    def delete_fun(self):
        selected_note = self.mynotes.get()
        answer = mb.askyesno("Delete", "Are you sure you want to delete this NOTE ?")
        if not answer:
            return
        cursor = connection.cursor()
        cursor.execute("DELETE FROM notes WHERE note_title = %s", (selected_note,))
        connection.commit()
        cursor.close()
        self.parent.switch_frame(MyNotes)


class ShowFrame(NewNote):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.notename_lbl.configure(text="The title")
        self.content_lbl.configure(text="The content")
        self.notname_entry.insert("0", SELECTED_NOTE)        
        self.notname_entry.configure(state = DISABLED)
        self.save_button.destroy()
        self.return_button.configure(command = lambda: self.parent.switch_frame(MyNotes))
        self.return_button.place(x=160 , y=455)
        self.content_box.insert("1.0", self.get_content())
        self.content_box.configure(state=DISABLED)



    def get_content(self):
        cursor = connection.cursor()
        cursor.execute("SELECT note_content FROM notes WHERE note_title = %s", (SELECTED_NOTE,))
        rows = cursor.fetchall()
        cursor.close()
        content = rows[0][0]
        return content
        
class EditFrame(NewNote):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.notename_lbl.configure(text="The title")
        self.content_lbl.configure(text="The content")
        self.notname_entry.insert("0", SELECTED_NOTE)
        self.content_box.insert("1.0", self.bring_content())        
        self.save_button.configure(command= self.save_edit)
        self.return_button.configure(command = lambda: self.parent.switch_frame(MyNotes))

    def bring_content(self):
        cursor = connection.cursor()
        cursor.execute("SELECT note_content FROM notes WHERE note_title = %s", (SELECTED_NOTE,))
        rows = cursor.fetchall()
        cursor.close()
        content = rows[0][0]
        return content

    def save_edit(self):
        answer = mb.askyesno("Edit", "Are you sure you want to edit the note ?")
        if not answer:
            return
        
        cursor = connection.cursor()
        value=(self.notname_entry.get(), self.content_box.get("1.0", "end-1c"), SELECTED_NOTE)
        query='''
        UPDATE notes
        SET note_title = %s, note_content = %s
        WHERE note_title = %s
        '''
        cursor.execute(query, value)
        connection.commit()
        cursor.close()
        self.parent.switch_frame(MyNotes)

app = App()
app.mainloop()


connection.close()