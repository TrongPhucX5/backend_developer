import sys
import json
import os
from datetime import datetime

# Tên tệp lưu trữ dữ liệu
DATA_FILE = "tasks.json"

def load_tasks():
    """Đọc danh sách tác vụ từ tệp JSON."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    """Lưu danh sách tác vụ vào tệp JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)

def generate_id(tasks):
    """Tạo ID tự động tăng."""
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1

def add_task(description):
    tasks = load_tasks()
    new_task = {
        "id": generate_id(tasks),
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_task['id']})")

def update_task(task_id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = new_description
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully.")
            return
    print(f"Error: Task with ID {task_id} not found.")

def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t['id'] != task_id]
    if len(new_tasks) == len(tasks):
        print(f"Error: Task with ID {task_id} not found.")
    else:
        save_tasks(new_tasks)
        print(f"Task {task_id} deleted successfully.")

def mark_status(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as {status}.")
            return
    print(f"Error: Task with ID {task_id} not found.")

def list_tasks(filter_status=None):
    tasks = load_tasks()
    filtered = [t for t in tasks if filter_status is None or t['status'] == filter_status]
    
    if not filtered:
        print("No tasks found.")
        return

    for t in filtered:
        print(f"[{t['id']}] {t['description']} - Status: {t['status']} (Updated: {t['updatedAt']})")

def main():
    # sys.argv[0] là tên tệp, các phần tử tiếp theo là tham số người dùng nhập
    if len(sys.argv) < 2:
        print("Usage: python task-cli.py [command] [arguments]")
        return

    command = sys.argv[1]

    if command == "add" and len(sys.argv) > 2:
        add_task(sys.argv[2])
    elif command == "update" and len(sys.argv) > 3:
        update_task(int(sys.argv[2]), sys.argv[3])
    elif command == "delete" and len(sys.argv) > 2:
        delete_task(int(sys.argv[2]))
    elif command == "mark-in-progress" and len(sys.argv) > 2:
        mark_status(int(sys.argv[2]), "in-progress")
    elif command == "mark-done" and len(sys.argv) > 2:
        mark_status(int(sys.argv[2]), "done")
    elif command == "list":
        status = sys.argv[2] if len(sys.argv) > 2 else None
        list_tasks(status)
    else:
        print("Invalid command or missing arguments.")

if __name__ == "__main__":
    main()