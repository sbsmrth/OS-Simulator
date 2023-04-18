import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from persistence.model import Auth_User
import util.encoding_decoding as enc_dec
from persistence.repository.auth_user_repository import AuthUserRepository

class Register(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.auth_repository = AuthUserRepository()

        self.geometry("500x350")

        self.so_logo = ctk.CTkImage(dark_image=Image.open("./assets/skull.png"), size=(32, 32))
        self.button = ctk.CTkButton(self, image=self.so_logo, fg_color="transparent", text="Petya", font=("Roboto Medium",20),
                               hover=False)
        self.button.place(x=34, y=7)

        self.main_frame = RegisterFrame(master=self, login_reference=self, fg_color=self.cget("fg_color"))
        self.main_frame.pack(pady=50, padx=60, fill="both", expand=True)
    
    def destroyWindow(self):
        self.destroy()

class RegisterFrame(ctk.CTkFrame):
    def __init__(self, master, login_reference,**kwargs):
        super().__init__(master, **kwargs)    
        self.login_reference = login_reference
        
        self.login_label = ctk.CTkLabel(master=self, text="Create account", font=("Roboto Medium", 20, "bold"))
        self.login_label.pack(padx=0, pady=15)

        self.email_entry = ctk.CTkEntry(master=self, placeholder_text="Email", width=170)
        self.email_entry.pack(padx=0, pady=12)

        self.pass_entry = ctk.CTkEntry(master=self, placeholder_text="Password", show="*", width=170)
        self.pass_entry.pack(padx=0, pady=12)

        self.send_button = ctk.CTkButton(self, fg_color="red", text="Create account", font=("Roboto Medium", 16), hover=False, 
                                         command=self.register)
        self.send_button.pack(padx=0, pady=15)
    
    def getEmail(self):
        return self.email_entry.get()
    
    def getPassword(self):
        return self.pass_entry.get()
    
    def register(self):
        if not self.getEmail or not self.getPassword():
            messagebox.showerror(
                message="The fields are empty.", title="Error")
        else:                     
            user = Auth_User()
            user.email= self.getEmail()
            user_db: Auth_User = self.login_reference.auth_repository.getUserByEmail(
                self.getEmail()
            )
            
            if not (self.isUserRegister(user_db)):
                user.password = enc_dec.encrypted(self.getPassword())
                self.login_reference.auth_repository.insertUser(user)
                messagebox.showinfo(
                    message="User successfully created.", title="Message")     
                self.login_reference.destroyWindow()  

    def isUserRegister(self, user: Auth_User):
        status: bool = False
        if(user is not None):
            status = True
            messagebox.showerror(
                message="The user already exists.", title="Message")
        return status
