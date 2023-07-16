from flask import Blueprint, jsonify, request
from .functions import add_task, delete_task, fetch_tasks, update_task

tasks_bp = Blueprint('tasks', __name__)

# Add a task
@tasks_bp.route('/tasks/add', methods=['POST'])
def add_task_view():
    data = request.get_json()
    title = data.get('title')
    assignee = data.get('assignee')
    deadline = data.get('deadline')
    tags = data.get('tags')
    description = data.get('description')
    # Add input validation as needed
    task_id = add_task(title, assignee, deadline, tags, description)
    return jsonify({'task_id': task_id}), 201

# Update a task
@tasks_bp.route('/tasks/update/<int:task_id>', methods=['PUT'])
def update_task_view(task_id):
    data = request.get_json()
    title = data.get('title')
    assignee = data.get('assignee')
    deadline = data.get('deadline')
    tags = data.get('tags')
    description = data.get('description')
    # Add input validation as needed
    success = update_task(task_id, title, assignee, deadline, tags, description)
    if success:
        return jsonify({'message': 'Task updated'})
    else:
        return jsonify({'message': 'Task not found'}), 404

# Delete a task
@tasks_bp.route('/tasks/delete/<int:task_id>', methods=['DELETE'])
def delete_task_view(task_id):
    # Add input validation as needed
    success = delete_task(task_id)
    if success:
        return jsonify({'message': 'Task deleted'})
    else:
        return jsonify({'message': 'Task not found'}), 404

# Fetch all tasks
@tasks_bp.route('/tasks', methods=['GET'])
def fetch_tasks_view():
    tasks = fetch_tasks()
    return jsonify(tasks)

# Fetch a specific task by task_id
@tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
def fetch_task_view(task_id):
    tasks = fetch_tasks()
    task = next((t for t in tasks if t['task_id'] == task_id), None)
    if task:
        return jsonify(task)
    else:
        return jsonify({'message': 'Task not found'}), 404
