import psycopg2
import tkinter
import mysql.connector
import sqlite3

root = tkinter.Tk()
root.title('Web')
root.geometry("500x550+0+0")
root.resizable(width=False, height=False)
frame1 = tkinter.Frame(root)
frame1.pack()
lb1 = tkinter.Listbox(frame1)


def executeQuery(query):
    sqliteConnection = sqlite3.connect('MovieSite.db')
    cur = sqliteConnection.cursor()

    cur.execute(query)

    record = cur.fetchall()

    reloadListBox(record)
    cur.close()


def reloadListBox(record):
    lb1.delete(0, lb1.size())

    for i, movie in enumerate(record):
        lb1.insert(i, movie[0])
        print(lb1.get(i))

    lb1.pack()


def moreInfo():
    window = tkinter.Tk()
    window.title("More Movie Info")
    sqliteConnection = sqlite3.connect('MovieSite.db')
    cur = sqliteConnection.cursor()

    frm_form = tkinter.Frame(relief=tkinter.SUNKEN, borderwidth=3)
    frm_form.pack()

    labels = [
        "Title:",
        "Plot:",
        "Length:",
        "Year:",
        "genre:",
        "Rating;",
        "company name:",
        "Actor:",
    ]

    q = lb1.get(lb1.curselection())
    query = f"""select * from movies where title LIKE '%{q}%' """
    cur.execute(query)
    record = cur.fetchall()

    for idx, i in enumerate(labels):
        label = tkinter.Label(window, text=i)
        label2 = tkinter.Label(window, width=50, wraplength=200, text=record[0][idx])

        label.grid(row=idx, column=0, sticky="e")
        label2.grid(row=idx, column=1)

    watched = tkinter.Button(window, text="add to watched list", command=lambda: addWatched())
    watched.grid(row=9, column=1)

    window.mainloop()


def addWatched():
    sqliteConnection = sqlite3.connect('MovieSite.db')
    cur = sqliteConnection.cursor()
    q = lb1.get(lb1.curselection())
    insert = f"""INSERT into watched(user_id, title) VALUES ('1', '%{q}%') """
    cur.execute(insert)
    record = cur.fetchall()
    print(record)


def showWatch():
    query = """select title from watched"""
    executeQuery(query)


def search():
    q = entry1.get()
    g = entry2.get()
    a = entry3.get()

    query = """select * from movies """

    if len(q.split(" ")) == 0 and len(g.split(" ")) == 0 and len(a.split(" ")) == 0:
        executeQuery(query)
    else:
        query += "WHERE "
        addAnd = False
        if len(q.split(" ")) > 0:
            if addAnd is True:
                query += "AND "
            query += f"title LIKE '%{q}%' "
            addAnd = True
        if len(g.split(" ")) > 0:
            if addAnd is True:
                query += "AND "
            query += f"genre LIKE '%{g}%' "
            addAnd = True
        if len(a.split(" ")) > 0:
            if addAnd is True:
                query += "AND "
            query += f"actor_name LIKE '%{a}%' "
        executeQuery(query)


info = tkinter.Button(frame1, text="More Movie info", command=lambda: moreInfo())

label1 = tkinter.Label(frame1, text="Search By Title")
entry1 = tkinter.Entry(frame1, width=50)

label1.pack()
entry1.pack()

label2 = tkinter.Label(frame1, text="Search By Genre")
entry2 = tkinter.Entry(frame1, width=50)
label2.pack()
entry2.pack()

label3 = tkinter.Label(frame1, text="Search By Actor")
entry3 = tkinter.Entry(frame1, width=50)
submit1 = tkinter.Button(frame1, text="Search", command=lambda: search())
show = tkinter.Button(frame1, text="show watched", command=lambda: showWatch())
label3.pack()
entry3.pack()
submit1.pack()
show.pack()
info.pack()

sqliteConnection = sqlite3.connect('MovieSite.db')
cursor = sqliteConnection.cursor()

sqlite_select_Query = 'SELECT title FROM movies'
cursor.execute(sqlite_select_Query)
record = cursor.fetchall()

cursor.close()
reloadListBox(record)
root.mainloop()
