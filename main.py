import tkinter as tk
from login import LoginPage
from home import HomePage
    
def show_homepage(username, login_page):
    login_page.master.withdraw()
    HomePage(tk.Toplevel(), username)

root = tk.Tk()
app = LoginPage(root, lambda username: show_homepage(username, app))
root.mainloop()