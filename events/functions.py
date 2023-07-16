from bson import ObjectId
import json

def read_all_tasks():
    # Function to fetch all tasks from the "tasks" collection
    tasks = tasks_collection.find()
    task_list = []
    for task in tasks:
        task['_id'] = str(task['_id'])
        task_list.append(task)
    return json.dumps(list(task_list))


def create_task(task_data):
    # Function to add a new task to the "tasks" collection
    result = tasks_collection.insert_one(task_data)
    return str(result.inserted_id)


def read_task(task_id):
    # Function to fetch a single task by its ID from the "tasks" collection
    task = tasks_collection.find_one({'_id': ObjectId(task_id)})
    if task:
        task['_id'] = str(task['_id'])
    return task


def update_task(task_id, updated_data):
    # Function to update an existing task in the "tasks" collection
    tasks_collection.update_one(
        {'_id': ObjectId(task_id)}, {'$set': updated_data})
    return True


def delete_task(task_id):
    # Function to delete a task by its ID from the "tasks" collection
    tasks_collection.delete_one({'_id': ObjectId(task_id)})
    return True
