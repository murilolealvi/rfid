
import customtkinter as ctk
from tkinter import *
from CTkTable import CTkTable
#from tkcalendar import Calendar, DateEntry

from database.mongo import MongodbConnectionHandler
from services.register import RegisterHandler
from services.authenticate import AuthenticationHandler
from services.log import LogHandler
from models.person import *

from serial import Serial
import numpy as np

serial_tty = "/dev/ttyUSB0"
mongo_conn = MongodbConnectionHandler(db="rfid").connect()
registration = RegisterHandler(mongo_conn, 'tag')
authentication = AuthenticationHandler(mongo_conn, 'tag')
logging = LogHandler(mongo_conn, 'log')


def read_tag():
    register_button.configure(state=DISABLED)
    register_tag_id.configure(text=str())
    register_info_label.configure(text=str())
    ser = Serial(port=serial_tty, baudrate=9600, timeout=3)
    serial_id = ser.readline().decode("utf-8")[:-2]
    check = authentication.check(serial_id)
    if serial_id and check == False:
        register_tag_id.configure(text=serial_id)
        register_button.configure(state=NORMAL)
        register_info_label.configure(text="Tag successfully identified!")
    elif serial_id and check:
        register_info_label.configure(text="Tag already registered, erase it before use!")
    else:
        register_info_label.configure(text="Tag not identified, failed to read...")

def register_tag():
    if register_username_entry.get():
        new_user = Person(id=register_tag_id.cget('text'), name=register_username_entry.get())
        registration_table.add_row([register_tag_id.cget('text'),register_username_entry.get(),now()])
        registration.register(new_user)
        register_info_label.configure(text="New user successfully registered!")
        register_username_entry.delete(0,END)
        register_button.configure(state=DISABLED)
        register_tag_id.configure(text=str())
    else:
        register_info_label.configure(text="Insert a name to register...")

def authenticate_by_id():
    check_username_entry.delete(0,END)
    ser = Serial(port=serial_tty, baudrate=9600, timeout=3)
    serial_id = ser.readline().decode("utf-8")[:-2]
    search_user = authentication.authenticate(serial_id, "id")
    if serial_id and search_user:
        check_username_entry.insert(END, search_user["name"])
        check_tag_id.configure(text=search_user["id"])
        check_info_label.configure(text="User authenticated!")
    elif serial_id:
        check_username_entry.delete(0,END)
        check_tag_id.configure(text=str())
        check_info_label.configure(text="User not found, try registering it first...")
    else:
        check_username_entry.delete(0,END)
        check_tag_id.configure(text=str())
        check_info_label.configure(text="Tag not identified, failed to read...")

def authenticate_by_name():
    user = check_username_entry.get()
    search_user = authentication.authenticate(user, "name")
    if search_user:
        check_tag_id.configure(text=search_user["id"])
        check_info_label.configure(text="User authenticated!")
    else:
        check_username_entry.delete(0,END)
        check_tag_id.configure(text=str())
        check_info_label.configure(text="User not found, try registering it first...")

def erase_by_name():
    erase_button.configure(state=DISABLED)
    user = erase_username_entry.get()
    search_user = authentication.authenticate(user, "name")
    if search_user:
        erase_tag_id.configure(text=search_user["id"])
        erase_info_label.configure(text="User found!")
        erase_button.configure(state=NORMAL)
    else:
        erase_username_entry.delete(0,END)
        erase_tag_id.configure(text=str())
        erase_info_label.configure(text="User not found, try registering it first...")

def erase_by_id():
    erase_username_entry.delete(0,END)
    erase_button.configure(state=DISABLED)
    ser = Serial(port=serial_tty, baudrate=9600, timeout=3)
    serial_id = ser.readline().decode("utf-8")[:-2]
    search_user = authentication.authenticate(serial_id, "id")
    if serial_id and search_user:
        erase_username_entry.insert(END, search_user["name"])
        erase_tag_id.configure(text=search_user["id"])
        erase_info_label.configure(text="User found!")
        erase_button.configure(state=NORMAL)
    elif serial_id:
        erase_username_entry.delete(0,END)
        erase_tag_id.configure(text=str())
        erase_info_label.configure(text="User not found, try registering it first...")
    else:
        erase_username_entry.delete(0,END)
        erase_tag_id.configure(text=str())
        erase_info_label.configure(text="Tag not identified, failed to read...")

def erase():
    registration.erase(erase_tag_id.cget("text"))
    erase_row = np.array(registration_table.get())
    registration_table.delete_row(*np.where(erase_row==erase_tag_id.cget("text"))[0])
    erase_info_label.configure(text="Tag successfully erased!")
    erase_username_entry.delete(0,END)
    erase_tag_id.configure(text=str())
    erase_button.configure(state=DISABLED)

def check_logs():
    logs = list(set(logging.timelogs) - set(logging_table.get_column(2)))
    for log in logs[::-1]:
        entry = logging.find(log)
        logging_table.add_row(index=1,values=[entry["name"], entry["date"], log])

window = ctk.CTk()
icon = PhotoImage(file="./icon.png")
window.iconphoto(True,icon)
window.title("RFID System")
window.geometry("750x750")
window.maxsize(width=750, height=750)
window.minsize(width=750, height=750)
ctk.set_default_color_theme("dark-blue")


tabview = ctk.CTkTabview(master=window, corner_radius=10, 
                         width=700, height=700)
tabview.add("Register")
tabview.add("Check")
tabview.add("Erase")
tabview.add("List")
tabview.pack()



# Register tab
register_username_label = ctk.CTkLabel(master=tabview.tab("Register"), text="Username:", font=("Arial",20))
register_username_label.grid(row=0, column=0, padx=50, pady=100)

register_username_entry = ctk.CTkEntry(master=tabview.tab("Register"), width=300, height=40, font=("Arial",18), placeholder_text="User")
register_username_entry.grid(row=0, column=1, padx=50, pady=50)

register_tag_label = ctk.CTkLabel(master=tabview.tab("Register"), text="Tag ID:", font=("Arial",20), corner_radius=0.5)
register_tag_label.grid(row=1, column=0, padx=20, pady=50)
register_tag_id = ctk.CTkLabel(master=tabview.tab("Register"), text=str(), font=("Arial",20, "bold"), corner_radius=0.5)
register_tag_id.grid(row=1, column=1, padx=20, pady=20)

register_button = ctk.CTkButton(master=tabview.tab("Register"), text="Register", font=("Arial",20),
                            corner_radius=20, state=DISABLED, height=75, command=register_tag, fg_color="#2A8C55")
register_button.grid(row=4, column=0, padx=65, pady=20, sticky="w")

check_button = ctk.CTkButton(master=tabview.tab("Register"), text="Read Tag ID", font=("Arial",20),
                         corner_radius=20, command=read_tag, height=75)
check_button.grid(row=4, column=1, padx=65, pady=20, sticky="e")

register_info_label = ctk.CTkLabel(master=tabview.tab("Register"), text=str(), font=("Arial",18, "italic")) 
register_info_label.grid(row=3, column=0, padx=50, pady=20, columnspan=2)


# Authenticate tab
check_username_label = ctk.CTkLabel(master=tabview.tab("Check"), text="Username:", font=("Arial",20))
check_username_label.grid(row=0, column=0, padx=50, pady=100)
check_username_entry = ctk.CTkEntry(master=tabview.tab("Check"), width=300, height=40, font=("Arial",18), placeholder_text="User")
check_username_entry.grid(row=0, column=1, padx=50, pady=50)

check_tag_label = ctk.CTkLabel(master=tabview.tab("Check"), text="Tag ID:", font=("Arial",20), corner_radius=0.5)
check_tag_label.grid(row=1, column=0, padx=20, pady=50)

check_tag_id = ctk.CTkLabel(master=tabview.tab("Check"), text=str(), font=("Arial",20, "bold"), corner_radius=0.5)
check_tag_id.grid(row=1, column=1, padx=20, pady=20)

search_name_button = ctk.CTkButton(master=tabview.tab("Check"), text="By Name", font=("Arial",20),
                            corner_radius=20, height=75, command=authenticate_by_name)
search_name_button.grid(row=5, column=0, padx=65, pady=20, sticky="w")

search_id_button = ctk.CTkButton(master=tabview.tab("Check"), text="By Tag ID", font=("Arial",20),
                         corner_radius=20, height=75, command=authenticate_by_id)
search_id_button.grid(row=5, column=1, padx=65, pady=20, sticky="e")

check_modes_label = ctk.CTkLabel(master=tabview.tab("Check"), text="Validation Modes:", font=("Arial",16)) 
check_modes_label.grid(row=4, column=0, padx=20, pady=0, columnspan=2)

check_info_label = ctk.CTkLabel(master=tabview.tab("Check"), text=str(), font=("Arial",18, "italic")) 
check_info_label.grid(row=3, column=0, padx=50, pady=50, columnspan=2)


# Erase tab
erase_username_label = ctk.CTkLabel(master=tabview.tab("Erase"), text="Username:", font=("Arial",20))
erase_username_label.grid(row=0, column=0, padx=50, pady=100)
erase_username_entry = ctk.CTkEntry(master=tabview.tab("Erase"), width=300, height=40, font=("Arial",18), placeholder_text="User")
erase_username_entry.grid(row=0, column=1, padx=50, pady=50)

erase_tag_label = ctk.CTkLabel(master=tabview.tab("Erase"), text="Tag ID:", font=("Arial",20), corner_radius=0.5)
erase_tag_label.grid(row=1, column=0, padx=20, pady=30)

erase_tag_id = ctk.CTkLabel(master=tabview.tab("Erase"), text=str(), font=("Arial",20, "bold"), corner_radius=0.5)
erase_tag_id.grid(row=1, column=1, padx=20, pady=20)

erase_search_name_button = ctk.CTkButton(master=tabview.tab("Erase"), text="By Name", font=("Arial",20),
                            corner_radius=20, height=75, command=erase_by_name)
erase_search_name_button.grid(row=5, column=0, padx=65, pady=20, sticky="w")

erase_search_id_button = ctk.CTkButton(master=tabview.tab("Erase"), text="By Tag ID", font=("Arial",20),
                         corner_radius=20, height=75, command=erase_by_id)
erase_search_id_button.grid(row=5, column=1, padx=65, pady=20, sticky="e")

erase_button = ctk.CTkButton(master=tabview.tab("Erase"), text="Erase", font=("Arial",20),
                         corner_radius=20, height=40, fg_color='#f00', state=DISABLED, command=erase)
erase_button.grid(row=6, column=0, columnspan=2)

delete_modes_label = ctk.CTkLabel(master=tabview.tab("Erase"), text="Delete Modes:", font=("Arial",16)) 
delete_modes_label.grid(row=4, column=0, padx=20, pady=0, columnspan=2)

erase_info_label = ctk.CTkLabel(master=tabview.tab("Erase"), text=str(), font=("Arial",18, "italic")) 
erase_info_label.grid(row=3, column=0, padx=50, pady=50, columnspan=2)


# List tab
tables = ctk.CTkTabview(master=tabview.tab("List"), corner_radius=10, width=600, height=600, 
                        segmented_button_selected_color="#0384fc", command=check_logs)
tables.add("Registration")
tables.add("Log")
tables.pack(side=BOTTOM, expand=True)

log_label = ctk.CTkLabel(master=tables.tab("Log"), text="Logging Table", font=("Arial",20))
log_label.pack(expand=True)
#date_selector = DateEntry(master=tables.tab("Log"), selectmode='day', date_pattern= 'dd/mm/y')
#date_selector.pack(expand=True)
#print(date_selector.get_date().strftime("%d/%m/%Y"))

registration_label = ctk.CTkLabel(master=tables.tab("Registration"), text="Registration Table", font=("Arial",20))
registration_label.pack(expand=True)

#Registration table
registration_table_frame = ctk.CTkScrollableFrame(master=tables.tab("Registration"), fg_color="transparent")
registration_table_frame.pack(expand=True, fill="both")
registration_headers = np.array(["Tag ID", "Name", "Date"])
if authentication.user_exists():
    registration_table_values = np.vstack((registration_headers, authentication.all_users())) 
else:
    registration_table_values = [registration_headers]
registration_table = CTkTable(master=registration_table_frame, values=list(registration_table_values), header_color="#7d32a8", font=("Arial",16))
registration_table.pack(expand=True, fill="both", padx=20, pady=20)

#Logging table
logging_table_frame = ctk.CTkScrollableFrame(master=tables.tab("Log"), fg_color="transparent")
logging_table_frame.pack(expand=True, fill="both")
logging_headers = np.array(["Name", "Date", "Time"])
if logging.log_exists():
    logging_table_values = np.vstack((logging_headers, logging.dump())) 
else:
    logging_table_values = [logging_headers]
logging_table = CTkTable(master=logging_table_frame, values=list(logging_table_values), header_color="#7d32a8", font=("Arial",16))
logging_table.pack(expand=True, fill="both", padx=20, pady=20)



window.mainloop()


