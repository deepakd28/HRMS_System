# Core Tkinter and CustomTkinter imports
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from customtkinter import (
    CTkLabel, 
    CTkFrame, 
    CTkScrollableFrame, 
    CTkButton,
    CTkToplevel
)

from customtkinter import *
from tkinter import StringVar, Label

# Additional UI and Date Related
from tkcalendar import Calendar
from datetime import datetime
from tkinter import ttk


# Database Imports
from pymongo import MongoClient

# MongoDB insertion
client = MongoClient('ur mongo db url')
# client = MongoClient('mongodb://localhost:27017')  #oly for offline mode.
db = client['projectdb']
patient_collection = db['patient_record']
doctor_collection = db['doctor_record']
appointment_collection = db['appointment_record']
id_collection = db['id_records']
dept_collection = db['dept_record']
admin_collection = db['admin_record']
record_collection = db['medical_record']
btn_width = 300
btn_height = 70

# Global app reference to use across functions
app = None
frame = None

def clear_frame():
    """Clear all widgets in the frame."""
    for widget in frame.winfo_children():
        widget.destroy()

def login():
    clear_frame()
    
    # Add a label for the title inside the frame
    label = CTkLabel(master=frame, text="Login", font=("Arial", 24))
    label.grid(row=0, column=0, columnspan=2, pady=20)

    # Add username label and entry inside the frame
    username_label = CTkLabel(master=frame, text="Username")
    username_label.grid(row=1, column=0, padx=20, pady=10, sticky="e")

    username_entry = CTkEntry(master=frame, width=300)
    username_entry.grid(row=1, column=1, padx=20, pady=10)

    # Add password label and entry inside the frame
    password_label = CTkLabel(master=frame, text="Password")
    password_label.grid(row=2, column=0, padx=20, pady=10, sticky="e")

    password_entry = CTkEntry(master=frame, width=300, show="*")
    password_entry.grid(row=2, column=1, padx=20, pady=10)

    # Add user type label inside the frame
    user_type_label = CTkLabel(master=frame, text="User Type:")
    user_type_label.grid(row=3, column=0, padx=20, pady=10, sticky="e")

    radio_var = StringVar(value="")  # Change to StringVar to store user type directly

    # Add radio buttons in the same row with suitable padding
    radiobutton_doctor = CTkRadioButton(master=frame, text="Doctor", variable=radio_var, value="doctor")
    radiobutton_doctor.grid(row=3, column=1, padx=20, pady=5, sticky="w")

    radiobutton_admin = CTkRadioButton(master=frame, text="Admin", variable=radio_var, value="admin")
    radiobutton_admin.grid(row=3, column=1, padx=100, pady=5, sticky="w")

    radiobutton_patient = CTkRadioButton(master=frame, text="Patient", variable=radio_var, value="patient")
    radiobutton_patient.grid(row=3, column=1, padx=180, pady=5, sticky="w")

    def retrieve_input():
        username = username_entry.get()
        password = password_entry.get()
        user_type = radio_var.get()

        # Check if any field is empty
        if username == "" or password == "" or user_type == "":
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        # Validate user based on user type
        if user_type == "patient":
            # Check patient collection
            user_record = patient_collection.find_one({
                "name": username, 
                "password": password
            })
            if user_record:
                global user_id_apt, user_details
                user_details = user_record
                user_id_apt = user_record['user_id']
                patient_home()
                return

        elif user_type == "doctor":
            # Check doctor collection
            user_record = doctor_collection.find_one({
                "doc_name": username, 
                "password": password
            })
            if user_record:
                global doctor_details
                doctor_details = user_record
                doctor_home()
                return

        elif user_type == "admin":
            # Check admin collection (assuming you have an admin collection)
            user_record = admin_collection.find_one({
                "username": username, 
                "password": password
            })
            if user_record:
                global admin_details
                admin_details = user_record
                admin_home()
                return

        # If no matching record found
        messagebox.showerror("Invalid Credentials", "Invalid username, password, or user type.")
        print(f"Login failed for {username} as {user_type}")

    # Login button
    login_button = CTkButton(master=frame, text="Login", command=retrieve_input)
    login_button.grid(row=6, column=0, columnspan=2, pady=20)

    # Signup section
    signup_label = CTkLabel(master=frame, text="Don't have an account? Create one.")
    signup_label.grid(row=7, column=1, padx=60, pady=10, sticky="w")

    signup_button = CTkButton(master=frame, text="Signup", command=signup)
    signup_button.grid(row=8, column=0, columnspan=2, pady=20)
def signup():
    # Clear frame for signup UI
    for widget in frame.winfo_children():
        widget.destroy()

    # Add title
    label = CTkLabel(master=frame, text="Signup", font=("Arial", 24))
    label.grid(row=0, column=0, columnspan=2, pady=20)

    # Username label and entry
    username_label = CTkLabel(master=frame, text="Username")
    username_label.grid(row=1, column=0, padx=20, pady=10, sticky="e")

    username_entry = CTkEntry(master=frame, width=300)
    username_entry.grid(row=1, column=1, padx=20, pady=10)

    # Password label and entry
    password_label = CTkLabel(master=frame, text="Password")
    password_label.grid(row=2, column=0, padx=20, pady=10, sticky="e")

    password_entry = CTkEntry(master=frame, width=300, show="*")
    password_entry.grid(row=2, column=1, padx=20, pady=10)

    # Date of Birth Selection
    dob_label = CTkLabel(master=frame, text="Date of Birth")
    dob_label.grid(row=3, column=0, padx=20, pady=10, sticky="e")

    # Date display entry (read-only)
    date_display = CTkEntry(master=frame, width=200, state="readonly")
    date_display.grid(row=3, column=1, padx=20, pady=10, sticky="w")

    # Calendar frame
    calendar_frame = CTkFrame(master=frame)
    calendar_frame.grid(row=4, column=0, columnspan=2, pady=10)

    # Create calendar
    cal = Calendar(calendar_frame, selectmode='day', 
                   year=datetime.now().year, 
                   month=datetime.now().month, 
                   day=datetime.now().day,
                   date_pattern='y-mm-dd')
    cal.pack(padx=10, pady=10)

    # Date confirmation button
    def confirm_date():
        selected_date = cal.get_date()
        date_display.configure(state="normal")
        date_display.delete(0, 'end')
        date_display.insert(0, selected_date)
        date_display.configure(state="readonly")

    confirm_date_button = CTkButton(master=frame, text="Confirm Date", command=confirm_date)
    confirm_date_button.grid(row=5, column=0, columnspan=2, pady=10)

    # Signup button
    def retrieve_input_sign():
        username = username_entry.get()
        password = password_entry.get()
        selected_date = date_display.get()
        
        if username == "" or password == "" or selected_date == "":
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return
        
        # Get the most recent patient ID and increment
        recent_id = id_collection.find_one()["patient_id"]
        filter = { 'patient_id': recent_id }
        recent_id += 1
        newvalues = { "$set": { 'patient_id': recent_id } }
        id_collection.update_one(filter, newvalues)

        # Create document for insertion
        document = {
            "user_id": recent_id,
            "name": username, 
            "password": password, 
            "date": selected_date,
            "user_type":"user"
        }
        
        # Insert document
        inserted_document = patient_collection.insert_one(document)
        
        # Print confirmation details
        print("============================")
        print("Inserted document ID:", inserted_document.inserted_id)
        print("user_id : ", recent_id)
        print("user_name : ", username)
        print("DOB : ", selected_date)
        print("============================")
        
        # Proceed to login screen
        login()

    signup_button = CTkButton(master=frame, text="Signup", command=retrieve_input_sign)
    signup_button.grid(row=6, column=0, columnspan=2, pady=20)

    # Back button
    back_button = CTkButton(master=frame, text="Back", command=login)
    back_button.grid(row=7, column=0, columnspan=2, pady=20)

def patient_home():
    clear_frame()  # Clear any existing content from the frame

    # Create a main content frame that will take the remaining space
    main_content_frame = CTkFrame(master=app, fg_color="#4a4e54")  # Set a background color for visibility
    main_content_frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0, anchor="nw")  # Fill remaining space

    # Initialize the main content area with the dashboard view
    show_dashboard(main_content_frame)

def show_dashboard(main_content_frame):
    clear_frame_content(main_content_frame)  # Clear main content area

    # Outer frame (Patient's Dashboard)
    main_label = CTkLabel(master=main_content_frame, text=f"Welcome {user_details['name'].capitalize()} ({user_details['user_id']})", font=("Arial", 24), text_color="white")
    main_label.pack(pady=20)  # Adds top padding

    # Inner dashboard frame (Dashboard) inside the main content frame
    dashboard_frame = CTkFrame(master=main_content_frame, border_color="#4a4e54", corner_radius=10, width=500, height=300)  # Predefined size for the inner dashboard
    dashboard_frame.pack(pady=10, padx=10, fill="both", expand=True)  

    sub_dashboard_frame = CTkFrame(master=dashboard_frame, border_color="white", corner_radius=10, width=400, height=200)
    sub_dashboard_frame.pack(pady=10, padx=10, fill="both", expand=True)  # Stretch to fill the remaining space with padding
    # Define padding between the buttons
    button_padding_x = 20
    button_padding_y = 10

    # Add buttons to the container and link to display content in the inner frame
    profile_button = CTkButton(master=sub_dashboard_frame, height=btn_height, width=btn_width, text="Profile", font=("Arial", 25),border_width=2,border_color="white",fg_color="transparent", command=lambda: show_patient_profile(main_content_frame))
    profile_button.grid(row=1, column=0, padx=button_padding_x, pady=button_padding_y)

    appointment_button = CTkButton(master=sub_dashboard_frame, text="Appointments", font=("Arial", 25),border_width=2,border_color="white",fg_color="transparent", height=btn_height, width=btn_width, command=lambda: show_appointments(main_content_frame))
    appointment_button.grid(row=1, column=1, padx=button_padding_x, pady=button_padding_y)

    records_button = CTkButton(master=sub_dashboard_frame, text="Records", font=("Arial", 25),border_width=2,border_color="white",fg_color="transparent",
    height=btn_height, width=btn_width, command=lambda: show_records(main_content_frame))
    records_button.grid(row=1, column=2, padx=button_padding_x, pady=button_padding_y)

    logout_button = CTkButton(master=sub_dashboard_frame, text="Logout", font=("Arial", 25),fg_color="red",text_color="white", hover_color="#963d36",
    height=btn_height, width=btn_width, command=lambda: (main_content_frame.destroy(), login()))
    logout_button.grid(row=1, column=3, padx=button_padding_x, pady=button_padding_y)

    # Set equal column weights for the buttons to ensure even spacing
    dashboard_frame.grid_columnconfigure((1, 2, 3, 4), weight=1)

def show_patient_profile(main_content_frame):
    """
    Display doctor profile page in a static view
    
    :param main_content_frame: Main frame to display the profile
    """
    # Clear existing content
    for widget in main_content_frame.winfo_children():
        widget.destroy()
    
    # Configure main content frame
    main_content_frame.configure(fg_color="transparent")
    
    # Scroll Frame for longer content
    scroll_frame = CTkScrollableFrame(
        master=main_content_frame, 
        width=500, 
        height=600,
        fg_color="transparent"
    )
    scroll_frame.pack(padx=20, pady=20, fill="both", expand=True)
    

    details_frame = CTkFrame(master=scroll_frame, fg_color="transparent")
    details_frame.pack(pady=20, padx=20, fill="x")
    
    # Profile Details Styling
    label_font = ("Arial", 16)
    value_font = ("Arial", 16, "bold")
    
    # Profile Detail Rows
    profile_details = [
        ("Name", user_details.get('name', 'N/A')),
        ("User ID", user_details.get('user_id', 'N/A')),
        ("DOB", user_details.get('date', 'N/A')),
        ("Email", user_details.get('email', 'N/A')),
        ("Phone no", user_details.get('phone', 'N/A')),
    ]
    
    # Display Profile Details
    for label, value in profile_details:
        detail_frame = CTkFrame(master=details_frame, fg_color="transparent")
        detail_frame.pack(fill="x", pady=5)
        
        CTkLabel(
            master=detail_frame, 
            text=f"{label}:", 
            font=label_font, 
            width=200,
            anchor="w"
        ).pack(side="left", padx=(0, 10))
        
        CTkLabel(
            master=detail_frame, 
            text=value, 
            font=value_font,
            anchor="w"
        ).pack(side="left", expand=True)
    
    # Back to Dashboard Button
    back_button = CTkButton(
        master=main_content_frame, 
        text="Back to Dashboard", 
        command=lambda: show_dashboard(main_content_frame)
    )
    back_button.pack(pady=20)



# Function to show the appointment dashboard
def show_appointments(main_content_frame):
    # Clear existing content
    clear_frame_content(main_content_frame)
    
    # Function to get and display appointments
    def display_appointments(frame):
        # Clear existing content in the frame, except headers
        for widget in frame.winfo_children():
            if widget.grid_info()['row'] != 0:  # Preserve headers
                widget.destroy()
        
        # Get appointment count
        appointment_count = appointment_collection.count_documents(filter={"user_id":user_id_apt})
        main_label.configure(text=f"My Appointments (Total: {appointment_count})")
        
        # Fetch appointments
        appointments = fetch_appointments(user_id_apt)
        
        if appointments:
            for row, appointment in enumerate(appointments, start=1):
                # Unpack appointment details
                doctor_name, date, department, appt_id = appointment
                
                # Display appointment details
                for col, detail in enumerate([doctor_name, date, department, appt_id]):
                    label = CTkLabel(
                        master=frame, 
                        text=str(detail), 
                        font=("Arial", 14)
                    )
                    label.grid(row=row, column=col, padx=10, pady=5, sticky="w")
                
                # Status label 
                status_label = CTkLabel(
                    master=frame, 
                    text="Scheduled", 
                    text_color="green", 
                    font=("Arial", 14)
                )
                status_label.grid(row=row, column=4, padx=10, pady=5, sticky="w")
        else:
            # No appointments message
            no_appts_label = CTkLabel(
                master=frame, 
                text="No appointments found.", 
                font=("Arial", 16),
                text_color="grey"
            )
            no_appts_label.grid(row=1, column=0, columnspan=5, padx=10, pady=20, sticky="w")
    
    # Main label with appointment count
    main_label = CTkLabel(
        master=main_content_frame, 
        text="My Appointments", 
        font=("Arial", 24), 
        text_color="white"
    )
    main_label.pack(pady=20)
    
    # Outer dashboard frame
    dashboard_frame = CTkFrame(
        master=main_content_frame, 
        border_color="#4a4e54", 
        corner_radius=10, 
        width=800, 
        height=500
    )
    dashboard_frame.pack(pady=10, padx=10, fill="both", expand=True)
    
    # Frame for action buttons
    action_frame = CTkFrame(
        master=dashboard_frame, 
        fg_color="transparent"
    )
    action_frame.pack(pady=10, padx=10, fill="x")
    
    # Book Appointment Button
    book_btn = CTkButton(
        master=action_frame, 
        text="Book New Appointment", 
        fg_color="green",
        hover_color="darkgreen",
        font=("Arial", 16),
        command=bookin_win
    )
    book_btn.pack(side="left", padx=10)
    
    # Cancel Appointment Button
    cancel_btn = CTkButton(
        master=action_frame, 
        text="Cancel Appointment", 
        fg_color="red",
        hover_color="#963d36",
        font=("Arial", 16),
        command=cancel_win
    )
    cancel_btn.pack(side="left", padx=10)
    
    # Scrollable frame for appointments
    appointments_frame = CTkScrollableFrame(
        master=dashboard_frame, 
        corner_radius=10, 
        width=750, 
        height=400
    )
    appointments_frame.pack(pady=10, padx=10, fill="both", expand=True)
    
    # Table headers
    headers = [
        "Doctor Name", 
        "Appointment Date", 
        "Department", 
        "Appointment ID", 
        "Status"
    ]
    
    # Create headers
    for col, header in enumerate(headers):
        header_label = CTkLabel(
            master=appointments_frame, 
            text=header, 
            font=("Arial", 16, "bold")
        )
        header_label.grid(row=0, column=col, padx=10, pady=10, sticky="w")
    
    # Refresh Button
    refresh_btn = CTkButton(
        master=action_frame, 
        text="🔄 Refresh", 
        fg_color="blue",
        hover_color="darkblue",
        font=("Arial", 16),
        command=lambda: display_appointments(appointments_frame)
    )
    refresh_btn.pack(side="left", padx=10)
    
    # Initial population of appointments
    display_appointments(appointments_frame)
    
    # Back to Dashboard Button
    back_button = CTkButton(
        master=main_content_frame, 
        text="Back to Dashboard", 
        font=("Arial", 16),
        command=lambda: show_dashboard(main_content_frame)
    )
    back_button.pack(pady=10)

def fetch_appointments(user_id):
    try:
        appointments = appointment_collection.find({"user_id": user_id})
        data = []
        for appointment in appointments:
            data.append((
                appointment.get("doctor_name", "N/A"),
                appointment.get("appointment_date", "N/A"),
                appointment.get("department", "N/A"),
                appointment.get("appointment_id", "N/A")
            ))

        if not data:
            print(f"No appointments found for username: {user_id}")
        return data

    except Exception as e:
        # Catch and log any errors
        print(f"Error fetching appointments for {user_id}: {e}")
        return []

def bookin_win():
    booking_window = CTkToplevel()
    booking_window.title("Book Appointment")
    booking_window.geometry("400x650")
    booking_window.grab_set()  # Make it a modal overlay

    # Patient Name
    name_label = CTkLabel(booking_window, text="Enter Patient Name:")
    name_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    name_entry = CTkEntry(booking_window, width=200)
    name_entry.grid(row=3, column=1, padx=10, pady=10)
    

    # Calendar Frame
    calendar_frame = CTkFrame(booking_window)
    calendar_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
    calendar = Calendar(
        calendar_frame, 
        selectmode='day', 
        date_pattern='yyyy-mm-dd',
        showweeknumbers=False
    )
    calendar.pack(padx=10, pady=10)

    # Appointment Date
    date_label = CTkLabel(booking_window, text="Selected Appointment Date:")
    date_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    date_entry = CTkEntry(booking_window, width=200, state="readonly")
    date_entry.grid(row=2, column=1, padx=10, pady=10)

    # Function to update date entry when a date is selected
    def select_date():
        selected_date = calendar.get_date()
        date_entry.configure(state='normal')
        date_entry.delete(0, 'end')
        date_entry.insert(0, selected_date)
        date_entry.configure(state='readonly')

    # Calendar Selection Button
    calendar_button = CTkButton(
        booking_window, 
        text="Select Date", 
        command=select_date
    )
    calendar_button.grid(row=1, column=1, padx=10, pady=10)

    # Department Selection
    dept_label = CTkLabel(booking_window, text="Select Department:")
    dept_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    dept_options = [dept["dept_name"] for dept in dept_collection.find()]
    dept_var = StringVar(value="Select Department")
    dept_menu = CTkOptionMenu(
        booking_window, 
        values=dept_options, 
        variable=dept_var
    )
    dept_menu.grid(row=4, column=1, padx=10, pady=10)

    # Check Availability Button
    def check_doctor_availability():
        selected_dept = dept_var.get()
        
        # Validate department selection
        if selected_dept == "Select Department":
            messagebox.showerror("Error", "Please select a department first.")
            return
        
        # Find doctors in the selected department
        available_doctors = [
            doc["doc_name"] for doc in doctor_collection.find({"department": selected_dept})
        ]
        
        # Update doctor dropdown
        if available_doctors:
            doctor_menu.configure(values=available_doctors)
            doctor_var.set(available_doctors[0])  # Set first doctor as default
            messagebox.showinfo("Doctors Available", 
                f"Found {len(available_doctors)} doctors in {selected_dept} department.")
        else:
            messagebox.showwarning("No Doctors", 
                f"No doctors found in {selected_dept} department.")

    check_availability_btn = CTkButton(
        booking_window, 
        text="Check Availability", 
        command=check_doctor_availability
    )
    check_availability_btn.grid(row=5, column=1, padx=10, pady=10)

    # Doctor Selection
    doctor_label = CTkLabel(booking_window, text="Select Doctor:")
    doctor_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
    doctor_var = StringVar(value="Select Doctor")
    doctor_menu = CTkOptionMenu(
        booking_window, 
        values=["Select Doctor"], 
        variable=doctor_var
    )
    doctor_menu.grid(row=6, column=1, padx=10, pady=10)

    # Slot Selection
    slot_label = CTkLabel(booking_window, text="Select Slot:")
    slot_label.grid(row=7, column=0, padx=10, pady=10, sticky="w")
    slot_options = [str(i) for i in range(1, 11)]
    slot_var = StringVar(value="Select Slot")
    slot_menu = CTkOptionMenu(
        booking_window, 
        values=slot_options, 
        variable=slot_var
    )
    slot_menu.grid(row=7, column=1, padx=10, pady=10)

    # Confirm Button
    def confirm_booking():
        patient_name = name_entry.get()
        appointment_date = date_entry.get()
        selected_dept = dept_var.get()
        selected_doctor = doctor_var.get()
        selected_slot = slot_var.get()
        result = patient_collection.find_one({"name": patient_name})
        appointment_id = id_collection.find_one()["appointment_id"]
        filter = { 'appointment_id': appointment_id }
        appointment_id+=1
        newvalues = { "$set": { 'appointment_id': appointment_id } }
        id_collection.update_one(filter, newvalues)

        if result:
            user_id = result["user_id"]  # Assign the found user_id
            print(f"User ID found: {user_id}")
        else:
            
            user_id = "not registered"
            print(f"No existing user found for user: {patient_name}")
        # Validation
        if (not patient_name or not appointment_date or 
            selected_dept == "Select Department" or 
            selected_doctor == "Select Doctor" or 
            selected_slot == "Select Slot"):
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        # Insert appointment into the database
        appointment_document = {
            "appointment_id":appointment_id,
            "user_id":user_id,
            "patient_name": patient_name,
            "appointment_date": appointment_date,
            "department": selected_dept,
            "doctor_name": selected_doctor,
            "slot_number": selected_slot,
        }
        appointment_collection.insert_one(appointment_document)
        messagebox.showinfo("Success", "Appointment booked successfully!")
        booking_window.destroy()


        

    # Confirm Button
    confirm_btn = CTkButton(
        booking_window, 
        text="Confirm Booking", 
        command=confirm_booking
    )
    confirm_btn.grid(row=8, column=1, padx=10, pady=10) 
# Close the overlay after checking
def cancel_win():
    # Create the cancellation window
    cancel_window = CTkToplevel()
    cancel_window.title("Cancel Appointment")
    cancel_window.geometry("400x500")
    cancel_window.grab_set()  # Make it a modal overlay

    # Fetch existing appointments for the current user
    existing_appointments = list(appointment_collection.find({"user_id": user_id_apt}))
    
    # Prepare appointment options for dropdown
    if not existing_appointments:
        messagebox.showinfo("No Appointments", "You have no current appointments to cancel.")
        cancel_window.destroy()
        return

    # Create appointment options (Appointment ID - Patient Name - Doctor - Date)
    appointment_options = [
        f"App ID: {app['appointment_id']} | {app['patient_name']} | {app['doctor_name']} | {app['appointment_date']}" 
        for app in existing_appointments
    ]

    # Appointment Selection
    appointment_label = CTkLabel(cancel_window, text="Select Appointment to Cancel:")
    appointment_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Dropdown for appointment selection
    appointment_var = StringVar(value="Select Appointment")
    appointment_dropdown = CTkOptionMenu(
        cancel_window, 
        values=["Select Appointment"] + appointment_options,
        variable=appointment_var,
        width=350
    )
    appointment_dropdown.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    # Confirmation Radio Button
    confirmation_var = StringVar(value="")
    confirmation_label = CTkLabel(cancel_window, text="Confirm Cancellation:")
    confirmation_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    confirm_radio = CTkRadioButton(
        cancel_window, 
        text="I want to cancel this appointment", 
        variable=confirmation_var, 
        value="confirmed"
    )
    confirm_radio.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # Confirm Cancellation Button
    def cancel_appointment():
        # Get selected appointment
        selected_appointment = appointment_var.get()
        confirmation = confirmation_var.get()

        # Validate selection
        if selected_appointment == "Select Appointment":
            messagebox.showerror("Error", "Please select an appointment to cancel.")
            return

        if confirmation != "confirmed":
            messagebox.showerror("Error", "Please confirm the cancellation.")
            return

        # Extract appointment ID from the selected option
        appointment_id = int(selected_appointment.split("App ID: ")[1].split(" |")[0])

        # Remove the appointment from the database
        result = appointment_collection.delete_one({"appointment_id": appointment_id})
        
        if result.deleted_count > 0:
            messagebox.showinfo("Success", "Appointment cancelled successfully!")
            cancel_window.destroy()
        else:
            messagebox.showerror("Error", "Failed to cancel the appointment.")

    # Confirm Cancel Button (initially disabled)
    confirm_cancel_btn = CTkButton(
        cancel_window, 
        text="Confirm Cancellation", 
        command=cancel_appointment,
        state="normal"  # You might want to implement dynamic enabling/disabling
    )
    confirm_cancel_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # Back Button
    back_btn = CTkButton(
        cancel_window, 
        text="Back", 
        command=cancel_window.destroy
    )
    back_btn.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
def show_records(main_content_frame):
    # Clear previous content
    for widget in main_content_frame.winfo_children():
        widget.destroy()
    
    # Configure main content frame
    main_content_frame.configure(fg_color="transparent")
    
    # Main label for Medical Records
    main_label = ctk.CTkLabel(
        master=main_content_frame, 
        text="My Medical Records", 
        font=("Arial", 24), 
        text_color="white"
    )
    main_label.pack(pady=20)
    
    # Outer dashboard frame
    dashboard_frame = ctk.CTkFrame(
        master=main_content_frame, 
        border_color="#4a4e54", 
        corner_radius=10, 
        width=800, 
        height=500
    )
    dashboard_frame.pack(pady=10, padx=10, fill="both", expand=True)
    
    # Scrollable frame for records
    records_frame = ctk.CTkScrollableFrame(
        master=dashboard_frame, 
        corner_radius=10, 
        width=750, 
        height=400
    )
    records_frame.pack(pady=10, padx=10, fill="both", expand=True)
    
    # Table headers
    headers = [
        "Patient Name", 
        "Doctor Name", 
        "Appointment Date", 
        "Action"
    ]
    
    # Create headers
    for col, header in enumerate(headers):
        header_label = ctk.CTkLabel(
            master=records_frame, 
            text=header, 
            font=("Arial", 16, "bold")
        )
        header_label.grid(row=0, column=col, padx=10, pady=10, sticky="w")
    
    # Function to open record details window
    def open_record_details(record):
        details_window = ctk.CTkToplevel()
        details_window.title("Record Details")
        details_window.geometry("400x500")
        
        # Create a frame for details
        details_frame = ctk.CTkFrame(master=details_window)
        details_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Safely convert record to dictionary
        record = dict(record) if not isinstance(record, dict) else record
        
        # Display record details
        details = [
            ("Appointment ID", record.get('appointment_id', 'N/A')),
            ("User ID", record.get('user_id', 'N/A')),
            ("Patient Name", record.get('patient_name', 'N/A')),
            ("Appointment Date", record.get('appointment_date', 'N/A')),
            ("Department", record.get('department', 'N/A')),
            ("Doctor Name", record.get('doctor_name', 'N/A'))
        ]
        
        for label, value in details:
            ctk.CTkLabel(
                master=details_frame, 
                text=f"{label}: {value}", 
                font=("Arial", 16)
            ).pack(pady=10)
        
        # Close button
        close_btn = ctk.CTkButton(
            master=details_frame, 
            text="Close", 
            command=details_window.destroy
        )
        close_btn.pack(pady=20)
    
    # Fetch records from MongoDB
    try:
        # Extract user_id from user_details (assuming it's a DataFrame or dictionary-like)
        user_id = user_details['user_id'] if isinstance(user_details, dict) else user_details.iloc[0]['user_id']
        
        # Find records for the specific user
        records = list(record_collection.find({'user_id': user_id}))
        
        # Check if records exist
        if not records:
            # Display message if no records found
            no_records_label = ctk.CTkLabel(
                master=records_frame, 
                text="No medical records found.", 
                font=("Arial", 16),
                text_color="gray"
            )
            no_records_label.grid(row=1, column=0, columnspan=4, padx=10, pady=20)
        else:
            # Populate records
            for row, record in enumerate(records, start=1):
                # Record details
                ctk.CTkLabel(
                    master=records_frame, 
                    text=str(record.get('patient_name', 'N/A'))
                ).grid(row=row, column=0, padx=10, pady=5, sticky='w')
                
                ctk.CTkLabel(
                    master=records_frame, 
                    text=str(record.get('doctor_name', 'N/A'))
                ).grid(row=row, column=1, padx=10, pady=5, sticky='w')
                
                ctk.CTkLabel(
                    master=records_frame, 
                    text=str(record.get('appointment_date', 'N/A'))
                ).grid(row=row, column=2, padx=10, pady=5, sticky='w')
                
                # View Details button
                view_btn = ctk.CTkButton(
                    master=records_frame, 
                    text="View Details", 
                    width=100,
                    command=lambda rec=record: open_record_details(rec)
                )
                view_btn.grid(row=row, column=3, padx=10, pady=5)
    
    except Exception as e:
        error_label = ctk.CTkLabel(
            master=records_frame, 
            text=f"Error fetching records: {str(e)}",
            text_color="red"
        )
        error_label.grid(row=1, column=0, columnspan=4, padx=10, pady=20)
    
    # Button frame for Back to Dashboard
    button_frame = ctk.CTkFrame(master=main_content_frame, fg_color="transparent")
    button_frame.pack(pady=10)
    
    # Back to Dashboard Button
    back_button = ctk.CTkButton(
        master=button_frame, 
        text="Back to Dashboard", 
        font=("Arial", 20),
        command=lambda: show_dashboard(main_content_frame)
    )
    back_button.pack(pady=10)

def doctor_home():
    clear_frame()  # Clear any existing content from the frame

    # Create a main content frame that will take the remaining space
    main_content_frame = CTkFrame(master=app, fg_color="#4a4e54")
    main_content_frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0, anchor="nw")

    # Initialize the main content area with the dashboard view
    show_doctor_dashboard(main_content_frame)

def show_doctor_dashboard(main_content_frame):
    clear_frame_content(main_content_frame)  # Clear main content area

    # Outer frame (Doctor's Dashboard)
    main_label = CTkLabel(master=main_content_frame, 
                           text=f"Welcome {doctor_details['doc_name'].capitalize()} ({doctor_details['doc_id']})", 
                           font=("Arial", 24), 
                           text_color="white")
    main_label.pack(pady=20)  # Adds top padding

    # Inner dashboard frame
    dashboard_frame = CTkFrame(master=main_content_frame, 
                                border_color="#4a4e54", 
                                corner_radius=10, 
                                width=500, 
                                height=300)
    dashboard_frame.pack(pady=10, padx=10, fill="both", expand=True)  

    sub_dashboard_frame = CTkFrame(master=dashboard_frame, 
                                   border_color="white", 
                                   corner_radius=10, 
                                   width=400, 
                                   height=200)
    sub_dashboard_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Define padding between the buttons
    button_padding_x = 20
    button_padding_y = 10

    # Doctor-specific buttons
    profile_button = CTkButton(master=sub_dashboard_frame, 
                                height=btn_height, 
                                width=btn_width, 
                                text="Profile", 
                                font=("Arial", 25),
                                border_width=2,
                                border_color="white",
                                fg_color="transparent", 
                                command=lambda: show_doctor_profile(main_content_frame))
    profile_button.grid(row=1, column=0, padx=button_padding_x, pady=button_padding_y)

    appointments_button = CTkButton(master=sub_dashboard_frame, 
                                    text="My Appointments", 
                                    font=("Arial", 25),
                                    border_width=2,
                                    border_color="white",
                                    fg_color="transparent", 
                                    height=btn_height, 
                                    width=btn_width, 
                                    command=lambda: show_doctor_appointments(main_content_frame))
    appointments_button.grid(row=1, column=1, padx=button_padding_x, pady=button_padding_y)

    logout_button = CTkButton(
        master=sub_dashboard_frame, 
        text="Logout", 
        font=("Arial", 25),
        fg_color="red",
        text_color="white", 
        hover_color="#963d36",
        height=btn_height, 
        width=btn_width, 
        command=lambda: (main_content_frame.destroy(), login())
    )
    logout_button.grid(row=1, column=2, padx=button_padding_x, pady=button_padding_y)
    # Set equal column weights for the buttons to ensure even spacing
    dashboard_frame.grid_columnconfigure((1, 2, 3, 4), weight=1)
def show_doctor_profile(main_content_frame):
    """
    Display doctor profile page in a static view
    
    :param main_content_frame: Main frame to display the profile
    """
    # Clear existing content
    for widget in main_content_frame.winfo_children():
        widget.destroy()
    
    # Configure main content frame
    main_content_frame.configure(fg_color="transparent")
    
    # Scroll Frame for longer content
    scroll_frame = CTkScrollableFrame(
        master=main_content_frame, 
        width=500, 
        height=600,
        fg_color="transparent"
    )
    scroll_frame.pack(padx=20, pady=20, fill="both", expand=True)
    

    details_frame = CTkFrame(master=scroll_frame, fg_color="transparent")
    details_frame.pack(pady=20, padx=20, fill="x")
    
    # Profile Details Styling
    label_font = ("Arial", 16)
    value_font = ("Arial", 16, "bold")
    
    # Profile Detail Rows
    profile_details = [
        ("Name", doctor_details.get('doc_name', 'N/A')),
        ("Doctor ID", doctor_details.get('doc_id', 'N/A')),
        ("specialization", doctor_details.get('specialization', 'N/A')),
        ("Department", doctor_details.get('department', 'N/A')),
        ("Phone Number", doctor_details.get('phone', 'N/A'))
    ]
    
    # Display Profile Details
    for label, value in profile_details:
        detail_frame = CTkFrame(master=details_frame, fg_color="transparent")
        detail_frame.pack(fill="x", pady=5)
        
        CTkLabel(
            master=detail_frame, 
            text=f"{label}:", 
            font=label_font, 
            width=200,
            anchor="w"
        ).pack(side="left", padx=(0, 10))
        
        CTkLabel(
            master=detail_frame, 
            text=value, 
            font=value_font,
            anchor="w"
        ).pack(side="left", expand=True)
    
    # Back to Dashboard Button
    back_button = CTkButton(
        master=main_content_frame, 
        text="Back to Dashboard", 
        command=lambda: show_doctor_dashboard(main_content_frame)
    )
    back_button.pack(pady=20)
def show_doctor_appointments(main_content_frame):
    # Clear previous content
    clear_frame_content(main_content_frame)
    
    # Get current doctor's name from user record
    doctor_name = doctor_details['doc_name']
    
    # Fetch appointments from MongoDB
    try:
        # Find appointments for the specific doctor
        appointments = appointment_collection.find({'doctor_name': doctor_name})
        appointment_list = list(appointments)
        total_appointments = len(appointment_list)
    except Exception as e:
        print(f"Error fetching appointments: {e}")
        total_appointments = 0
        appointment_list = []
    
    # Main label with doctor's name and appointment count
    main_label = CTkLabel(
        master=main_content_frame, 
        text=f"{doctor_name}'s Appointments (Total: {total_appointments})", 
        font=("Arial", 24), 
        text_color="white"
    )
    main_label.pack(pady=20)
    
    # Outer dashboard frame
    dashboard_frame = CTkFrame(
        master=main_content_frame, 
        border_color="#4a4e54", 
        corner_radius=10, 
        width=800, 
        height=500
    )
    dashboard_frame.pack(pady=10, padx=10, fill="both", expand=True)
    
    # Scrollable frame for appointments
    appointments_frame = CTkScrollableFrame(
        master=dashboard_frame, 
        corner_radius=10, 
        width=750, 
        height=400
    )
    appointments_frame.pack(pady=10, padx=10, fill="both", expand=True)
    
    # Table headers
    headers = [
        "Appointment No", 
        "Patient Name", 
        "Patient ID", 
        "slot_number",
        "Action"
    ]
    
    # Create headers
    for col, header in enumerate(headers):
        header_label = CTkLabel(
            master=appointments_frame, 
            text=header, 
            font=("Arial", 16, "bold")
        )
        header_label.grid(row=0, column=col, padx=10, pady=10, sticky="w")
    
    # Populate appointments
    for row, appointment in enumerate(appointment_list, start=1):
        # Appointment details
        CTkLabel(master=appointments_frame, text=str(appointment.get('appointment_id', 'N/A'))).grid(row=row, column=0, padx=10, pady=5)
        CTkLabel(master=appointments_frame, text=appointment.get('patient_name', 'N/A')).grid(row=row, column=1, padx=10, pady=5)
        CTkLabel(master=appointments_frame, text=appointment.get('user_id', 'N/A')).grid(row=row, column=2, padx=10, pady=5)
        CTkLabel(master=appointments_frame, text=appointment.get('slot_number', 'N/A')).grid(row=row, column=3, padx=10, pady=5)
        
        # Complete appointment button
        complete_btn = CTkButton(
            master=appointments_frame, 
            text="Complete", 
            fg_color="green", 
            hover_color="darkgreen",
            command=lambda appt_id=appointment['appointment_id']: complete_appointment(appt_id,main_content_frame)
        )
        complete_btn.grid(row=row, column=4, padx=10, pady=5)
    
    # Back button
    back_button = CTkButton(
        master=main_content_frame, 
        text="Back to Dashboard", 
        font=("Arial", 20),
        command=lambda: show_doctor_dashboard(main_content_frame)
    )
    back_button.pack(pady=10)

def complete_appointment(appointment_id,main_content_frame):
    try:
        # Remove the completed appointment from the database
        appointments = appointment_collection.find_one({'appointment_id': appointment_id})
        user_id=appointments['user_id']
        patient_name=appointments['patient_name']
        date=appointments['appointment_date']
        department=appointments['department']
        doctor_name=appointments['doctor_name']


        appointment_document = {
            "appointment_id":appointment_id,
            "user_id":user_id,
            "patient_name": patient_name,
            "appointment_date": date,
            "department": department,
            "doctor_name": doctor_name
        }
        record_collection.insert_one(appointment_document)
        show_doctor_appointments(main_content_frame)
        
        appointment_collection.delete_one({'appointment_id': appointment_id})
        # Optional: Show a confirmation message
        messagebox.showinfo(title="Appointment Completed", message="Appointment has been marked as completed.")
    except Exception as e:
        messagebox.showinfo(title="Error", message=f"Could not complete appointment: {e}", icon="cancel")

def admin_home():
    clear_frame()  # Clear any existing content from the frame

    # Create a main content frame that will take the remaining space
    main_content_frame = CTkFrame(master=app, fg_color="#4a4e54")
    main_content_frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0, anchor="nw")

    # Initialize the main content area with the dashboard view
    show_admin_dashboard(main_content_frame)

def show_admin_dashboard(main_content_frame):
    clear_frame_content(main_content_frame)  # Clear main content area

    # Outer frame (Admin's Dashboard)
    main_label = CTkLabel(master=main_content_frame, 
                           text=f"Welcome {admin_details['username'].capitalize()}", 
                           font=("Arial", 24), 
                           text_color="white")
    main_label.pack(pady=20)  # Adds top padding

    # Inner dashboard frame
    dashboard_frame = CTkFrame(master=main_content_frame, 
                                border_color="#4a4e54", 
                                corner_radius=10, 
                                width=500, 
                                height=300)
    dashboard_frame.pack(pady=10, padx=10, fill="both", expand=True)  

    sub_dashboard_frame = CTkFrame(master=dashboard_frame, 
                                   border_color="white", 
                                   corner_radius=10, 
                                   width=400, 
                                   height=200)
    sub_dashboard_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Define padding between the buttons
    button_padding_x = 25
    button_padding_y = 10

    # Admin-specific buttons
    manage_users_button = CTkButton(master=sub_dashboard_frame, 
                                    height=btn_height, 
                                    width=btn_width, 
                                    text="Manage Users", 
                                    font=("Arial", 25),
                                    border_width=2,
                                    border_color="white",
                                    fg_color="transparent", 
                                    command=lambda: show_manage_users(main_content_frame))
    manage_users_button.grid(row=1, column=0, padx=button_padding_x, pady=button_padding_y)

    manage_doctors_button = CTkButton(master=sub_dashboard_frame, 
                                      text="Manage Doctors", 
                                      font=("Arial", 25),
                                      border_width=2,
                                      border_color="white",
                                      fg_color="transparent", 
                                      height=btn_height, 
                                      width=btn_width, 
                                      command=lambda: view_doctors_list(main_content_frame))
    manage_doctors_button.grid(row=1, column=1, padx=button_padding_x, pady=button_padding_y)

    logout_button = CTkButton(master=sub_dashboard_frame, 
                              text="Logout", 
                              font=("Arial", 25),
                              fg_color="red",
                              text_color="white", 
                              hover_color="#963d36",
                              height=btn_height, 
                              width=btn_width, 
                              command=lambda: (main_content_frame.destroy(), login()))
    logout_button.grid(row=1, column=2, padx=button_padding_x, pady=button_padding_y)

    # Set equal column weights for the buttons to ensure even spacing
    dashboard_frame.grid_columnconfigure((1, 2, 3, 4, 5), weight=1)


def view_doctors_list(main_content_frame):
    # Clear previous content
    for widget in main_content_frame.winfo_children():
        widget.destroy()
    
    # Configure main content frame
    main_content_frame.configure(fg_color="transparent")
    
    # Main label for Doctors List
    main_label = ctk.CTkLabel(
        master=main_content_frame, 
        text="Doctors List", 
        font=("Arial", 24), 
        text_color="white"
    )
    main_label.pack(pady=20)
    
    # Outer dashboard frame
    dashboard_frame = ctk.CTkFrame(
        master=main_content_frame, 
        border_color="#4a4e54", 
        corner_radius=10, 
        width=800, 
        height=500
    )
    dashboard_frame.pack(pady=10, padx=10, fill="both", expand=True)
    
    # Scrollable frame for doctors
    doctors_frame = ctk.CTkScrollableFrame(
        master=dashboard_frame, 
        corner_radius=10, 
        width=750, 
        height=400
    )
    doctors_frame.pack(pady=10, padx=10, fill="both", expand=True)
    
    # Table headers
    headers = [
        "Doctor ID", 
        "Doctor Name", 
        "Department", 
        "Specialization", 
        "Email",
        "Action"
    ]
    
    # Create headers
    for col, header in enumerate(headers):
        header_label = ctk.CTkLabel(
            master=doctors_frame, 
            text=header, 
            font=("Arial", 16, "bold")
        )
        header_label.grid(row=0, column=col, padx=10, pady=10, sticky="w")
    
    # Fetch doctors from MongoDB
    try:
        # Fetch all doctors
        doctors = list(doctor_collection.find())
        
        # Populate doctors
        for row, doctor in enumerate(doctors, start=1):
            # Doctor details
            ctk.CTkLabel(master=doctors_frame, text=str(doctor.get('doc_id', 'N/A'))).grid(row=row, column=0, padx=10, pady=5)
            ctk.CTkLabel(master=doctors_frame, text=doctor.get('doc_name', 'N/A')).grid(row=row, column=1, padx=10, pady=5)
            ctk.CTkLabel(master=doctors_frame, text=doctor.get('department', 'N/A')).grid(row=row, column=2, padx=10, pady=5)
            ctk.CTkLabel(master=doctors_frame, text=doctor.get('specialization', 'N/A')).grid(row=row, column=3, padx=10, pady=5)
            ctk.CTkLabel(master=doctors_frame, text=doctor.get('email', 'N/A')).grid(row=row, column=4, padx=10, pady=5)
            
            # Edit and Delete buttons
            action_frame = ctk.CTkFrame(master=doctors_frame, fg_color="transparent")
            action_frame.grid(row=row, column=6, padx=10, pady=5)
            
            edit_btn = ctk.CTkButton(
                master=action_frame, 
                text="Edit", 
                width=60,
                command=lambda doc=doctor: open_edit_doctor_window(doc)
            )
            edit_btn.pack(side="left", padx=2)
            
            delete_btn = ctk.CTkButton(
                master=action_frame, 
                text="Delete", 
                width=60,
                fg_color="red", 
                hover_color="#963d36",
                command=lambda doc=doctor: confirm_delete_doctor(doc)
            )
            delete_btn.pack(side="left", padx=2)
    
    except Exception as e:
        ctk.CTkLabel(
            master=doctors_frame, 
            text=f"Error fetching doctors: {str(e)}",
            text_color="red"
        ).pack(pady=20)
    
    # Button frame
    button_frame = ctk.CTkFrame(master=main_content_frame, fg_color="transparent")
    button_frame.pack(pady=10)
    
    # Add Doctor Button
    add_doctor_button = ctk.CTkButton(
        master=button_frame, 
        text="Add Doctor", 
        font=("Arial", 20),
        command=lambda: open_add_doctor_window(main_content_frame)
    )
    add_doctor_button.pack(side="left", padx=10)
    
    # Back to Dashboard Button
    back_button = ctk.CTkButton(
        master=button_frame, 
        text="Back to Dashboard", 
        font=("Arial", 20),
        command=lambda: show_admin_dashboard(main_content_frame)
    )
    back_button.pack(side="left", padx=10)

def open_edit_doctor_window(doctor):
    # Create edit window
    edit_window = ctk.CTkToplevel()
    edit_window.title("Edit Doctor Details")
    edit_window.geometry("400x600")

    # Scrollable frame for edit
    scroll_frame = ctk.CTkScrollableFrame(
        master=edit_window, 
        width=350, 
        height=500,
        fg_color="transparent"
    )
    scroll_frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Create input fields
    def create_labeled_entry(master, label_text, default_value=''):
        detail_frame = ctk.CTkFrame(master=master, fg_color="transparent")
        detail_frame.pack(fill="x", pady=5)
        
        label = ctk.CTkLabel(
            master=detail_frame, 
            text=f"{label_text}:", 
            font=("Arial", 16),
            width=150,
            anchor="w"
        )
        label.pack(side="left", padx=(0, 10))
        
        entry = ctk.CTkEntry(
            master=detail_frame, 
            width=200,
            font=("Arial", 16)
        )
        entry.pack(side="left", expand=True, fill="x")
        entry.insert(0, str(default_value) if default_value is not None else '')
        
        return entry

    # Input fields
    doc_id_entry = create_labeled_entry(scroll_frame, "Doctor ID", doctor.get('doc_id', ''))
    doc_id_entry.configure(state='disabled')  # Make ID non-editable

    doc_name_entry = create_labeled_entry(scroll_frame, "Doctor Name", doctor.get('doc_name', ''))
    email_entry = create_labeled_entry(scroll_frame, "Email", doctor.get('email', ''))
    phone_entry = create_labeled_entry(scroll_frame, "Phone", doctor.get('phone', ''))
    
    # Department dropdown
    dept_frame = ctk.CTkFrame(master=scroll_frame, fg_color="transparent")
    dept_frame.pack(fill="x", pady=5)
    
    dept_label = ctk.CTkLabel(
        master=dept_frame, 
        text="Department:", 
        font=("Arial", 16),
        width=150,
        anchor="w"
    )
    dept_label.pack(side="left", padx=(0, 10))
    dept_options = [dept["dept_name"] for dept in dept_collection.find()]
    dept_dropdown = ctk.CTkOptionMenu(
        master=dept_frame, 
        values=dept_options,
        width=200,
        font=("Arial", 16)
    )
    dept_dropdown.pack(side="left", expand=True, fill="x")
    dept_dropdown.set(doctor.get('department', ''))

    specialization_entry = create_labeled_entry(scroll_frame, "Specialization", doctor.get('specialization', ''))
    
    # DOB Entry
    dob_entry = create_labeled_entry(scroll_frame, "Date of Birth", doctor.get('dob', ''))

    # Buttons frame
    buttons_frame = ctk.CTkFrame(master=scroll_frame, fg_color="transparent")
    buttons_frame.pack(pady=20)

    def update_doctor():
        try:
            # Prepare update data
            update_data = {
                'doc_name': doc_name_entry.get(),
                'email': email_entry.get(),
                'phone': phone_entry.get(),
                'department': dept_dropdown.get(),
                'specialization': specialization_entry.get(),
                'dob': dob_entry.get()
            }

            # Update in MongoDB
            doctor_collection.update_one(
                {'_id': doctor['_id']}, 
                {'$set': update_data}
            )

            messagebox.showinfo("Success", "Doctor details updated successfully")
            edit_window.destroy()
            
            
            # Refresh the doctors list if main_content_frame is available
            # You might need to pass main_content_frame from the calling function
            # view_doctors_list(main_content_frame)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update doctor: {str(e)}")

    update_button = ctk.CTkButton(
        master=buttons_frame, 
        text="Update", 
        font=("Arial", 16),
        command=update_doctor
    )
    update_button.pack(side="left", padx=10)

    cancel_button = ctk.CTkButton(
        master=buttons_frame, 
        text="Cancel", 
        font=("Arial", 16),
        fg_color="gray", 
        hover_color="darkgray",
        command=edit_window.destroy
    )
    cancel_button.pack(side="left", padx=10)

def confirm_delete_doctor(doctor):
    # Confirmation dialog
    confirm = messagebox.askyesno(
        "Confirm Delete", 
        "Are you sure you want to delete this doctor?\nThis action cannot be undone."
    )

    if confirm:
        try:
            # Delete from MongoDB
            result = doctor_collection.delete_one({'_id': doctor['_id']})
            
            if result.deleted_count > 0:
                messagebox.showinfo("Success", "Doctor deleted successfully")
                # Note: You might want to refresh the list here
                # view_doctors_list(main_content_frame)
            else:
                messagebox.showerror("Error", "Failed to delete doctor")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete doctor: {str(e)}")

def open_add_doctor_window(main_content_frame):
    # Create add doctor window
    add_window = ctk.CTkToplevel()
    add_window.title("Add New Doctor")
    add_window.geometry("400x600")

    # Scrollable frame for adding doctor
    scroll_frame = ctk.CTkScrollableFrame(
        master=add_window, 
        width=350, 
        height=500,
        fg_color="transparent"
    )
    scroll_frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Reusable function to create labeled entry (similar to edit window)
    def create_labeled_entry(master, label_text, default_value=''):
        detail_frame = ctk.CTkFrame(master=master, fg_color="transparent")
        detail_frame.pack(fill="x", pady=5)
        
        label = ctk.CTkLabel(
            master=detail_frame, 
            text=f"{label_text}:", 
            font=("Arial", 16),
            width=150,
            anchor="w"
        )
        label.pack(side="left", padx=(0, 10))
        
        entry = ctk.CTkEntry(
            master=detail_frame, 
            width=200,
            font=("Arial", 16)
        )
        entry.pack(side="left", expand=True, fill="x")
        entry.insert(0, str(default_value) if default_value is not None else '')
        
        return entry

    # Input fields
    recent_id = id_collection.find_one()
     
    doc_id_entry = create_labeled_entry(scroll_frame, "Doctor ID", recent_id.get('doc_id', ''))
    doc_id_entry.configure(state='disabled')
    doc_name_entry = create_labeled_entry(scroll_frame, "Doctor Name")
    email_entry = create_labeled_entry(scroll_frame, "Email")
    password_entry = create_labeled_entry(scroll_frame, "Password")
    phone_entry = create_labeled_entry(scroll_frame, "Phone")
    
    # Department dropdown
    dept_frame = ctk.CTkFrame(master=scroll_frame, fg_color="transparent")
    dept_frame.pack(fill="x", pady=5)
    
    dept_label = ctk.CTkLabel(
        master=dept_frame, 
        text="Department:", 
        font=("Arial", 16),
        width=150,
        anchor="w"
    )
    dept_label.pack(side="left", padx=(0, 10))
    dept_options = [dept["dept_name"] for dept in dept_collection.find()]
    dept_dropdown = ctk.CTkOptionMenu(
        master=dept_frame, 
        values=dept_options,
        width=200,
        font=("Arial", 16)
    )
    dept_dropdown.pack(side="left", expand=True, fill="x")

    specialization_entry = create_labeled_entry(scroll_frame, "Specialization")
    dob_entry = create_labeled_entry(scroll_frame, "Date of Birth (DD/MM/YYYY)")

    # Buttons frame
    buttons_frame = ctk.CTkFrame(master=scroll_frame, fg_color="transparent")
    buttons_frame.pack(pady=20)

    def save_new_doctor():
        try:
            recent_id = id_collection.find_one()["doc_id"]
            new_doctor_data = {
                'doc_id':recent_id,
                'doc_name': doc_name_entry.get(),
                'email': email_entry.get(),
                'email': email_entry.get(),
                'password': password_entry.get(),
                'phone': phone_entry.get(),
                'department': dept_dropdown.get(),
                'specialization': specialization_entry.get(),
                'dob': dob_entry.get(),
                'user_type':'doctor'
            }

            # Insert into MongoDB
            doctor_collection.insert_one(new_doctor_data)
            filter = { 'doc_id': recent_id }
            prefix = recent_id[0]  # Extract the prefix 'd'
            number = int(recent_id[1:])  # Convert the numeric part to an integer
            incremented_id = number + 1
            new_id = f"{prefix}{incremented_id}"
            newvalues = { "$set": { 'doc_id': new_id} }
            id_collection.update_one(filter, newvalues)

            messagebox.showinfo("Success", "New doctor added successfully")
            add_window.destroy()
            
            # Refresh the doctors list
            view_doctors_list(main_content_frame)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add doctor: {str(e)}")

    save_button = ctk.CTkButton(
        master=buttons_frame, 
        text="Save", 
        font=("Arial", 16),
        command=save_new_doctor
    )
    save_button.pack(side="left", padx=10)

    cancel_button = ctk.CTkButton(
        master=buttons_frame, 
        text="Back", 
        font=("Arial", 16),
        fg_color="gray", 
        hover_color="darkgray",
        command=add_window.destroy
    )
    cancel_button.pack(side="left", padx=10)



def show_manage_users(main_content_frame):
    # Clear previous content
    for widget in main_content_frame.winfo_children():
        widget.destroy()
    
    # Configure main content frame
    main_content_frame.configure(fg_color="transparent")
    
    # Main label for Doctors List
    main_label = ctk.CTkLabel(
        master=main_content_frame, 
        text="Patients List", 
        font=("Arial", 24), 
        text_color="white"
    )
    main_label.pack(pady=20)
    
    # Outer dashboard frame
    dashboard_frame = ctk.CTkFrame(
        master=main_content_frame, 
        border_color="#4a4e54", 
        corner_radius=10, 
        width=800, 
        height=500
    )
    dashboard_frame.pack(pady=10, padx=10, fill="both", expand=True)
    
    # Scrollable frame for doctors
    patients_frame = ctk.CTkScrollableFrame(
        master=dashboard_frame, 
        corner_radius=10, 
        width=750, 
        height=400
    )
    patients_frame.pack(pady=10, padx=10, fill="both", expand=True)
    
    # Table headers
    headers = [
        "Patient ID", 
        "Patient Name",  
        "Email",
        "Action"
    ]
    
    # Create headers
    for col, header in enumerate(headers):
        header_label = ctk.CTkLabel(
            master=patients_frame, 
            text=header, 
            font=("Arial", 16, "bold")
        )
        header_label.grid(row=0, column=col, padx=10, pady=10, sticky="w")
    
    # Fetch Patients from MongoDB
    try:
        # Fetch all Patients
        patients = list(patient_collection.find())
        
        # Populate doctors
        for row, patient in enumerate(patients, start=1):
            # Doctor details
            ctk.CTkLabel(master=patients_frame, text=str(patient.get('user_id', 'N/A'))).grid(row=row, column=0, padx=10, pady=5)
            ctk.CTkLabel(master=patients_frame, text=patient.get('name', 'N/A')).grid(row=row, column=1, padx=10, pady=5)
            ctk.CTkLabel(master=patients_frame, text=patient.get('email', 'N/A')).grid(row=row, column=2, padx=10, pady=5)
            
            # Edit and Delete buttons
            action_frame = ctk.CTkFrame(master=patients_frame, fg_color="transparent")
            action_frame.grid(row=row, column=6, padx=10, pady=5)
            
            edit_btn = ctk.CTkButton(
                master=action_frame, 
                text="Edit", 
                width=60,
                command=lambda pat=patient: open_edit_patient_window(pat)
            )
            edit_btn.pack(side="left", padx=2)
            
            delete_btn = ctk.CTkButton(
                master=action_frame, 
                text="Delete", 
                width=60,
                fg_color="red", 
                hover_color="#963d36",
                command=lambda pat=patient: confirm_delete_patient(pat)
            )
            delete_btn.pack(side="left", padx=2)
    
    except Exception as e:
        ctk.CTkLabel(
            master=patients_frame, 
            text=f"Error fetching patients: {str(e)}",
            text_color="red"
        ).pack(pady=20)
    
    # Button frame
    button_frame = ctk.CTkFrame(master=main_content_frame, fg_color="transparent")
    button_frame.pack(pady=10)
    
    # Add Doctor Button
    add_patient_button = ctk.CTkButton(
        master=button_frame, 
        text="Add Patient", 
        font=("Arial", 20),
        command=lambda: open_add_patient_window(main_content_frame)
    )
    add_patient_button.pack(side="left", padx=10)
    
    # Back to Dashboard Button
    back_button = ctk.CTkButton(
        master=button_frame, 
        text="Back to Dashboard", 
        font=("Arial", 20),
        command=lambda: show_admin_dashboard(main_content_frame)
    )
    back_button.pack(side="left", padx=10)

def open_edit_patient_window(patient):
    # Create edit window
    edit_window = ctk.CTkToplevel()
    edit_window.title("Edit Patient Details")
    edit_window.geometry("400x600")

    # Scrollable frame for edit
    scroll_frame = ctk.CTkScrollableFrame(
        master=edit_window, 
        width=350, 
        height=500,
        fg_color="transparent"
    )
    scroll_frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Create input fields
    def create_labeled_entry(master, label_text, default_value=''):
        detail_frame = ctk.CTkFrame(master=master, fg_color="transparent")
        detail_frame.pack(fill="x", pady=5)
        
        label = ctk.CTkLabel(
            master=detail_frame, 
            text=f"{label_text}:", 
            font=("Arial", 16),
            width=150,
            anchor="w"
        )
        label.pack(side="left", padx=(0, 10))
        
        entry = ctk.CTkEntry(
            master=detail_frame, 
            width=200,
            font=("Arial", 16)
        )
        entry.pack(side="left", expand=True, fill="x")
        entry.insert(0, str(default_value) if default_value is not None else '')
        
        return entry

    # Input fields
    patient_id_entry = create_labeled_entry(scroll_frame, "Patient ID", patient.get('user_id', ''))
    patient_id_entry.configure(state='disabled')  # Make ID non-editable

    patient_name_entry = create_labeled_entry(scroll_frame, "Patient Name", patient.get('name', ''))
    email_entry = create_labeled_entry(scroll_frame, "Email", patient.get('email', ''))
    phone_entry = create_labeled_entry(scroll_frame, "Phone", patient.get('phone', ''))
    dob_entry = create_labeled_entry(scroll_frame, "Date of Birth", patient.get('date', ''))

    # Buttons frame
    buttons_frame = ctk.CTkFrame(master=scroll_frame, fg_color="transparent")
    buttons_frame.pack(pady=20)

    def update_patient():
        try:
            # Prepare update data
            update_data = {
                'name': patient_name_entry.get(),
                'email': email_entry.get(),
                'phone': phone_entry.get(),
                'date': dob_entry.get()
            }

            # Update in MongoDB
            patient_collection.update_one(
                {'_id': patient['_id']}, 
                {'$set': update_data}
            )

            messagebox.showinfo("Success", "Patient details updated successfully")
            edit_window.destroy()
            
            
            # Refresh the doctors list if main_content_frame is available
            # You might need to pass main_content_frame from the calling function
            # view_doctors_list(main_content_frame)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update patient: {str(e)}")

    update_button = ctk.CTkButton(
        master=buttons_frame, 
        text="Update", 
        font=("Arial", 16),
        command=update_patient
    )
    update_button.pack(side="left", padx=10)

    cancel_button = ctk.CTkButton(
        master=buttons_frame, 
        text="Cancel", 
        font=("Arial", 16),
        fg_color="gray", 
        hover_color="darkgray",
        command=edit_window.destroy
    )
    cancel_button.pack(side="left", padx=10)

def confirm_delete_patient(patient):
    # Confirmation dialog
    confirm = messagebox.askyesno(
        "Confirm Delete", 
        "Are you sure you want to delete this patient?\nThis action cannot be undone."
    )

    if confirm:
        try:
            # Delete from MongoDB
            result = patient_collection.delete_one({'user_id': patient['user_id']})
            
            if result.deleted_count > 0:
                messagebox.showinfo("Success", "patient deleted successfully")
                # Note: You might want to refresh the list here
                # view_doctors_list(main_content_frame)
            else:
                messagebox.showerror("Error", "Failed to delete patient")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to patient doctor: {str(e)}")


def open_add_patient_window(main_content_frame):
    # Create add doctor window
    add_window = ctk.CTkToplevel()
    add_window.title("Add New Patient")
    add_window.geometry("400x600")

    # Scrollable frame for adding doctor
    scroll_frame = ctk.CTkScrollableFrame(
        master=add_window, 
        width=350, 
        height=500,
        fg_color="transparent"
    )
    scroll_frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Reusable function to create labeled entry (similar to edit window)
    def create_labeled_entry(master, label_text, default_value=''):
        detail_frame = ctk.CTkFrame(master=master, fg_color="transparent")
        detail_frame.pack(fill="x", pady=5)
        
        label = ctk.CTkLabel(
            master=detail_frame, 
            text=f"{label_text}:", 
            font=("Arial", 16),
            width=150,
            anchor="w"
        )
        label.pack(side="left", padx=(0, 10))
        
        entry = ctk.CTkEntry(
            master=detail_frame, 
            width=200,
            font=("Arial", 16)
        )
        entry.pack(side="left", expand=True, fill="x")
        entry.insert(0, str(default_value) if default_value is not None else '')
        
        return entry

    # Input fields

    recent_id = id_collection.find_one()
    patient_id_entry = create_labeled_entry(scroll_frame, "Patient ID", recent_id.get('patient_id', ''))
    patient_id_entry.configure(state='disabled')
    patient_name_entry = create_labeled_entry(scroll_frame, "Patient Name")
    email_entry = create_labeled_entry(scroll_frame, "Email")
    password_entry = create_labeled_entry(scroll_frame, "Password")
    phone_entry = create_labeled_entry(scroll_frame, "Phone")
    dob_entry = create_labeled_entry(scroll_frame, "Date of Birth (DD/MM/YYYY)")

    # Buttons frame
    buttons_frame = ctk.CTkFrame(master=scroll_frame, fg_color="transparent")
    buttons_frame.pack(pady=20)

    def save_new_patient():
        try:
            # Prepare new doctor data
            recent_id = id_collection.find_one()["patient_id"]
            new_patient_data = {
                'user_id':recent_id,
                'name': patient_name_entry.get(),
                'email': email_entry.get(),
                'password': password_entry.get(),
                'phone': phone_entry.get(),
                'date': dob_entry.get(),
                'user_type':"user"
            }

            # Insert into MongoDB
            patient_collection.insert_one(new_patient_data)
            filter = { 'patient_id': recent_id }
            recent_id+=1
            newvalues = { "$set": { 'patient_id': recent_id} }
            id_collection.update_one(filter, newvalues)


            messagebox.showinfo("Success", "New patient added successfully")
            add_window.destroy()
            
            # Refresh the doctors list
            show_manage_users(main_content_frame)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add patient: {str(e)}")

    save_button = ctk.CTkButton(
        master=buttons_frame, 
        text="Save", 
        font=("Arial", 16),
        command=save_new_patient
    )
    save_button.pack(side="left", padx=10)

    cancel_button = ctk.CTkButton(
        master=buttons_frame, 
        text="Back", 
        font=("Arial", 16),
        fg_color="gray", 
        hover_color="darkgray",
        command=add_window.destroy
    )
    cancel_button.pack(side="left", padx=10)



#====================================main app window=============================================== 
# Main app window
win = CTk()
win.geometry("800x600")
btn_frame = CTkFrame(win)
btn_frame.pack(pady=20)
# Helper function to clear main content frame
def clear_frame_content(frame):
    for widget in frame.winfo_children():
        widget.destroy()
# Initialize the main app window
app = CTk()
app.title("Hospital Management System")

# Automatically maximize the window
app.after(0, lambda: app.state('zoomed'))

set_appearance_mode("dark")

# Create a frame with increased width (600 pixels) and height
frame = CTkFrame(master=app, width=600, height=400)
frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame
login()

# Start the Tkinter main loop
app.mainloop()
