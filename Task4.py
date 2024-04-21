import sqlite3 as sql
from tkinter import *
from tkinter import messagebox
from  random import choice
try:
       con = sql.connect('Загадка записи.db')
       cur = con.cursor()
       cur.execute('''СОЗДАТЬ ТАБЛИЦУ notes_table
                        (date text, notes_title text, notes text)''')
except:
       print("Подключен к таблице базы данных")

btn = []
playArea = list(range(1, 16))
playArea.append(0)

def play(n):
    m = playArea.index(0)
    if abs(m - n) == 1 and n//4 == m//4 or abs(m - n) == 4:
        playArea[m], playArea[n] = playArea[n], playArea[m]
        btn[m].config(text=playArea[m])
        btn[n].config(text=" ")

for i in range(0, 4):
    frm = Frame()
    frm.pack(expand=YES, fill=BOTH)
    for j in  range(0, 4):
        btn += [Button(frm, text=playArea[i*4+j], font=('mono', 20, 'bold'),
                       width=3, height=2,
                       command=lambda n=i*4+j: play(n))]
        btn[i*4+j].pack(side=LEFT, expand=YES, fill=BOTH)

for i in range(0, 3000):
    play(choice(range(0, 16)))
mainloop()      

def add_notes():
       
       today = date_entry.get()
       notes_title = notes_title_entry.get()
       notes = notes_entry.get("1.0", "end-1c")
      
       if (len(today) <=0) & (len(notes_title)<=0) & (len(notes)<=1):
               messagebox.showerror(message = "ВВЕДИТЕ НЕОБХОДИМЫЕ ДАННЫЕ" )
       else:
            cur.execute("INSERT INTO notes_table VALUES ('%s','%s','%s')" %(today, notes_title, notes))
            messagebox.showinfo(message="Добавлена заметка")
       
            con.commit()

def view_notes():
       
       date = date_entry.get()
       notes_title = notes_title_entry.get()
    
       if (len(date) <=0) & (len(notes_title)<=0):
               sql_statement = "SELECT * FROM notes_table"

       elif (len(date) <=0) & (len(notes_title)>0):
               sql_statement = "SELECT * FROM notes_table where notes_title ='%s'" %notes_title
       
       elif (len(date) >0) & (len(notes_title)<=0):
               sql_statement = "SELECT * FROM notes_table where date ='%s'"%date
       
       else:
               sql_statement = "SELECT * FROM notes_table where date ='%s' and notes_title ='%s'" %(date, notes_title)
              
       cur.execute(sql_statement)
       row = cur.fetchall()
       
       if len(row)<=0:
               messagebox.showerror(message="Записка не найдена")
       else:
               for i in row:
                       messagebox.showinfo(message="Дата: "+i[0]+"\nTitle: "+i[1]+"\nЗаписи: "+i[2])

def delete_notes():
       date = date_entry.get()
       notes_title = notes_title_entry.get()
       choice = messagebox.askquestion(message="Вы хотите удалить все заметки?")
       
       if choice == 'да':
               sql_statement = "DELETE FROM notes_table" 
       else:
               if (len(date) <=0) & (len(notes_title)<=0): 
                       
                       messagebox.showerror(message = "ВВЕДИТЕ НЕОБХОДИМЫЕ ДАННЫЕ" )
                       return
               else:
                      sql_statement = "DELETE FROM notes_table where date ='%s' and notes_title ='%s'" %(date, notes_title)
       
       cur.execute(sql_statement)
       messagebox.showinfo(message="Запись(и) удалена(ы)")
       con.commit()

def update_notes():
       
       today = date_entry.get()
       notes_title = notes_title_entry.get()
       notes = notes_entry.get("1.0", "end-1c")
       
       if (len(today) <=0) & (len(notes_title)<=0) & (len(notes)<=1):
               messagebox.showerror(message = "ВВЕДИТЕ НЕОБХОДИМЫЕ ДАННЫЕ" )
       
       else:
                sql_statement = "UPDATE notes_table SET notes = '%s' where date ='%s' and notes_title ='%s'" %(notes, today, notes_title)
       cur.execute(sql_statement)
       messagebox.showinfo(message="Запись обновлена")
       con.commit()

window = Tk()

window.geometry("500x300")
window.title("Загадка записи")
 
title_label = Label(window, text="Закрепите свою заметку").pack()

date_label = Label(window, text="Дата:").place(x=10,y=20)
date_entry = Entry(window,  width=20)
date_entry.place(x=50,y=20)

notes_title_label = Label(window, text="Название:").place(x=10,y=50)
notes_title_entry = Entry(window,  width=30)
notes_title_entry.place(x=80,y=50)

notes_label = Label(window, text="Запись   :").place(x=10,y=90)
notes_entry = Text(window, width=50,height=5)
notes_entry.place(x=60,y=90)
 
button1 = Button(window,text='Добавить', bg = 'Turquoise',fg='Red',command=add_notes).place(x=10,y=190)
button2 = Button(window,text='Посмотреть', bg = 'Turquoise',fg='Red',command=view_notes).place(x=110,y=190)
button3 = Button(window,text='Удалить', bg = 'Turquoise',fg='Red',command=delete_notes).place(x=210,y=190)
button4 = Button(window,text='Обновить', bg = 'Turquoise',fg='Red',command=update_notes).place(x=320,y=190)
 
window.mainloop()
con.close()