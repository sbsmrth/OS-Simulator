import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from persistence.model import Auth_User
import util.encoding_decoding as enc_dec
from persistence.repository.auth_user_repository import AuthUserRepository
from gui.desktop import DesktopWindow
from gui.register import Register
import os

class Login(ctk.CTk):
    def __init__(self, *args, **kwargs):
        self.auth_repository = AuthUserRepository()
        super().__init__(*args, **kwargs)
    
        win_width = 900
        win_height = 580
        user_scren_width = self.winfo_screenwidth()
        user_screen_height = self.winfo_screenheight()
        x = int((user_scren_width - win_width) / 2)
        y = int((user_screen_height - win_height) / 2)
        self.geometry(f"{win_width}x{win_height}+{x}+{y}")
        self.title("Petya S.O")

        self.resizable(False, False)

        so_logo = ctk.CTkImage(dark_image=Image.open("./assets/skull.png"), size=(32, 32))
        self.button = ctk.CTkButton(self, image=so_logo, fg_color="transparent", text="Petya", font=("Roboto Medium",20),
                       hover=False)
        self.button.place(x=34, y=7)

        so_logo = ctk.CTkImage(dark_image=Image.open("./assets/shutdown.png"), size=(30, 30))
        self.button = ctk.CTkButton(self, image=so_logo, text="", fg_color="transparent",
                       hover=False, command=self.shutDown)
        self.button.place(x=790, y=530)

        self.main_frame = MainFrame(master=self)
        self.main_frame.pack(pady=60, padx=70, fill="both", expand=True)
    
    def open_toplevel(self):
        Register().mainloop()

    def isUser(self, user: Auth_User):
        status: bool = True
        if(user is None):
            status = False
            messagebox.showerror(
                message="The user doesn't exists.", title="Error")
        return status
    
    def isPassword(self, password: str, user: Auth_User):
        b_password = enc_dec.decrypt(user.password)
        if(password == b_password):
            self.destroy()
            DesktopWindow().mainloop()
        else:
            messagebox.showerror(
                message="The password is wrong.", title="Error")
    
    def shutDown(self):
        os.system('shutdown /s /t 1')
            
class MainFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.login_logo = ctk.CTkImage(dark_image=Image.open("./assets/user-icon.png"), size=(80, 80))
        self.user_avatar = ctk.CTkButton(self, image=self.login_logo, fg_color="transparent", text="", hover=False)
        self.user_avatar.pack(pady=40)
        self.footer_label = ctk.CTkLabel(master=self, text="Copyright © 2023-2036 Petya Corporation", font=("Roboto Medium", 12))
        self.footer_label.pack(pady=0, side="bottom")
        self.progressbar = ctk.CTkProgressBar(master=self, height=2, width=340)
        self.progressbar.configure(fg_color="red", progress_color="red")
        self.progressbar.pack(pady=10, side="bottom")

        self.second_frame = SecondFrame(master=self, login_reference=master, fg_color=self.cget("fg_color"))
        self.second_frame.pack(pady=10)

        self.third_frame = ThirdFrame(master=self, login_reference=master, fg_color=self.cget("fg_color"))
        self.third_frame.pack(pady=10)

class SecondFrame(ctk.CTkFrame):
    def __init__(self, master, login_reference, **kwargs):
        super().__init__(master, **kwargs)
        self.login_reference = login_reference
        
        self.email_entry = ctk.CTkEntry(master=self, placeholder_text="Email", width=170)
        self.email_entry.pack(padx=0, pady=10)

        self.pass_entry = ctk.CTkEntry(master=self, placeholder_text="Password", show="*", width=170)
        self.pass_entry.pack(padx=0, pady=5)

        self.send_button = ctk.CTkButton(self, fg_color="red", text="Login", hover=False, height=26,
                                        command= self.check)
        self.send_button.pack(padx=0, pady=10)
    
    def check(self):
        user_db: Auth_User = self.login_reference.auth_repository.getUserByEmail(
            self.email_entry.get())
        if(self.login_reference.isUser(user_db)):
            self.login_reference.isPassword(self.pass_entry.get(), user_db)

class ThirdFrame(ctk.CTkFrame):
    def __init__(self, master, login_reference, **kwargs):
        super().__init__(master, **kwargs)
        self.account_button = ctk.CTkButton(master=self, text="Create account", fg_color="transparent", font=("Roboto Medium", 15), hover=False, 
                                       command=login_reference.open_toplevel)
        self.account_button.grid(row=0, column=0)
        self.forgot_psw_label = ctk.CTkButton(master=self, text="Change password", fg_color="transparent", font=("Roboto Medium", 15), hover=False)
        self.forgot_psw_label.grid(row=0, column=1)
