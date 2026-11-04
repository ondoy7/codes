
# ==========================================
# TASKFLOW: A SMART TASK MANAGEMENT SYSTEM
# ==========================================

tasks = []

PRIORITIES = ["High", "Medium", "Low"]


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def get_integer(prompt, minimum=None):
    while True:
        try:
            number = int(input(prompt))

            if minimum is not None and number < minimum:
                print(f"[ERROR] Enter a number >= {minimum}.")
                continue

            return number

        except ValueError:
            print("[ERROR] Please enter a valid whole number.")


def get_priority(prompt="Enter priority (High/Medium/Low): "):
    while True:
        priority = input(prompt).strip().capitalize()

        if priority in PRIORITIES:
            return priority

        print("[ERROR] Choose High, Medium, or Low.")


def get_task_number(action):
    if not tasks:
        print("\nNo tasks available.")
        return None

    view_tasks()

    number = get_integer(
        f"\nEnter task number to {action}: ",
        minimum=1
    )

    if number > len(tasks):
        print("[ERROR] Invalid task number.")
        return None

    return number - 1


def print_task_table(task_list, heading="ALL TASKS"):
    print("\n" + "=" * 94)
    print(heading.center(94))
    print("=" * 94)

    if not task_list:
        print("No tasks available.".center(94))
        print("=" * 94)
        return

    headers = [
        "NO.", "TASK TITLE", "SUBJECT",
        "PRIORITY", "DAYS LEFT", "STATUS"
    ]

    widths = [5, 24, 20, 12, 12, 12]

    header_row = " ".join(
        f"{header:<{width}}"
        for header, width in zip(headers, widths)
    )

    print(header_row)
    print("-" * 94)

    for number, task in enumerate(task_list, start=1):
        title, subject, priority, days_left, status = task

        # Shorten long text so the table stays aligned.
        values = [
            str(number),
            title,
            subject,
            priority,
            str(days_left),
            status
        ]

        row = " ".join(
            f"{value[:width - 1]:<{width}}"
            for value, width in zip(values, widths)
        )

        print(row)

    print("=" * 94)
    print("Total tasks:", len(task_list))


# ==========================================
# FEATURE 1 - ADD NEW TASK
# ==========================================

def add_task():
    print("\n========== ADD NEW TASK ==========")

    task_title = input("Enter task title: ").strip()
    while not task_title:
        print("[ERROR] Task title cannot be empty.")
        task_title = input("Enter task title: ").strip()

    subject = input("Enter subject: ").strip()
    while not subject:
        print("[ERROR] Subject cannot be empty.")
        subject = input("Enter subject: ").strip()

    priority = get_priority()

    days_left = get_integer(
        "Enter days until deadline "
        "(use 0 for today, negative for overdue): "
    )

    task = [
        task_title,
        subject,
        priority,
        days_left,
        "Pending"
    ]

    tasks.append(task)

    print("\n[SUCCESS] Task added successfully!")
    print_task_table([task], "NEWLY ADDED TASK")


# ==========================================
# FEATURE 2 - VIEW ALL TASKS
# ==========================================

def view_tasks():
    print_task_table(tasks, "ALL TASKS")


# ==========================================
# FEATURE 3 - UPDATE TASK
# ==========================================

def update_task():
    task_index = get_task_number("update")

    if task_index is None:
        return

    task = tasks[task_index]

    print("\nEnter new task information.")
    print("Press Enter to keep the current value.")

    new_title = input(
        f"Task title [{task[0]}]: "
    ).strip()

    new_subject = input(
        f"Subject [{task[1]}]: "
    ).strip()

    if new_title:
        task[0] = new_title

    if new_subject:
        task[1] = new_subject

    while True:
        new_priority = input(
            f"Priority [{task[2]}] (High/Medium/Low): "
        ).strip()

        if not new_priority:
            break

        normalized = new_priority.capitalize()

        if normalized in PRIORITIES:
            task[2] = normalized
            break

        print("[ERROR] Choose High, Medium, or Low.")

    while True:
        new_days = input(
            f"Days left [{task[3]}]: "
        ).strip()

        if not new_days:
            break

        try:
            task[3] = int(new_days)
            break
        except ValueError:
            print("[ERROR] Enter a valid whole number.")

    print("\n[SUCCESS] Task updated successfully!")
    view_tasks()


# ==========================================
# FEATURE 4 - COMPLETE TASK
# ==========================================

def complete_task():
    task_index = get_task_number("complete")

    if task_index is None:
        return

    task = tasks[task_index]

    if task[4] == "Completed":
        print("\n[INFO] This task is already completed.")
    else:
        task[4] = "Completed"
        print("\n[SUCCESS] Task marked as completed!")

    view_tasks()


# ==========================================
# FEATURE 5 - DELETE TASK
# ==========================================

def delete_task():
    task_index = get_task_number("delete")

    if task_index is None:
        return

    deleted_task = tasks[task_index]

    confirm = input(
        f"Delete '{deleted_task[0]}'? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        tasks.pop(task_index)
        print(
            f"\n[SUCCESS] Task '{deleted_task[0]}' "
            "deleted successfully!"
        )
    else:
        print("\n[INFO] Deletion cancelled.")

    view_tasks()


# ==========================================
# FEATURE 6 - VIEW PENDING TASKS
# ==========================================

def view_pending_tasks():
    pending = [
        task for task in tasks
        if task[4] == "Pending"
    ]

    print_task_table(pending, "PENDING TASKS")


# ==========================================
# FEATURE 7 - VIEW TASKS BY PRIORITY
# ==========================================

def view_by_priority():
    priority = get_priority(
        "\nEnter priority to view (High/Medium/Low): "
    )

    matching_tasks = [
        task for task in tasks
        if task[2] == priority
    ]

    print_task_table(
        matching_tasks,
        f"{priority.upper()} PRIORITY TASKS"
    )


# ==========================================
# FEATURE 8 - DEADLINE MONITOR
# ==========================================

def check_deadlines():
    print("\n" + "=" * 94)
    print("DEADLINE MONITOR".center(94))
    print("=" * 94)

    pending = [
        task for task in tasks
        if task[4] == "Pending"
    ]

    if not pending:
        print("No pending tasks to monitor.")
        print("=" * 94)
        return

    # Sort by the closest deadline first.
    pending.sort(key=lambda task: task[3])

    print_task_table(pending, "PENDING TASK DEADLINES")

    print("\nDEADLINE REMINDERS")
    print("-" * 40)

    for task in pending:
        title, subject, priority, days_left, status = task

        if days_left < 0:
            print(
                f"[OVERDUE] {title} - "
                f"{abs(days_left)} day(s) overdue!"
            )
        elif days_left == 0:
            print(f"[DUE TODAY] {title}")
        elif days_left == 1:
            print(f"[REMINDER] {title} is due tomorrow.")
        else:
            print(f"[UPCOMING] {title} - {days_left} days left.")

    print("=" * 94)


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():
    while True:
        print("\n" + "=" * 40)
        print("       TASKFLOW TASK MANAGEMENT")
        print("=" * 40)
        print("[1] Add New Task")
        print("[2] View All Tasks")
        print("[3] Update Task")
        print("[4] Complete Task")
        print("[5] Delete Task")
        print("[6] View Pending Tasks")
        print("[7] View Tasks by Priority")
        print("[8] Check Deadlines")
        print("[9] Exit System")
        print("=" * 40)

        choice = input("Select an option (1-9): ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            update_task()
        elif choice == "4":
            complete_task()
        elif choice == "5":
            delete_task()
        elif choice == "6":
            view_pending_tasks()
        elif choice == "7":
            view_by_priority()
        elif choice == "8":
            check_deadlines()
        elif choice == "9":
            print("\nExiting TaskFlow. Goodbye!")
            break
        else:
            print("\n[ERROR] Invalid option. Please select 1-9.")


# ==========================================
# START PROGRAM
# ==========================================

if __name__ == "__main__":
    main()
