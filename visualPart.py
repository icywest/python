import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class PieChartWindow:
    def __init__(self, master, tasks):
        self.master = master
        self.tasks = tasks
        
        self.top = tk.Toplevel(master)
        self.top.title("Pie Chart")
        
        self.create_pie_chart()

    def create_pie_chart(self):
        status_counts = {}
        for task in self.tasks:
            status = task["status"]
            if status in status_counts:
                status_counts[status] += 1
            else:
                status_counts[status] = 1
        
        # Create pie chart
        labels = list(status_counts.keys())
        sizes = list(status_counts.values())
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        canvas = FigureCanvasTkAgg(fig, master=self.top)
        canvas.draw()
        canvas.get_tk_widget().pack()

        ax.set_title("Task Status Distribution")
