import json
import time
import sys
import argparse
from datetime import datetime

# Simulating a persistent storage for a task manager
# This is a robust Todo CLI
TASKS_FILE = "tasks.json"

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(title, priority="medium"):
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "priority": priority.lower(),
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Added task: {title} [{priority}]")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("📭 No tasks found.")
        return

    print("\n📋 Current Tasks:")
    print("-" * 60)
    print(f"{'ID':<4} | {'Title':<30} | {'Priority':<10} | {'Status':<10}")
    print("-" * 60)
    for t in tasks:
        color = ""
        if t["priority"] == "high": color = "🔴 "
        elif t["priority"] == "medium": color = "🟡 "
        else: color = "🟢 "
        
        status_icon = "✔" if t["status"] == "done" else "⏳"
        print(f"{t['id']:<4} | {t['title']:<30} | {color}{t['priority']:<8} | {status_icon} {t['status']}")
    print("-" * 60)

def complete_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = "done"
            save_tasks(tasks)
            print(f"🎉 Task {task_id} marked as done!")
            return
    print(f"❌ Task {task_id} not found.")

def main():
    parser = argparse.ArgumentParser(description="Smart Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Task title")
    add_parser.add_argument("--priority", "-p", choices=["low", "medium", "high"], default="medium")

    # List command
    subparsers.add_parser("list", help="List all tasks")

    # Done command
    done_parser = subparsers.add_parser("done", help="Mark a task as completed")
    done_parser.add_argument("id", type=int, help="Task ID")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.title, args.priority)
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        complete_task(args.id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
