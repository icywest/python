from datetime import datetime

def filter_tasks(tasks, keywords, statuses, priorities):
    filtered_tasks = []

    for task in tasks:
        if all([
            (not keywords or keywords.lower() in task["title"].lower()),
            (not statuses or task["status"] in statuses),
            (not priorities or task["priority"] in priorities)
        ]):
            filtered_tasks.append(task)

    return filtered_tasks

def filter_by_keywords(tasks, keywords):
    return [task for task in tasks if keywords.lower() in task["title"].lower() or keywords.lower() in task.get("content", "").lower()]

def filter_by_statuses(tasks, selected_statuses):
    return [task for task in tasks if task["status"] in selected_statuses]

def filter_by_priority(tasks, selected_priority):
    return [task for task in tasks if task["priority"] == selected_priority]
