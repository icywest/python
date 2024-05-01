import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PieChartWindow:
    def __init__(self, parent, tasks):
        self.parent = parent
        self.tasks = tasks
        
        self.top = tk.Toplevel(parent)
        self.top.title("Task Status Pie Chart")
        
        self.create_pie_chart()
    
    def create_pie_chart(self):
        if not self.tasks:
            messagebox.showinfo("No Tasks", "There are no tasks available to analyze. Please schedule tasks.")
            self.top.destroy()
            return
        
        status_counts = {"Pending": 0, "In Progress": 0, "Completed": 0}
        for task in self.tasks:
            status_counts[task["status"]] += 1
        
        fig = Figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        
        ax.pie(status_counts.values(), labels=status_counts.keys(), autopct='%1.1f%%', startangle=140)
        ax.set_title("Task Status Distribution")
        
        canvas = FigureCanvasTkAgg(fig, master=self.top)
        canvas.draw()
        canvas.get_tk_widget().pack()