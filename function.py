def refresh(filter_type="all"):
    """به‌روزرسانی جدول بر اساس فیلتر انتخاب‌شده"""
    for row in tree.get_children():
        tree.delete(row)

    if filter_type == "done":
        cur.execute("SELECT * FROM tasks WHERE done=1 ORDER BY due_date")
    elif filter_type == "pending":
        cur.execute("SELECT * FROM tasks WHERE done=0 ORDER BY due_date")
    else:
        cur.execute("SELECT * FROM tasks ORDER BY due_date")

    for row in cur.fetchall():
        color = "#5cb85c" if row[3] else "#f0ad4e"
        tree.insert("", tk.END, values=row, tags=("colored",))
        tree.tag_configure("colored", background=color)

def add_task():
    title = entry_title.get().strip()
    due_date = entry_date.get().strip()

    if not title:
        messagebox.showwarning("خطا", "عنوان نمی‌تواند خالی باشد!")
        return

    cur.execute("INSERT INTO tasks (title, due_date) VALUES (?, ?)", (title, due_date))
    conn.commit()
    entry_title.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    refresh(filter_var.get())

def delete_task():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("اخطار", "هیچ وظیفه‌ای انتخاب نشده است.")
        return

    for sel in selected:
        task_id = tree.item(sel)["values"][0]
        cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    refresh(filter_var.get())

def complete_task():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("اخطار", "ابتدا یک وظیفه انتخاب کنید.")
        return
    for sel in selected:
        task_id = tree.item(sel)["values"][0]
        cur.execute("UPDATE tasks SET done=1 WHERE id=?", (task_id,))
    conn.commit()
    refresh(filter_var.get())

def edit_task():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("اخطار", "هیچ وظیفه‌ای انتخاب نشده است.")
        return
    item = tree.item(selected[0])["values"]
    new_title = entry_title.get().strip()
    new_date = entry_date.get().strip()
    if not new_title:
        messagebox.showwarning("خطا", "عنوان جدید نمی‌تواند خالی باشد.")
        return
    cur.execute("UPDATE tasks SET title=?, due_date=? WHERE id=?", (new_title, new_date, item[0]))
    conn.commit()
    entry_title.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    refresh(filter_var.get())

def notify_today_tasks():
    today = datetime.today().strftime("%Y-%m-%d")
    cur.execute("SELECT title FROM tasks WHERE due_date=? AND done=0", (today,))
    tasks = [t[0] for t in cur.fetchall()]
    if tasks:
        notification.notify(
            title="یادآوری وظایف امروز 🕒",
            message="\n".join(tasks),
            timeout=10
        )