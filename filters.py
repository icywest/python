def filter_tasks(tasks, filter_by, search_term):
    filtered_tasks = []
    for task in tasks:
        if filter_by == "Title":
            if search_term in task["title"].lower():
                filtered_tasks.append(task)
        elif filter_by == "Due Date":
            if search_term in task["due_date"]:
                filtered_tasks.append(task)
        elif filter_by == "Priority":
            if search_term in task["priority"]:
                filtered_tasks.append(task)
        elif filter_by == "Status":
            if search_term in task["status"]:
                filtered_tasks.append(task)
    return filtered_tasks
