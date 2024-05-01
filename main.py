import tkinter as tk
from registerPage import LoginPage
from homePage import HomePage

def main():
    def show_homepage(username, login_page):
        login_page.master.withdraw()
        HomePage(tk.Toplevel(), username)

    root = tk.Tk()
    app = LoginPage(root, lambda username: show_homepage(username, app))
    root.mainloop()

if __name__ == "__main__":
    main()
