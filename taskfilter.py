# task_filter.py

from datetime import datetime

def filter_tasks(tasks, keywords="", start_date="", end_date="", selected_statuses=[], selected_priority=""):
    filtered_tasks = tasks

    if keywords:
        filtered_tasks = filter_by_keywords(filtered_tasks, keywords)
    if start_date and end_date:
        filtered_tasks = filter_by_date_range(filtered_tasks, start_date, end_date)
    if selected_statuses:
        filtered_tasks = filter_by_statuses(filtered_tasks, selected_statuses)
    if selected_priority:
        filtered_tasks = filter_by_priority(filtered_tasks, selected_priority)

    return filtered_tasks

def filter_by_keywords(tasks, keywords):
    return [task for task in tasks if keywords.lower() in task["title"].lower() or keywords.lower() in task.get("content", "").lower()]

def filter_by_date_range(tasks, start_date, end_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    return [task for task in tasks if start_date <= datetime.strptime(task["due_date"], "%Y-%m-%d") <= end_date]

def filter_by_statuses(tasks, selected_statuses):
    return [task for task in tasks if task["status"] in selected_statuses]

def filter_by_priority(tasks, selected_priority):
    return [task for task in tasks if task["priority"] == selected_priority]
