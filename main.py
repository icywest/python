import tkinter as tk
from tkinter import ttk
from login import LoginPage
from home import HomePage 

def show_homepage(username, login_page):
    login_page.master.withdraw()
    HomePage(tk.Toplevel(), username)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

root = tk.Tk()
root.title("Login")
width = 250
height = 200
center_window(root, width, height)
app = LoginPage(root, lambda username: show_homepage(username, app))
root.mainloop()