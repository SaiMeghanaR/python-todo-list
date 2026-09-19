import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# =========================================================
# PROFESSIONAL NUDE / BEIGE THEME
# =========================================================

BG = "#F6F0E8"
CARD = "#FFFDF9"
PRIMARY = "#9A7B62"
PRIMARY_DARK = "#6F5846"
ACCENT = "#E8DDD1"
TEXT = "#4E433A"
MUTED = "#7C7066"
SUCCESS = "#6F8F72"
WARNING = "#B68A55"
DANGER = "#B76E5C"
BORDER = "#D8C7B8"

tasks = []

FILE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "tasks.json"
)

# =========================================================
# BASIC FILE FUNCTIONS
# =========================================================

def read_saved_tasks():
    if not os.path.exists(FILE_PATH):
        return []

    try:
        with open(FILE_PATH, "r") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except:
        return []


def write_saved_tasks(saved_tasks):
    try:
        with open(FILE_PATH, "w") as file:
            json.dump(saved_tasks, file, indent=4)

        return True

    except Exception as e:
        print("Error:", e)
        return False


# =========================================================
# LOAD TASKS
# =========================================================

def load_tasks():
    global tasks
    tasks = read_saved_tasks()


# =========================================================
# DATE FUNCTIONS
# =========================================================

def get_task_date(task):
    try:
        return datetime.strptime(
            task["due_date"],
            "%d-%m-%Y"
        ).date()

    except:
        return None


def get_overdue_count():
    today = datetime.today().date()
    count = 0

    for task in tasks:
        due = get_task_date(task)

        if due is not None:
            if due < today and task["status"] != "Completed":
                count += 1

    return count


def get_today_tasks():
    today = datetime.today().date()
    today_tasks = []

    for i, task in enumerate(tasks):
        due = get_task_date(task)

        if due == today and task["status"] != "Completed":
            today_tasks.append((i, task))

    return today_tasks


# =========================================================
# CHECK IF TASK IS SAVED
# =========================================================

def task_is_saved(task):
    saved_tasks = read_saved_tasks()

    for saved_task in saved_tasks:
        if saved_task.get("name", "").lower() == task["name"].lower():
            return True

    return False


# =========================================================
# UPDATE SAVED VERSION OF A TASK
# =========================================================

def update_saved_task(task):
    saved_tasks = read_saved_tasks()

    for i, saved_task in enumerate(saved_tasks):
        if saved_task.get("name", "").lower() == task["name"].lower():
            saved_tasks[i] = task
            write_saved_tasks(saved_tasks)
            return True

    return False


# =========================================================
# REMOVE TASK FROM SAVED FILE
# =========================================================

def remove_from_saved(task):
    saved_tasks = read_saved_tasks()
    new_saved_tasks = []

    for saved_task in saved_tasks:
        if saved_task.get("name", "").lower() != task["name"].lower():
            new_saved_tasks.append(saved_task)

    write_saved_tasks(new_saved_tasks)


# =========================================================
# DUE DATE REMINDER
# =========================================================

def check_reminders():
    today_tasks = get_today_tasks()
    overdue = get_overdue_count()
    message = ""

    if today_tasks:
        message += "Tasks due today:\n\n"

        for index, task in today_tasks:
            message += (
                str(index + 1)
                + ". "
                + task["name"]
                + " ("
                + task["priority"]
                + ")\n"
            )

    if overdue > 0:
        if message != "":
            message += "\n"

        message += (
            "You have "
            + str(overdue)
            + " overdue task(s)."
        )

    if message != "":
        messagebox.showwarning(
            "Task Reminder",
            message
        )


# =========================================================
# DASHBOARD MESSAGE
# =========================================================

def show_message(text):
    message_label.config(
        text=text,
        fg=SUCCESS
    )

    root.after(
        3000,
        lambda: message_label.config(text="")
    )


# =========================================================
# UPDATE DASHBOARD
# =========================================================

def update_dashboard():
    total = len(tasks)
    completed = 0

    for task in tasks:
        if task["status"] == "Completed":
            completed += 1

    pending = total - completed
    overdue = get_overdue_count()

    total_label.config(
        text="TOTAL TASKS\n" + str(total)
    )

    pending_label.config(
        text="PENDING\n" + str(pending)
    )

    completed_label.config(
        text="COMPLETED\n" + str(completed)
    )

    overdue_label.config(
        text="OVERDUE\n" + str(overdue)
    )

    if total > 0:
        progress = (completed / total) * 100
    else:
        progress = 0

    progress_bar["value"] = progress

    progress_text.config(
        text="Completion Progress: "
        + str(int(progress))
        + "%"
    )


# =========================================================
# POPUP DESIGN HELPERS
# =========================================================

def popup_header(window, title, subtitle=None):
    header = tk.Frame(
        window,
        bg=PRIMARY,
        height=90
    )

    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text=title,
        bg=PRIMARY,
        fg="white",
        font=("Arial", 20, "bold")
    ).pack(pady=(18, 2))

    if subtitle:
        tk.Label(
            header,
            text=subtitle,
            bg=PRIMARY,
            fg="#F3EDE6",
            font=("Arial", 10)
        ).pack()


def style_entry(entry):
    entry.config(
        bg="#F9F6F1",
        fg=TEXT,
        relief="solid",
        bd=1,
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=PRIMARY
    )


def make_action_button(
    parent,
    text,
    command,
    color=PRIMARY,
    width=20
):
    return tk.Button(
        parent,
        text=text,
        command=command,
        width=width,
        height=2,
        bg=color,
        fg="white",
        activebackground=(
            PRIMARY_DARK
            if color == PRIMARY
            else color
        ),
        activeforeground="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        bd=0,
        cursor="hand2"
    )


# =========================================================
# ADD TASK
# =========================================================

def add_task():
    window = tk.Toplevel(root)
    window.title("Add Task")
    window.geometry("450x470")
    window.resizable(False, False)
    window.configure(bg=BG)

    popup_header(
        window,
        "ADD NEW TASK",
        "Create a new task"
    )

    body = tk.Frame(
        window,
        bg=BG
    )

    body.pack(
        fill="both",
        expand=True,
        padx=35,
        pady=20
    )

    tk.Label(
        body,
        text="Task Name",
        bg=BG,
        fg=TEXT,
        font=("Arial", 10, "bold")
    ).pack(anchor="w")

    task_entry = tk.Entry(
        body,
        width=40,
        font=("Arial", 11)
    )

    style_entry(task_entry)

    task_entry.pack(
        pady=(5, 14),
        ipady=6
    )

    tk.Label(
        body,
        text="Priority",
        bg=BG,
        fg=TEXT,
        font=("Arial", 10, "bold")
    ).pack(anchor="w")

    priority_box = ttk.Combobox(
        body,
        values=["High", "Medium", "Low"],
        state="readonly",
        width=37
    )

    priority_box.pack(
        pady=(5, 14),
        ipady=4
    )

    priority_box.set("Medium")

    tk.Label(
        body,
        text="Due Date (DD-MM-YYYY)",
        bg=BG,
        fg=TEXT,
        font=("Arial", 10, "bold")
    ).pack(anchor="w")

    date_entry = tk.Entry(
        body,
        width=40,
        font=("Arial", 11)
    )

    style_entry(date_entry)

    date_entry.pack(
        pady=(5, 18),
        ipady=6
    )

    def add():
        name = task_entry.get().strip()
        priority = priority_box.get()
        due_date = date_entry.get().strip()

        if name == "":
            messagebox.showwarning(
                "Warning",
                "Please enter a task."
            )
            return

        if due_date == "":
            messagebox.showwarning(
                "Warning",
                "Please enter due date."
            )
            return

        try:
            datetime.strptime(
                due_date,
                "%d-%m-%Y"
            )
        except:
            messagebox.showwarning(
                "Warning",
                "Use DD-MM-YYYY format."
            )
            return

        for task in tasks:
            if task["name"].lower() == name.lower():
                messagebox.showwarning(
                    "Warning",
                    "This task already exists."
                )
                return

        new_task = {
            "name": name,
            "priority": priority,
            "due_date": due_date,
            "status": "Pending"
        }

        tasks.append(new_task)

        update_dashboard()

        window.destroy()

        show_message(
            "Task added! Use Save Tasks to save it."
        )

    make_action_button(
        body,
        "✓  ADD TASK",
        add
    ).pack(pady=5)


# =========================================================
# VIEW TASKS
# =========================================================

def view_tasks():
    window = tk.Toplevel(root)
    window.title("View Tasks")
    window.geometry("950x600")
    window.configure(bg=BG)

    popup_header(
        window,
        "MY TASKS",
        "View, filter and sort your tasks"
    )

    filter_frame = tk.Frame(
        window,
        bg=BG
    )

    filter_frame.pack(pady=12)

    tk.Label(
        filter_frame,
        text="Filter:",
        bg=BG,
        fg=TEXT,
        font=("Arial", 10, "bold")
    ).pack(
        side="left",
        padx=5
    )

    filter_box = ttk.Combobox(
        filter_frame,
        values=[
            "All",
            "Pending",
            "Completed",
            "High",
            "Medium",
            "Low"
        ],
        state="readonly",
        width=15
    )

    filter_box.pack(
        side="left",
        padx=5
    )

    filter_box.set("All")

    tk.Label(
        filter_frame,
        text="Sort:",
        bg=BG,
        fg=TEXT,
        font=("Arial", 10, "bold")
    ).pack(
        side="left",
        padx=(20, 5)
    )

    sort_box = ttk.Combobox(
        filter_frame,
        values=[
            "Priority",
            "Original Order"
        ],
        state="readonly",
        width=18
    )

    sort_box.pack(side="left")
    sort_box.set("Priority")

    table_frame = tk.Frame(
        window,
        bg=CARD,
        bd=1,
        relief="solid"
    )

    table_frame.pack(
        padx=25,
        pady=5,
        fill="both",
        expand=True
    )

    columns = (
        "No",
        "Task",
        "Priority",
        "Due Date",
        "Status"
    )

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=18
    )

    for column in columns:
        table.heading(
            column,
            text=column
        )

    table.column("No", width=60)
    table.column("Task", width=330)
    table.column("Priority", width=130)
    table.column("Due Date", width=160)
    table.column("Status", width=130)

    table.pack(
        padx=10,
        pady=10,
        fill="both",
        expand=True
    )

    # =====================================================
    # DISPLAY TASKS
    # =====================================================

    def display_tasks():

        for item in table.get_children():
            table.delete(item)

        selected_filter = filter_box.get()
        selected_sort = sort_box.get()

        filtered_tasks = []

        for index, task in enumerate(tasks):

            if selected_filter == "All":
                filtered_tasks.append(
                    (index, task)
                )

            elif selected_filter == "Pending":
                if task["status"] == "Pending":
                    filtered_tasks.append(
                        (index, task)
                    )

            elif selected_filter == "Completed":
                if task["status"] == "Completed":
                    filtered_tasks.append(
                        (index, task)
                    )

            elif selected_filter in [
                "High",
                "Medium",
                "Low"
            ]:

                if task["priority"] == selected_filter:
                    filtered_tasks.append(
                        (index, task)
                    )

        # Priority sorting
        if selected_sort == "Priority":

            priority_order = {
                "High": 1,
                "Medium": 2,
                "Low": 3
            }

            filtered_tasks.sort(
                key=lambda x:
                priority_order.get(
                    x[1]["priority"],
                    4
                )
            )

        # Display tasks
        for index, task in filtered_tasks:

            # Tick ONLY when completed
            if task["status"] == "Completed":
                status_text = "✓ Completed"
            else:
                status_text = "Pending"

            table.insert(
                "",
                "end",
                values=(
                    index + 1,
                    task["name"],
                    task["priority"],
                    task["due_date"],
                    status_text
                )
            )

        if len(filtered_tasks) == 0:

            table.insert(
                "",
                "end",
                values=(
                    "",
                    "No tasks found",
                    "",
                    "",
                    ""
                )
            )

    filter_box.bind(
        "<<ComboboxSelected>>",
        lambda event: display_tasks()
    )

    sort_box.bind(
        "<<ComboboxSelected>>",
        lambda event: display_tasks()
    )

    display_tasks()


# =========================================================
# DELETE TASK
# =========================================================

def delete_task():

    if len(tasks) == 0:
        messagebox.showinfo(
            "Delete Task",
            "No tasks available."
        )
        return

    window = tk.Toplevel(root)
    window.title("Delete Task")
    window.geometry("400x320")
    window.resizable(False, False)
    window.configure(bg=BG)

    popup_header(
        window,
        "DELETE TASK",
        "Remove a task from your list"
    )

    body = tk.Frame(
        window,
        bg=BG
    )

    body.pack(
        fill="both",
        expand=True,
        padx=35,
        pady=25
    )

    tk.Label(
        body,
        text="Enter task number:",
        bg=BG,
        fg=TEXT,
        font=("Arial", 10, "bold")
    ).pack()

    number_entry = tk.Entry(
        body,
        width=20,
        font=("Arial", 11)
    )

    style_entry(number_entry)

    number_entry.pack(
        pady=12,
        ipady=6
    )

    def delete():

        try:
            number = int(
                number_entry.get()
            )

            if number < 1 or number > len(tasks):
                messagebox.showwarning(
                    "Warning",
                    "Invalid task number."
                )
                return

            deleted_task = tasks[number - 1]

            del tasks[number - 1]

            remove_from_saved(
                deleted_task
            )

            update_dashboard()

            window.destroy()

            show_message(
                "Task deleted successfully!"
            )

        except ValueError:
            messagebox.showwarning(
                "Warning",
                "Enter a valid number."
            )

    make_action_button(
        body,
        "🗑  DELETE",
        delete,
        DANGER
    ).pack(pady=10)


# =========================================================
# UPDATE TASK
# =========================================================

def update_task():

    if len(tasks) == 0:
        messagebox.showinfo(
            "Update Task",
            "No tasks available."
        )
        return

    window = tk.Toplevel(root)
    window.title("Update Task")
    window.geometry("450x500")
    window.resizable(False, False)
    window.configure(bg=BG)

    popup_header(
        window,
        "UPDATE TASK",
        "Edit your selected task"
    )

    body = tk.Frame(
        window,
        bg=BG
    )

    body.pack(
        fill="both",
        expand=True,
        padx=35,
        pady=15
    )

    tk.Label(
        body,
        text="Enter task number",
        bg=BG,
        fg=TEXT,
        font=("Arial", 10, "bold")
    ).pack(anchor="w")

    number_entry = tk.Entry(
        body,
        width=20,
        font=("Arial", 11)
    )

    style_entry(number_entry)

    number_entry.pack(
        pady=(5, 10),
        ipady=5
    )

    tk.Label(
        body,
        text="New Task Name",
        bg=BG,
        fg=TEXT,
        font=("Arial", 10, "bold")
    ).pack(anchor="w")

    name_entry = tk.Entry(
        body,
        width=35,
        font=("Arial", 11)
    )

    style_entry(name_entry)

    name_entry.pack(
        pady=(5, 10),
        ipady=5
    )

    tk.Label(
        body,
        text="New Priority",
        bg=BG,
        fg=TEXT,
        font=("Arial", 10, "bold")
    ).pack(anchor="w")

    priority_box = ttk.Combobox(
        body,
        values=["High", "Medium", "Low"],
        state="readonly",
        width=32
    )

    priority_box.pack(
        pady=(5, 10),
        ipady=3
    )

    priority_box.set("Medium")

    tk.Label(
        body,
        text="New Due Date",
        bg=BG,
        fg=TEXT,
        font=("Arial", 10, "bold")
    ).pack(anchor="w")

    date_entry = tk.Entry(
        body,
        width=35,
        font=("Arial", 11)
    )

    style_entry(date_entry)

    date_entry.pack(
        pady=(5, 15),
        ipady=5
    )

    def update():

        try:
            number = int(
                number_entry.get()
            )

            if number < 1 or number > len(tasks):
                messagebox.showwarning(
                    "Warning",
                    "Invalid task number."
                )
                return

            old_task_name = tasks[
                number - 1
            ]["name"]

            name = name_entry.get().strip()
            priority = priority_box.get()
            due_date = date_entry.get().strip()

            if name == "":
                messagebox.showwarning(
                    "Warning",
                    "Enter task name."
                )
                return

            if due_date == "":
                messagebox.showwarning(
                    "Warning",
                    "Enter due date."
                )
                return

            try:
                datetime.strptime(
                    due_date,
                    "%d-%m-%Y"
                )

            except:
                messagebox.showwarning(
                    "Warning",
                    "Use DD-MM-YYYY format."
                )
                return

            tasks[number - 1]["name"] = name
            tasks[number - 1]["priority"] = priority
            tasks[number - 1]["due_date"] = due_date

            saved_tasks = read_saved_tasks()

            for i, saved_task in enumerate(saved_tasks):

                if saved_task.get(
                    "name",
                    ""
                ).lower() == old_task_name.lower():

                    saved_tasks[i] = tasks[
                        number - 1
                    ]

                    write_saved_tasks(
                        saved_tasks
                    )

                    break

            update_dashboard()

            window.destroy()

            show_message(
                "Task updated successfully!"
            )

        except ValueError:
            messagebox.showwarning(
                "Warning",
                "Enter a valid task number."
            )

    make_action_button(
        body,
        "✎  UPDATE",
        update
    ).pack(pady=5)


# =========================================================
# MARK COMPLETED
# =========================================================

def mark_completed():

    if len(tasks) == 0:
        messagebox.showinfo(
            "Completed",
            "No tasks available."
        )
        return

    window = tk.Toplevel(root)
    window.title("Mark Completed")
    window.geometry("400x320")
    window.resizable(False, False)
    window.configure(bg=BG)

    popup_header(
        window,
        "MARK COMPLETED",
        "Complete a task"
    )

    body = tk.Frame(
        window,
        bg=BG
    )

    body.pack(
        fill="both",
        expand=True,
        padx=35,
        pady=25
    )

    tk.Label(
        body,
        text="Enter task number:",
        bg=BG,
        fg=TEXT,
        font=("Arial", 10, "bold")
    ).pack()

    number_entry = tk.Entry(
        body,
        width=20,
        font=("Arial", 11)
    )

    style_entry(number_entry)

    number_entry.pack(
        pady=12,
        ipady=6
    )

    def complete():

        try:
            number = int(
                number_entry.get()
            )

            if number < 1 or number > len(tasks):
                messagebox.showwarning(
                    "Warning",
                    "Invalid task number."
                )
                return

            tasks[number - 1]["status"] = "Completed"

            update_saved_task(
                tasks[number - 1]
            )

            update_dashboard()

            window.destroy()

            show_message(
                "Task marked as completed!"
            )

        except ValueError:
            messagebox.showwarning(
                "Warning",
                "Enter a valid number."
            )

    make_action_button(
        body,
        "✓  MARK COMPLETED",
        complete,
        SUCCESS
    ).pack(pady=10)


# =========================================================
# SEARCH TASK
# =========================================================

def search_task():

    window = tk.Toplevel(root)
    window.title("Search Tasks")
    window.geometry("950x600")
    window.configure(bg=BG)

    popup_header(
        window,
        "SEARCH TASK",
        "Find a task quickly"
    )

    # Search area
    search_frame = tk.Frame(
        window,
        bg=BG
    )
    search_frame.pack(pady=20)

    tk.Label(
        search_frame,
        text="Search Task:",
        bg=BG,
        fg=TEXT,
        font=("Arial", 11, "bold")
    ).pack(side="left", padx=10)

    search_entry = tk.Entry(
        search_frame,
        width=45,
        font=("Arial", 12)
    )
    style_entry(search_entry)
    search_entry.pack(
        side="left",
        padx=10,
        ipady=6
    )

    # Table
    columns = (
        "No",
        "Task",
        "Priority",
        "Due Date",
        "Status"
    )

    table_frame = tk.Frame(
        window,
        bg=CARD,
        bd=1,
        relief="solid"
    )

    table_frame.pack(
        padx=50,
        pady=10,
        fill="both",
        expand=True
    )

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    for column in columns:
        table.heading(
            column,
            text=column
        )

    table.column(
        "No",
        width=80,
        anchor="center"
    )

    table.column(
        "Task",
        width=400
    )

    table.column(
        "Priority",
        width=180,
        anchor="center"
    )

    table.column(
        "Due Date",
        width=180,
        anchor="center"
    )

    table.column(
        "Status",
        width=180,
        anchor="center"
    )

    table.pack(
        padx=15,
        pady=15,
        fill="both",
        expand=True
    )

    # Search function
    def search():

        for item in table.get_children():
            table.delete(item)

        keyword = search_entry.get().lower().strip()

        found = False

        for i, task in enumerate(tasks):

            if keyword in task["name"].lower():

                table.insert(
                    "",
                    "end",
                    values=(
                        i + 1,
                        task["name"],
                        task["priority"],
                        task["due_date"],
                        task["status"]
                    )
                )

                found = True

        if not found:

            table.insert(
                "",
                "end",
                values=(
                    "",
                    "No matching task found",
                    "",
                    "",
                    ""
                )
            )

    # Search button
    make_action_button(
        search_frame,
        "⌕  SEARCH",
        search,
        PRIMARY,
        15
    ).pack(
        side="left",
        padx=10
    )

    # Search automatically while typing
    search_entry.bind(
        "<KeyRelease>",
        lambda event: search()
    )

    # Show all tasks initially
    search()

# =========================================================
# SAVE ONLY SELECTED TASK
# =========================================================

def save_tasks():

    if len(tasks) == 0:
        messagebox.showinfo(
            "Save Task",
            "No tasks available."
        )
        return

    window = tk.Toplevel(root)
    window.title("Save Task")
    window.geometry("400x330")
    window.resizable(False, False)
    window.configure(bg=BG)

    popup_header(
        window,
        "SAVE TASK",
        "Save only the task you choose"
    )

    body = tk.Frame(
        window,
        bg=BG
    )

    body.pack(
        fill="both",
        expand=True,
        padx=35,
        pady=25
    )

    tk.Label(
        body,
        text="Enter task number:",
        bg=BG,
        fg=TEXT,
        font=("Arial", 10, "bold")
    ).pack()

    number_entry = tk.Entry(
        body,
        width=20,
        font=("Arial", 11)
    )

    style_entry(number_entry)

    number_entry.pack(
        pady=12,
        ipady=6
    )

    def save_selected():

        try:
            number = int(
                number_entry.get()
            )

            if number < 1 or number > len(tasks):
                messagebox.showwarning(
                    "Warning",
                    "Invalid task number."
                )
                return

            selected_task = tasks[
                number - 1
            ]

            saved_tasks = read_saved_tasks()

            for saved_task in saved_tasks:

                if saved_task.get(
                    "name",
                    ""
                ).lower() == selected_task[
                    "name"
                ].lower():

                    messagebox.showinfo(
                        "Save Task",
                        "This task is already saved."
                    )

                    return

            saved_tasks.append(
                selected_task
            )

            if write_saved_tasks(
                saved_tasks
            ):

                window.destroy()

                show_message(
                    "Task saved successfully!"
                )

            else:
                messagebox.showerror(
                    "Error",
                    "Unable to save task."
                )

        except ValueError:

            messagebox.showwarning(
                "Warning",
                "Enter a valid number."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                "Could not save task:\n" + str(e)
            )

    make_action_button(
        body,
        "💾  SAVE TASK",
        save_selected
    ).pack(pady=10)


# =========================================================
# CLEAR ALL SAVED TASKS
# =========================================================

def clear_saved_tasks():

    saved_tasks = read_saved_tasks()

    if len(saved_tasks) == 0:
        messagebox.showinfo(
            "Clear Saved Tasks",
            "No saved tasks found."
        )
        return

    answer = messagebox.askyesno(
        "Clear Saved Tasks",
        "Are you sure you want to delete ALL saved tasks?"
    )

    if answer:

        if write_saved_tasks([]):

            tasks.clear()

            update_dashboard()

            messagebox.showinfo(
                "Clear Saved Tasks",
                "All saved tasks have been deleted."
            )

        else:

            messagebox.showerror(
                "Error",
                "Could not clear saved tasks."
            )


# =========================================================
# EXIT
# =========================================================

def exit_program():
    # Do NOT save all tasks here.
    root.destroy()


# =========================================================
# LOGIN
# =========================================================

def login():

    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "1234":

        login_window.destroy()

        open_dashboard()

    else:

        messagebox.showerror(
            "Login Failed",
            "Invalid username or password."
        )


# =========================================================
# DASHBOARD
# =========================================================

def open_dashboard():

    global root
    global message_label
    global total_label
    global pending_label
    global completed_label
    global overdue_label
    global progress_bar
    global progress_text

    root = tk.Tk()

    # Professional nude/beige styling
    style = ttk.Style(root)

    try:
        style.theme_use("clam")
    except:
        pass

    style.configure(
        "Treeview",
        background=CARD,
        fieldbackground=CARD,
        foreground=TEXT,
        rowheight=32,
        font=("Arial", 10)
    )

    style.configure(
        "Treeview.Heading",
        background=PRIMARY_DARK,
        foreground="white",
        font=("Arial", 10, "bold")
    )

    style.configure(
        "TCombobox",
        fieldbackground=CARD,
        background=CARD,
        foreground=TEXT,
        padding=6
    )

    style.configure(
        "Horizontal.TProgressbar",
        troughcolor=ACCENT,
        background=PRIMARY,
        bordercolor=ACCENT,
        lightcolor=PRIMARY,
        darkcolor=PRIMARY
    )

    root.title("To-Do List Application")
    root.state("zoomed")
    root.configure(bg=BG)

    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    header = tk.Frame(
        root,
        bg=PRIMARY,
        height=105
    )

    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="✓  MY TO-DO LIST",
        bg=PRIMARY,
        fg="white",
        font=("Arial", 27, "bold")
    ).pack(pady=(18, 2))

    tk.Label(
        header,
        text="Task Management System",
        bg=PRIMARY,
        fg="#F3EDE6",
        font=("Arial", 11)
    ).pack()

    # -----------------------------------------------------
    # DASHBOARD CARDS
    # -----------------------------------------------------

    card_frame = tk.Frame(
        root,
        bg=BG
    )

    card_frame.pack(pady=20)

    def create_card(
        text,
        column,
        text_color
    ):

        card = tk.Frame(
            card_frame,
            bg=CARD,
            width=200,
            height=95,
            bd=1,
            relief="solid"
        )

        card.grid(
            row=0,
            column=column,
            padx=7
        )

        card.grid_propagate(False)

        label = tk.Label(
            card,
            text=text,
            bg=CARD,
            fg=text_color,
            font=("Arial", 14, "bold")
        )

        label.pack(
            expand=True
        )

        return label

    total_label = create_card(
        "TOTAL TASKS\n0",
        0,
        PRIMARY
    )

    pending_label = create_card(
        "PENDING\n0",
        1,
        WARNING
    )

    completed_label = create_card(
        "COMPLETED\n0",
        2,
        SUCCESS
    )

    overdue_label = create_card(
        "OVERDUE\n0",
        3,
        DANGER
    )

    # -----------------------------------------------------
    # PROGRESS BAR
    # -----------------------------------------------------

    progress_text = tk.Label(
        root,
        text="Completion Progress: 0%",
        bg=BG,
        fg=TEXT,
        font=("Arial", 12, "bold")
    )

    progress_text.pack(
        pady=(8, 4)
    )

    style.configure(
        "Custom.Horizontal.TProgressbar",
        troughcolor=ACCENT,
        background=PRIMARY,
        bordercolor=ACCENT,
        lightcolor=PRIMARY,
        darkcolor=PRIMARY
    )

    progress_bar = ttk.Progressbar(
        root,
        orient="horizontal",
        length=650,
        mode="determinate",
        style="Custom.Horizontal.TProgressbar"
    )

    progress_bar.pack(pady=5)

    # -----------------------------------------------------
    # MESSAGE
    # -----------------------------------------------------

    message_label = tk.Label(
        root,
        text="",
        bg=BG,
        fg=SUCCESS,
        font=("Arial", 11, "bold")
    )

    message_label.pack(pady=7)

    # -----------------------------------------------------
    # MENU
    # -----------------------------------------------------

    tk.Label(
        root,
        text="MENU",
        bg=BG,
        fg=TEXT,
        font=("Arial", 18, "bold")
    ).pack(pady=8)

    menu_frame = tk.Frame(
        root,
        bg=BG
    )

    menu_frame.pack()

    buttons = [
        ("1.  Add Task", add_task, PRIMARY),
        ("2.  View Tasks", view_tasks, PRIMARY),
        ("3.  Delete Task", delete_task, DANGER),
        ("4.  Update Task", update_task, PRIMARY),
        ("5.  Mark Completed", mark_completed, SUCCESS),
        ("6.  Search Task", search_task, PRIMARY),
        ("7.  Save Tasks", save_tasks, SUCCESS),
        ("8.  Clear Saved Tasks", clear_saved_tasks, DANGER)
    ]

    for i, (text, command, color) in enumerate(buttons):

        row = i // 2
        column = i % 2

        btn = tk.Button(
            menu_frame,
            text=text,
            width=27,
            height=2,
            command=command,
            bg=color,
            fg="white",
            activebackground=(
                PRIMARY_DARK
                if color == PRIMARY
                else color
            ),
            activeforeground="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2"
        )

        btn.grid(
            row=row,
            column=column,
            padx=10,
            pady=6
        )

    exit_btn = tk.Button(
        menu_frame,
        text="9.  Exit",
        width=27,
        height=2,
        command=exit_program,
        bg="#6B625B",
        fg="white",
        activebackground="#4E4843",
        activeforeground="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        bd=0,
        cursor="hand2"
    )

    exit_btn.grid(
        row=4,
        column=0,
        columnspan=2,
        pady=6
    )

    # -----------------------------------------------------
    # UPDATE DASHBOARD
    # -----------------------------------------------------

    update_dashboard()

    root.after(
        500,
        check_reminders
    )

    root.mainloop()


# =========================================================
# LOGIN WINDOW
# =========================================================

load_tasks()

login_window = tk.Tk()

login_window.title("Login")
login_window.state("zoomed")
login_window.resizable(True, True)
login_window.configure(bg=BG)

# ---------------------------------------------------------
# LOGIN HEADER
# ---------------------------------------------------------

login_header = tk.Frame(
    login_window,
    bg=PRIMARY,
    height=120
)

login_header.pack(fill="x")
login_header.pack_propagate(False)

tk.Label(
    login_header,
    text="✓  TO-DO LIST",
    bg=PRIMARY,
    fg="white",
    font=("Arial", 25, "bold")
).pack(pady=(25, 5))

tk.Label(
    login_header,
    text="Task Management System",
    bg=PRIMARY,
    fg="#F3EDE6",
    font=("Arial", 10)
).pack()

# ---------------------------------------------------------
# LOGIN BODY
# ---------------------------------------------------------

login_body = tk.Frame(
    login_window,
    bg=BG
)
login_body.pack(
    fill="both",
    expand=True,
    padx=80,
    pady=40
)

# Username
tk.Label(
    login_body,
    text="Username",
    bg=BG,
    fg=TEXT,
    font=("Arial", 11, "bold")
).grid(
    row=0,
    column=0,
    padx=15,
    pady=20,
    sticky="e"
)

username_entry = tk.Entry(
    login_body,
    width=30,
    font=("Arial", 11)
)
style_entry(username_entry)

username_entry.grid(
    row=0,
    column=1,
    padx=15,
    pady=20,
    ipady=6
)

# Password
tk.Label(
    login_body,
    text="Password",
    bg=BG,
    fg=TEXT,
    font=("Arial", 11, "bold")
).grid(
    row=1,
    column=0,
    padx=15,
    pady=20,
    sticky="e"
)

password_entry = tk.Entry(
    login_body,
    width=30,
    show="*",
    font=("Arial", 11)
)
style_entry(password_entry)

password_entry.grid(
    row=1,
    column=1,
    padx=15,
    pady=20,
    ipady=6
)

# Login button
make_action_button(
    login_body,
    "LOGIN",
    login,
    PRIMARY,
    20
).grid(
    row=2,
    column=0,
    columnspan=2,
    pady=20
)

# Login details
tk.Label(
    login_body,
    text="Username: admin    Password: 1234",
    bg=BG,
    fg=MUTED,
    font=("Arial", 10)
).grid(
    row=3,
    column=0,
    columnspan=2,
    pady=10
)
login_window.mainloop()