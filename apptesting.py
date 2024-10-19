


from database.mongo import MongodbConnectionHandler
from services.register import RegisterHandler
from services.authenticate import AuthenticationHandler
from models.person import Person

import tkinter
from tkinter import messagebox

mongo_conn = MongodbConnectionHandler(db="rfid").connect()

registration_handler = RegisterHandler(mongo_conn, 'database')
authentication = AuthenticationHandler(mongo_conn)

window = tkinter.Tk()
window.title("RFID Registry")
window.geometry('440x640')
window.configure(bg='#333333')

frame = tkinter.Frame(bg='#333333')


registration_label = tkinter.Label(frame, text="Register")
username_label = tkinter.Label(frame, text="Name")
username_entry = tkinter.Entry(window)
tag_label = tkinter.Label(window, text="Tag ID")
register_button = tkinter.Button(window, text="Register")

registration_label.grid(row=0,column=0,columnspan=2)
username_label.grid(row=1,column=0)
username_entry.grid(row=1,column=1)
tag_label.grid(row=2,column=0)
register_button.grid(row=3,column=0,columnspan=2)

frame.pack()
window.mainloop()