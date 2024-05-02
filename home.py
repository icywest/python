import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os
from visualPart import PieChartWindow
from tkcalendar import DateEntry
import taskfilter

class HomePage:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        self.master.title("Welcome " + username + "!")
        self.user_tasks_dir = f"user_tasks/{username}"
        os.makedirs(self.user_tasks_dir, exist_ok=True)
        
        self.load_tasks()
        self.create_widgets()

    def load_tasks(self):
        tasks_file = os.path.join(self.user_tasks_dir, "tasks.json")
        if os.path.exists(tasks_file):
            with open(tasks_file, "r") as file:
                self.tasks = json.load(file)
        else:
            self.tasks = []

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.master, style="Main.TFrame")
        self.main_frame.pack(padx=20, pady=20)
        
        self.greeting_label = ttk.Label(self.main_frame, text="Welcome, " + self.username + "!", font=("Arial", 14), style="Greeting.TLabel")
        self.greeting_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.task_tree = ttk.Treeview(self.main_frame, columns=("Title", "Due Date", "Priority", "Status", "Comments"), style="Treeview.Treeview")
        self.task_tree.heading("Title", text="Title")
        self.task_tree.heading("Due Date", text="Due Date")
        self.task_tree.heading("Priority", text="Priority")
        self.task_tree.heading("Status", text="Status")
        self.task_tree.heading("Comments", text="Comments")
        self.task_tree.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        
        self.add_button = ttk.Button(self.main_frame, text="Add Task", command=self.add_task, style="AddButton.TButton")
        self.add_button.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        
        self.edit_button = ttk.Button(self.main_frame, text="Edit Task", command=self.edit_task, style="EditButton.TButton")
        self.edit_button.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        self.delete_button = ttk.Button(self.main_frame, text="Delete Task", command=self.delete_task, style="DeleteButton.TButton")
        self.delete_button.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        
        self.show_pie_chart_button = ttk.Button(self.main_frame, text="Show Pie Chart", command=self.show_pie_chart_window, style="ShowPieChartButton.TButton")
        self.show_pie_chart_button.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        self.create_filter_widgets()
        self.update_task_list()

    def create_filter_widgets(self):
        self.filter_frame = ttk.Frame(self.master, style="Filter.TFrame")
        self.filter_frame.pack(padx=20, pady=10)

        # Filter Keywords
        ttk.Label(self.filter_frame, text="Filter by Keywords:", style="FilterLabel.TLabel").grid(row=0, column=0, padx=5, pady=5)
        self.keywords_entry = ttk.Entry(self.filter_frame)
        self.keywords_entry.grid(row=0, column=1, padx=5, pady=5)
        

        # Filter Statuses
        ttk.Label(self.filter_frame, text="Filter by Statuses:", style="FilterLabel.TLabel").grid(row=2, column=0, padx=5, pady=5)
        self.statuses_var = {status: tk.BooleanVar() for status in ["Pending", "In Progress", "Completed"]}
        for idx, (status, var) in enumerate(self.statuses_var.items()):
            ttk.Checkbutton(self.filter_frame, text=status, variable=var, style="FilterCheck.TCheckbutton").grid(row=2, column=idx+1, padx=5, pady=5)

        # Filter Priority
        ttk.Label(self.filter_frame, text="Filter by Priority:", style="FilterLabel.TLabel").grid(row=3, column=0, padx=5, pady=5)
        self.priority_vars = {priority: tk.BooleanVar() for priority in ["Low", "Medium", "High"]}
        for idx, (priority, var) in enumerate(self.priority_vars.items()):
            ttk.Checkbutton(self.filter_frame, text=priority, variable=var, style="FilterCheck.TCheckbutton").grid(row=3, column=idx+1, padx=5, pady=5)



        # Filter Button
        self.filter_button = ttk.Button(self.filter_frame, text="Apply Filter", command=self.apply_filter)
        self.filter_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
    
    def apply_filter(self):
        keywords = self.keywords_entry.get()
        selected_statuses = [status for status, var in self.statuses_var.items() if var.get()]
        selected_priorities = [priority for priority, var in self.priority_vars.items() if var.get()]
        filtered_tasks = taskfilter.filter_tasks(self.tasks, keywords, selected_statuses, selected_priorities)

        self.update_task_list(filtered_tasks)

   
    def add_task(self):
        task_dialog = TaskDialog(self.master)
        self.master.wait_window(task_dialog.top)
        
        if task_dialog.task_data:
            self.tasks.append(task_dialog.task_data)
            self.save_tasks() 
            
            self.update_task_list()

    def edit_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Edit Task", "Please select a task to edit.")
            return
        
        task_id = int(self.task_tree.item(selected_item, "text"))
        task = self.tasks[task_id - 1]
        
        task_dialog = TaskDialog(self.master, task)
        self.master.wait_window(task_dialog.top)
        
        if task_dialog.task_data:
            self.tasks[task_id - 1] = task_dialog.task_data
            self.save_tasks()  
            self.update_task_list()

    def delete_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Delete Task", "Please select a task to delete.")
            return
        
        task_id = int(self.task_tree.item(selected_item, "text"))
        
        confirm = messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?")
        if confirm:
            del self.tasks[task_id - 1]
            self.save_tasks()
            self.update_task_list()

    def update_task_list(self, tasks=None):
        self.task_tree.delete(*self.task_tree.get_children())

        if tasks is None:
            tasks = self.tasks

        for idx, task in enumerate(tasks, start=1):
            self.task_tree.insert("", "end", text=idx, values=(task["title"], task["due_date"], task["priority"], task["status"], task.get("comments", "")))

    def show_pie_chart_window(self):
        PieChartWindow(self.master, self.tasks)

    def save_tasks(self):
        tasks_file = os.path.join(self.user_tasks_dir, "tasks.json")
        with open(tasks_file, "w") as file:
            json.dump(self.tasks, file)

class TaskDialog:
    def __init__(self, parent, task=None):
        self.parent = parent
        self.task_data = None
        
        self.top = tk.Toplevel(parent)
        self.top.title("Task Details")
        
        self.create_widgets(task)
        
    def create_widgets(self, task):
        # Title
        ttk.Label(self.top, text="Title:", style="DialogLabel.TLabel").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = ttk.Entry(self.top)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Due Date
        ttk.Label(self.top, text="Due Date:", style="DialogLabel.TLabel").grid(row=1, column=0, padx=5, pady=5)
        self.due_date_entry = DateEntry(self.top, date_pattern="yyyy-mm-dd")  # Use DateEntry widget for date input
        self.due_date_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Priority
        ttk.Label(self.top, text="Priority:", style="DialogLabel.TLabel").grid(row=2, column=0, padx=5, pady=5)
        self.priority_combobox = ttk.Combobox(self.top, values=["Low", "Medium", "High"])
        self.priority_combobox.grid(row=2, column=1, padx=5, pady=5)
        
        # Status
        ttk.Label(self.top, text="Status:", style="DialogLabel.TLabel").grid(row=3, column=0, padx=5, pady=5)
        self.status_combobox = ttk.Combobox(self.top, values=["Pending", "In Progress", "Completed"])
        self.status_combobox.grid(row=3, column=1, padx=5, pady=5)
        
        # Comments
        ttk.Label(self.top, text="Comments:", style="DialogLabel.TLabel").grid(row=4, column=0, padx=5, pady=5)
        self.comments_text = tk.Text(self.top, height=5, width=30)
        self.comments_text.grid(row=4, column=1, padx=5, pady=5)
        
        # Buttons
        self.save_button = ttk.Button(self.top, text="Save", command=self.save_task, style="SaveButton.TButton")
        self.save_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        
        self.cancel_button = ttk.Button(self.top, text="Cancel", command=self.top.destroy, style="CancelButton.TButton")
        self.cancel_button.grid(row=5, column=1, columnspan=2, padx=5, pady=5)
        
        if task:
            self.title_entry.insert(0, task["title"])
            self.due_date_entry.set_date(datetime.strptime(task["due_date"], "%Y-%m-%d"))
            self.priority_combobox.set(task["priority"])
            self.status_combobox.set(task["status"])
            if "comments" in task:
                self.comments_text.insert(tk.END, task["comments"])

    def save_task(self):
        title = self.title_entry.get()
        due_date = self.due_date_entry.get()
        priority = self.priority_combobox.get()
        status = self.status_combobox.get()
        comments = self.comments_text.get("1.0", tk.END).strip()
        
        if not (title and due_date and priority and status):
            messagebox.showwarning("Save Task", "Please fill in all fields.")
            return
        
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Save Task", "Invalid due date format. Please use YYYY-MM-DD.")
            return
        
        self.task_data = {
            "title": title,
            "due_date": due_date,
            "priority": priority,
            "status": status,
            "comments": comments
        }
    
        self.top.destroy()

def main():
    root = tk.Tk()
    app = HomePage(root, "User")
    root.mainloop()

if __name__ == "__main__":
    main()
