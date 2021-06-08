import tkinter
import tkinter.messagebox
import sqlite3

conn = sqlite3.connect("task.db")

c = conn.cursor()

#Database operations

#c.execute("""DROP TABLE tasks""")

#c.execute("""CREATE TABLE tasks (
 #           task TEXT NOT NULL
  #          )""")

#c.execute("SELECT * FROM tasks")

#c.execute("""DROP TABLE tasks""")

conn.commit()

root = tkinter.Tk()
root.title("Todo List")

#database functions

def insert_task(task):
    with conn:
        c.execute("INSERT INTO tasks VALUES (:task)", {'task': task})

def remove_task(to_be_deleted):
    with conn:
        c.execute("DELETE FROM tasks WHERE ROWID = :ROWID", {"ROWID": to_be_deleted})

#functions
def add_task():
    task = entry_task.get()
    c.execute("SELECT task FROM tasks")
    if task != "":
        insert_task(task)
        load_tasks()
        entry_task.delete(0, tkinter.END)
    else:
        tkinter.messagebox.showwarning(title="Warning!", message="You must enter a task.")

def delete_task():
    try:
        rowid_value = listbox_id.get(listbox_tasks.curselection()[0])
        remove_task(rowid_value)
        load_tasks()
    except:
        tkinter.messagebox.showwarning(title="Warning!", message="You must select a task.")

def load_tasks():
    try:
        listbox_tasks.delete(0, tkinter.END)
        listbox_id.delete(0, tkinter.END)
        c.execute("SELECT ROWID, task FROM tasks")
        all_data = c.fetchall()
        for task in range(len(all_data)):
            listbox_tasks.insert(tkinter.END, all_data[task][1])
            listbox_id.insert(tkinter.END, all_data[task][0])
    except:
        tkinter.messagebox.showwarning(title="Warning!", message="Cannot find task.dat")


#GUI
frame_tasks = tkinter.Frame(root)
frame_tasks.pack()

listbox_id = tkinter.Listbox(frame_tasks, height=10, width=10)
listbox_id.pack(side=tkinter.LEFT)

listbox_tasks = tkinter.Listbox(frame_tasks, height=10, width=40)
listbox_tasks.pack(side=tkinter.LEFT)

scrollbar_tasks = tkinter.Scrollbar(frame_tasks)
scrollbar_tasks.pack(side=tkinter.RIGHT, fill=tkinter.Y)

listbox_tasks.config(yscrollcommand=scrollbar_tasks.set)
scrollbar_tasks.config(command=listbox_tasks.yview)

entry_task = tkinter.Entry(root, width=50)
entry_task.pack()

button_add_task = tkinter.Button(root, text = "Add task", width = 48, command = add_task)
button_add_task.pack()

button_delete_task = tkinter.Button(root, text="Delete task", width=48, command=delete_task)
button_delete_task.pack()

button_load_tasks = tkinter.Button(root, text = "Load tasks", width = 48, command = load_tasks)#needs change-->probably delete
button_load_tasks.pack()

root.mainloop()

conn.close()