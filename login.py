import tkinter as tk
from tkinter import ttk, messagebox
import json
from PIL import Image, ImageTk

class LoginPage:
    def __init__(self, master, on_login_success):
        self.master = master
        self.master.title("Login Page")
        self.on_login_success = on_login_success
        self.image_path = "D:\\Usuarios\\Cynthia Nicolas\\OneDrive - ITEDU\\Documents\\Keiser University\\Junior First\\Python\\taskManager\\img\\person.png"

        self.load_image()
        self.create_widgets()

    def create_widgets(self):
        # Frame for login form
        self.login_frame = ttk.Frame(self.master, padding="20")
        self.login_frame.pack()

        # Load the image
        self.image_label = ttk.Label(self.login_frame, image=self.img_tk)
        self.image_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Username label and entry
        self.username_label = ttk.Label(self.login_frame, text="Username:")
        self.username_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)

        # Password label and entry
        self.password_label = ttk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        # Login button
        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=3, column=0, padx=5, pady=5)

        # Register button
        self.register_button = ttk.Button(self.login_frame, text="Register", command=self.show_register_window)
        self.register_button.grid(row=3, column=1, padx=5, pady=5)

    def load_image(self):
        # Open the image file
        self.img = Image.open(self.image_path)
        # Resize the image to a smaller size
        width, height = 50, 50
        self.img = self.img.resize((width, height))
        self.img_tk = ImageTk.PhotoImage(self.img)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.authenticate_user(username, password):
            self.on_login_success(username)
        else:
            messagebox.showerror("Login", "Incorrect username or password")

    def show_register_window(self):
        register_window = tk.Toplevel(self.master)
        RegisterPage(register_window, self.register)

    def register(self, username, password):
        try:
            with open("user_data.json", "r") as file:
                user_data = json.load(file)
        except FileNotFoundError:
            user_data = {"users": []}

        for user in user_data["users"]:
            if user["username"] == username:
                messagebox.showerror("Registration", "Username already exists.")
                return

        user_data["users"].append({"username": username, "password": password})

        with open("user_data.json", "w") as file:
            json.dump(user_data, file)

        messagebox.showinfo("Registration", "Registration successful. You can now login.")

    def authenticate_user(self, username, password):
        try:
            with open("user_data.json", "r") as file:
                user_data = json.load(file)
                for user in user_data["users"]:
                    if user["username"] == username and user["password"] == password:
                        return True
        except FileNotFoundError:
            messagebox.showerror("Login", "User data file not found.")
        except json.JSONDecodeError:
            messagebox.showerror("Login", "Invalid user data format.")
        return False

class RegisterPage:
    def __init__(self, master, register_callback):
        self.master = master
        self.master.title("Register")
        self.register_callback = register_callback
        self.create_widgets()

    def create_widgets(self):
        # Frame for register form
        self.register_frame = ttk.Frame(self.master, padding="20")
        self.register_frame.pack()

        # Username label and entry
        self.username_label = ttk.Label(self.register_frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = ttk.Entry(self.register_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        # Password label and entry
        self.password_label = ttk.Label(self.register_frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = ttk.Entry(self.register_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Register button
        self.register_button = ttk.Button(self.register_frame, text="Register", command=self.register)
        self.register_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not (username and password):
            messagebox.showerror("Registration", "Please enter both username and password.")
            return

        self.register_callback(username, password)
        self.master.destroy()

def on_login_success(username):
    print(f"Login successful for user: {username}")

def main():
    root = tk.Tk()
    app = LoginPage(root, on_login_success)
    root.mainloop()

if __name__ == "__main__":
    main()