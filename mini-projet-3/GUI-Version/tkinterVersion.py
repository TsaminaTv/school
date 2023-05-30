import customtkinter
from tkinter import messagebox

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme(color_string="dark-blue")


class GestionExamens(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Gestion des Examens")
        self.geometry("750x500")
        self.configure(background='#ff0000')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.grid(row=0, column=0)

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(master=self.frame, text="Gestion des Examens", font=("Roboto", 20))
        self.label.grid(row=0, column=0, pady=12, padx=10)

        self.username = customtkinter.CTkEntry(master=self.frame, placeholder_text="Username")
        self.username.grid(row=1, column=0, pady=12, padx=10)

        self.password = customtkinter.CTkEntry(master=self.frame, placeholder_text="Password", show="*")
        self.password.grid(row=2, column=0, pady=12, padx=10)

        self.login_button = customtkinter.CTkButton(master=self.frame, text="Login", command=self.login)
        self.login_button.grid(row=3, column=0, pady=12, padx=10)

        self.register_button = customtkinter.CTkButton(master=self.frame, text="Register", command=self.register)
        self.register_button.grid(row=4, column=0, pady=12, padx=10)

        self.quit_button = customtkinter.CTkButton(master=self.frame, text="Quit", command=self.quit)
        self.quit_button.grid(row=5, column=0, pady=(12, 50), padx=10)

    def register(self):
        # Check if the username and password are not empty
        if self.username.get() == "" or self.password.get() == "":
            messagebox.showerror("Error", "Please fill all the fields")
            return
        
        print(self.username.get(), self.password.get())

        with open("GUI-Version/Accounts/accounts.txt", mode="r", encoding='utf-8') as file:
            accounts = file.readlines()
            for account in accounts:
                # extract username and password from the line
                username, password = account.split(":")
                # remove the \n from the password
                password = password.strip()
                # check if the username already exists
                if username == self.username.get():
                    messagebox.showerror("Error", "Username already exists")
                    return

        with open("GUI-Version/Accounts/accounts.txt", mode="a", encoding='utf-8') as file:
            file.write(f"{self.username.get()}:{self.password.get()}\n")

        self.frame.grid_forget()
        # add button to go back to the login page
        self.back_button = customtkinter.CTkButton(master=self, text="Back", command=self.back)
        self.back_button.grid(row=0, column=0, pady=12, padx=10)


    def login(self):
        # Check if the username and password are not empty
        if self.username.get() == "" or self.password.get() == "":
            messagebox.showerror("Error", "Please fill all the fields")
            return

        with open("GUI-Version/Accounts/accounts.txt", mode="r", encoding='utf-8') as file:
            accounts = file.readlines()
            for account in accounts:
                # extract username and password from the line
                username, password = account.split(":")
                # remove the \n from the password
                password = password.strip()
                # check if the username and password are correct
                if username == self.username.get() and password == self.password.get():
                    self.frame.grid_forget()
                    self.back_button = customtkinter.CTkButton(master=self, text="Back", command=self.back)
                    self.back_button.grid(row=0, column=0, pady=12, padx=10)
                    messagebox.showinfo("Success", "Login successful")
                    return

            messagebox.showerror("Error", "Wrong username or password")


    def back(self):
        self.back_button.grid_forget()
        self.frame.grid(row=0, column=0)

        
def main():
    app = GestionExamens()
    app.mainloop()

if __name__ == "__main__":
    main()




# VERSION 2 NESCAP


# from typing import Optional, Tuple, Union
# import customtkinter
# from PIL import Image
# from tkinter import messagebox

# # set appearance mode and default color theme
# customtkinter.set_appearance_mode("dark")
# customtkinter.set_default_color_theme("dark-blue")

# class App(customtkinter.CTk):
#     # window size
#     width = 800
#     height = 600

#     def __init__(self, *args, **kwargs):
#         # call super constructor
#         super().__init__(*args, **kwargs)
        
#         # configure root
#         self.title("Gestion des examens")
#         self.geometry(f"{self.width}x{self.height}")
#         self.minsize(self.width, self.height)
#         self.config(background="#41B77F")

#         self.grid_columnconfigure(0, weight=1)
#         self.grid_rowconfigure(0, weight=1)

#         # create main frame
#         self.frame_main = customtkinter.CTkFrame(self, width=200, height=200)
#         self.frame_main.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
#         self.frame_main.grid_columnconfigure(0, weight=1)
#         self.frame_main.grid_columnconfigure(1, weight=1)
#         self.frame_main.grid_columnconfigure(2, weight=1)

#         # create main frame widgets
#         self.label_heading = customtkinter.CTkLabel(self.frame_main, text="CustomTkinter main Page", font=customtkinter.CTkFont(size=20, weight="bold"))
#         self.label_heading.grid(row=0, column=0, padx=30, pady=30, columnspan=3)
        
#         self.image_eleve = Image.open("GUI-Version/images/student.png")
#         self.image_eleve = customtkinter.CTkImage(self.image_eleve, size=(100, 100))
#         self.image_label = customtkinter.CTkLabel(self.frame_main, image=self.image_eleve)
#         self.image_label.grid(row=1, column=0, padx=30, pady=15)

#         self.button_eleve = customtkinter.CTkButton(self.frame_main, text="Mode étudiant", font=customtkinter.CTkFont(size=20, weight="bold"), command=self.show_frame_login)
#         self.button_eleve.grid(row=2, column=0, padx=30, pady=15)

#         self.image_prof = Image.open("GUI-Version/images/teacher.png")
#         self.image_prof = customtkinter.CTkImage(self.image_prof, size=(100, 100))
#         self.image_label = customtkinter.CTkLabel(self.frame_main, image=self.image_prof)
#         self.image_label.grid(row=1, column=1, padx=30, pady=15)

#         self.button_prof = customtkinter.CTkButton(self.frame_main, text="Mode professeur", font=customtkinter.CTkFont(size=20, weight="bold"), command=self.show_frame_prof)
#         self.button_prof.grid(row=2, column=1, padx=30, pady=15)

#         self.image_quit = Image.open("GUI-Version/images/hand.png")
#         self.image_quit = customtkinter.CTkImage(self.image_quit, size=(100, 100))
#         self.image_label = customtkinter.CTkLabel(self.frame_main, image=self.image_quit)
#         self.image_label.grid(row=1, column=2, padx=30, pady=15)

#         self.button_quit = customtkinter.CTkButton(self.frame_main, text="Quitter", font=customtkinter.CTkFont(size=20, weight="bold"), command=self.quit)
#         self.button_quit.grid(row=2, column=2, padx=30, pady=15)

#         # create eleve frame
#         self.frame_eleve = customtkinter.CTkFrame(self)
#         self.frame_eleve.grid_columnconfigure(0, weight=1)

#         self.label_heading = customtkinter.CTkLabel(self.frame_eleve, text="Eleve", font=customtkinter.CTkFont(size=20, weight="bold"))
#         self.label_heading.grid(row=0, column=0, padx=30, pady=(150, 15))

#         self.button_back = customtkinter.CTkButton(self.frame_eleve, text="Retour", font=customtkinter.CTkFont(size=20, weight="bold"), command=self.back_event)
#         self.button_back.grid(row=1, column=0, padx=30, pady=15)

#         # create prof frame
#         self.frame_prof = customtkinter.CTkTabview(self, width=250)
#         self.frame_prof.add("Créer un QCM")
#         self.frame_prof.add("Créer un élève")
#         self.frame_prof.add("Corriger un QCM")
        
#         self.label_heading = customtkinter.CTkLabel(self.frame_prof.tab("Créer un QCM"), text="Créer un QCM", font=customtkinter.CTkFont(size=20, weight="bold"))
#         self.label_heading.grid(row=2, column=0, padx=30, pady=(150, 15))

#         self.label_heading = customtkinter.CTkLabel(self.frame_prof.tab("Créer un élève"), text="Créer un élève", font=customtkinter.CTkFont(size=20, weight="bold"))
#         self.label_heading.grid(row=2, column=0, padx=30, pady=(150, 15))

#         self.label_heading = customtkinter.CTkLabel(self.frame_prof.tab("Corriger un QCM"), text="Corriger un QCM", font=customtkinter.CTkFont(size=20, weight="bold"))
#         self.label_heading.grid(row=2, column=0, padx=30, pady=(150, 15))

#         self.button_back = customtkinter.CTkButton(self.frame_prof, text="Retour", font=customtkinter.CTkFont(size=20, weight="bold"), command=self.back_event)
#         self.button_back.grid(row=3, column=0, padx=30, pady=15)
        

#         # create login frame
#         self.frame_login = customtkinter.CTkFrame(self)
#         self.frame_login.grid_columnconfigure(0, weight=1)

#         self.label_heading = customtkinter.CTkLabel(self.frame_login, text="Login", font=customtkinter.CTkFont(size=20, weight="bold"))
#         self.label_heading.grid(row=0, column=0, padx=30, pady=(150, 15))

#         self.button_login = customtkinter.CTkButton(self.frame_login, text="Login", font=customtkinter.CTkFont(size=20, weight="bold"), command=self.show_frame_eleve)
#         self.button_login.grid(row=1, column=0, padx=30, pady=15)

#         self.button_back = customtkinter.CTkButton(self.frame_login, text="Retour", font=customtkinter.CTkFont(size=20, weight="bold"), command=self.back_event)
#         self.button_back.grid(row=0, column=0, padx=30, pady=15)

#     def back_event(self):
#         # hide eleve frame
#         self.frame_eleve.grid_forget()
#         self.frame_prof.grid_forget()
#         self.frame_login.grid_forget()
#         # show main frame
#         self.frame_main.grid(row=0, column=0, sticky="ns", padx=20, pady=20)


#     def show_frame_login(self):
#         # hide main frame
#         self.frame_main.grid_forget()
#         # show login frame
#         self.frame_login.grid(row=0, column=0, sticky="ns", padx=20, pady=20)

#     def show_frame_eleve(self):
#         # hide main frame
#         self.frame_login.grid_forget()
#         # show eleve frame
#         self.frame_eleve.grid(row=0, column=0, sticky="ns", padx=20, pady=20)

#     def show_frame_prof(self):
#         # hide main frame
#         self.frame_main.grid_forget()
#         # show prof frame
#         self.frame_prof.grid(row=0, column=0, sticky="ns", padx=20, pady=20)


#     # ------------ ZBEB ------------
#     # Backend functions
    


# if __name__ == "__main__":
#     app = App()
#     app.mainloop()