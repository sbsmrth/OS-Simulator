import customtkinter as ctk

class DesktopWindow(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        win_width = 1280
        win_height = 720
        user_scren_width = self.winfo_screenwidth()
        user_screen_height = self.winfo_screenheight()
        x = int((user_scren_width - win_width) / 2)
        y = int((user_screen_height - win_height) / 2)
        self.geometry(f"{win_width}x{win_height}+{x}+{y}")

        self.label = ctk.CTkLabel(self, text="Desktop", font=("Roboto Medium", 60))
        self.label.place(x=540, y=350)
