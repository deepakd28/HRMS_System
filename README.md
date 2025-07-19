# Hospital Management System (CustomTkinter & MongoDB)

This repository contains a desktop application built with **Python's CustomTkinter** for the graphical user interface and **PyMongo** for seamless interaction with a MongoDB database. The system is designed to streamline various operations within a hospital environment, providing distinct functionalities for **patients, doctors, and administrators**.

## ✨ Features

* **User Authentication**: Secure login system for three user roles:
    * **Patient**: Access personal profile, view and book/cancel appointments, and review medical records.
    * **Doctor**: View their appointment schedule, manage patient records by marking appointments as complete.
    * **Admin**: Manage patient records (add, edit, delete) and doctor records (add, edit, delete).
* **Patient Management**:
    * **Signup**: New patients can register with a username, password, and date of birth.
    * **Profile View**: Patients can view their registered details.
    * **Appointment Booking**: Patients can book new appointments by selecting date, department, doctor, and slot.
    * **Appointment Cancellation**: Patients can view and cancel their existing appointments.
    * **Medical Records**: Patients can view their past medical records.
* **Doctor Management**:
    * **Profile View**: Doctors can view their personal and professional details.
    * **Appointments List**: Doctors can see a list of their scheduled appointments.
    * **Appointment Completion**: Doctors can mark appointments as complete, which moves the appointment details to medical records.
* **Admin Dashboard**:
    * **Manage Patients**: Add new patients, edit existing patient details (name, email, phone, DOB), and delete patient records.
    * **Manage Doctors**: Add new doctors, edit existing doctor details (name, email, phone, department, specialization, DOB), and delete doctor records.
* **Database Integration**: Utilizes MongoDB for robust and scalable data storage for patient, doctor, appointment, department, admin, and medical record collections.
* **User-Friendly Interface**: Built with CustomTkinter for a modern, customizable, and responsive GUI.
* **Date Selection**: Integrated `tkcalendar` for easy date picking during signup and appointment booking.

## 💻 Technologies Used

* **Python 3.x**
* **CustomTkinter**: For creating modern-looking Tkinter GUIs.
* **Pymongo**: Python driver for MongoDB.
* **Tkcalendar**: For date selection widgets.
* **MongoDB**: NoSQL database for data storage.

## 🛠️ Installation & Setup

### 1. Prerequisites

* **Python 3.x**: Make sure you have Python installed on your system.
    [Download Python](https://www.python.org/downloads/)
* **MongoDB**: You'll need a running MongoDB instance. You can:
    * Install MongoDB Community Server locally: [MongoDB Installation Guide](https://docs.mongodb.com/manual/installation/)
    * Use MongoDB Atlas (cloud-based): [MongoDB Atlas](https://www.mongodb.com/atlas)

### 2. Clone the Repository

```bash
git clone https://github.com/deepakd28/HRMS_System.git
cd HRMS_System
