
import customtkinter as ctk
from tkinter import *
from datetime import datetime
from CTkTable import CTkTable

from database.mongo import MongodbConnectionHandler
from services.register import RegisterHandler
from services.authenticate import AuthenticationHandler
from models.person import Person

mongo_conn = MongodbConnectionHandler(db="rfid").connect()

registration_handler = RegisterHandler(mongo_conn, 'tag')
authentication = AuthenticationHandler(mongo_conn)




window = ctk.CTk()
#window.iconbitmap
window.title("RFID Registry")
window.geometry("750x750")
window.resizable(0,0)
window.maxsize(width=750, height=750)
window.minsize(width=750, height=750)
window.resizable(width=True, height=True)
ctk.set_default_color_theme("dark-blue")


tabview = ctk.CTkTabview(master=window, corner_radius=10, width=700, height=700)
tabview.add("Register")
tabview.add("Authenticate")
tabview.add("Erase")
tabview.add("Log")
tabview.pack()

def now():
    return datetime.now().strftime("%d-%m-%Y %H:%M")
def read_tag():
    #read serial
    tag_id.configure(text=register_username_entry.get(), fg_color='#f00')

# a = Person(id=45,name='Murilo',last_time=now())
# registration_handler.register(a)


# Register tab
register_username_label = ctk.CTkLabel(master=tabview.tab("Register"), text="Username:", font=("Arial",20))
register_username_label.grid(row=0, column=0, padx=50, pady=100)

register_username_entry = ctk.CTkEntry(master=tabview.tab("Register"), width=300, height=40, font=("Arial",18), placeholder_text="User")
register_username_entry.grid(row=0, column=1, padx=50, pady=50)

tag_label = ctk.CTkLabel(master=tabview.tab("Register"), text="Tag ID:", font=("Arial",20), corner_radius=0.5)
tag_label.grid(row=1, column=0, padx=20, pady=50)
tag_id = ctk.CTkLabel(master=tabview.tab("Register"), text=str(), font=("Arial Bold",20), corner_radius=0.5)
tag_id.grid(row=1, column=1, padx=20, pady=20)

register_button = ctk.CTkButton(master=tabview.tab("Register"), text="Register", font=("Arial",20),
                            corner_radius=20, state=DISABLED, height=75)
register_button.grid(row=4, column=0, padx=55, pady=20, sticky="w")
#register_button.configure(state=NORMAL)

check_button = ctk.CTkButton(master=tabview.tab("Register"), text="Read Tag ID", font=("Arial",20),
                         corner_radius=20, command=read_tag, height=75)
check_button.grid(row=4, column=1, padx=55, pady=20, sticky="e")

info_label = ctk.CTkLabel(master=tabview.tab("Register"), text=str()) 
#, text=str(), font=("Arial Bold",16), fg_color='#f00'
info_label.grid(row=3, column=0, padx=50, pady=20, columnspan=2)


# Authenticate tab
username_label = ctk.CTkLabel(master=tabview.tab("Authenticate"), text="Username:", font=("Arial",18))
username_label.grid(row=0, column=0, padx=0, pady=20)
username_textbox = ctk.CTkEntry(master=tabview.tab("Authenticate"), width=200, height=40, font=("Arial",16))
username_textbox.grid(row=0, column=1, padx=20, pady=20)
tag_label = ctk.CTkLabel(master=tabview.tab("Authenticate"), text="Tag ID:", font=("Arial",18), corner_radius=0.5)
tag_label.grid(row=1, column=0, padx=20, pady=20)

search_name_button = ctk.CTkButton(master=tabview.tab("Authenticate"), text="By Name", font=("Arial",20),
                            corner_radius=20)
search_name_button.grid(row=5, column=0, padx=20, pady=20, sticky="w")

search_id_button = ctk.CTkButton(master=tabview.tab("Authenticate"), text="By Tag ID", font=("Arial",20),
                         corner_radius=20)
search_id_button.grid(row=5, column=1, padx=20, pady=20, sticky="e")

modes_label = ctk.CTkLabel(master=tabview.tab("Authenticate"), text="Authentication Modes:", font=("Arial",14)) 
modes_label.grid(row=4, column=0, padx=20, pady=0, columnspan=2)

info_label = ctk.CTkLabel(master=tabview.tab("Authenticate"), text=str()) 
#, text=str(), font=("Arial Bold",16), fg_color='#f00'
info_label.grid(row=3, column=0, padx=20, pady=20, columnspan=2)


# Erase tab
username_label = ctk.CTkLabel(master=tabview.tab("Erase"), text="Username:", font=("Arial",18))
username_label.grid(row=0, column=0, padx=0, pady=20)
username_textbox = ctk.CTkEntry(master=tabview.tab("Authenticate"), width=200, height=40, font=("Arial",16))
username_textbox.grid(row=0, column=1, padx=20, pady=20)
tag_label = ctk.CTkLabel(master=tabview.tab("Erase"), text="Tag ID:", font=("Arial",18), corner_radius=0.5)
tag_label.grid(row=1, column=0, padx=20, pady=20)

search_name_button = ctk.CTkButton(master=tabview.tab("Erase"), text="By Name", font=("Arial",20),
                            corner_radius=20)
search_name_button.grid(row=5, column=0, padx=20, pady=20, sticky="w")

search_id_button = ctk.CTkButton(master=tabview.tab("Erase"), text="By Tag ID", font=("Arial",20),
                         corner_radius=20)
search_id_button.grid(row=5, column=1, padx=20, pady=20, sticky="e")

modes_label = ctk.CTkLabel(master=tabview.tab("Erase"), text="Delete Modes:", font=("Arial",14)) 
modes_label.grid(row=4, column=0, padx=20, pady=0, columnspan=2)

info_label = ctk.CTkLabel(master=tabview.tab("Erase"), text=str()) 
#, text=str(), font=("Arial Bold",16), fg_color='#f00'
info_label.grid(row=3, column=0, padx=20, pady=20, columnspan=2)


# Log tab
tables = ctk.CTkTabview(master=tabview.tab("Log"), corner_radius=10, width=350, height=360)
tables.add("Log")
tables.add("Registration")
tables.pack(side=BOTTOM, expand=True)

log_label = ctk.CTkLabel(master=tables.tab("Log"), text="Logging Table", font=("Arial",18))
log_label.pack(expand=True)

registration_label = ctk.CTkLabel(master=tables.tab("Registration"), text="Registration Table", font=("Arial",18))
registration_label.pack(expand=True)

value = [[1,2,3,4,5],
         [1,2,3,4,5],
         [1,2,3,4,5],
         [1,2,3,4,5],
         [1,2,3,4,5],
         [1,2,3,4,5],
         [1,2,3,4,10],
         [1,2,3,4,5],
         [1,2,3,4,5],
         [1,2,3,4,5],
         [1,2,3,4,5],
         [1,2,3,4,5],
         [1,2,3,4,5],
         [1,2,3,4,10]]

table = CTkTable(master=tables.tab("Log"), row=5, column=5, values=value)


table_frame = ctk.CTkScrollableFrame(master=tables.tab("Log"), fg_color="transparent")
table_frame.pack(expand=True, fill="both")
table = CTkTable(master=table_frame, values=value, header_color="#2A8C55", hover_color="#B4B4B4")
table.pack(expand=True, fill="both", padx=20, pady=20)

window.mainloop()


