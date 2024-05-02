from datetime import datetime, timedelta

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

def filter_tasks_by_date(tasks, selected_date, period='day'):
    filtered_tasks = []
    if period == 'day':
        for task in tasks:
            if task.get("due_date") == selected_date:
                filtered_tasks.append(task)
    elif period == 'week':
        start_of_week = selected_date - timedelta(days=selected_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        for task in tasks:
            if start_of_week <= datetime.strptime(task.get("due_date"), '%Y-%m-%d') <= end_of_week:
                filtered_tasks.append(task)
    elif period == 'month':
        start_of_month = selected_date.replace(day=1)
        end_of_month = start_of_month.replace(month=start_of_month.month+1, day=1) - timedelta(days=1)
        for task in tasks:
            task_due_date = datetime.strptime(task.get("due_date"), '%Y-%m-%d')
            if start_of_month <= task_due_date <= end_of_month:
                filtered_tasks.append(task)
    return filtered_tasks

def filter_by_keywords(tasks, keywords):
    return [task for task in tasks if keywords.lower() in task["title"].lower() or keywords.lower() in task.get("content", "").lower()]

def filter_by_statuses(tasks, selected_statuses):
    return [task for task in tasks if task["status"] in selected_statuses]

def filter_by_priority(tasks, selected_priority):
    return [task for task in tasks if task["priority"] == selected_priority]
