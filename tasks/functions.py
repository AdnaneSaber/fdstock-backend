from bson import ObjectId
from helpers import CustomJSONEncoder
import json


tasks = []

def initialize_tasks():
    global tasks
    tasks = []


def add_task(title, assignee, deadline, tags, description):
    global tasks
    task = {
        'title': title,
        'assignee': assignee,
        'deadline': deadline,
        'tags': tags,
        'description': description
    }
    tasks.append(task)



def update_task(task_index, title=None, assignee=None, deadline=None, tags=None, description=None):
    global tasks
    if task_index < 0 or task_index >= len(tasks):
        raise IndexError("Task index out of range.")
    task = tasks[task_index]
    if title is not None:
        task['title'] = title
    if assignee is not None:
        task['assignee'] = assignee
    if deadline is not None:
        task['deadline'] = deadline
    if tags is not None:
        task['tags'] = tags
    if description is not None:
        task['description'] = description



def fetch_tasks():
    return tasks

