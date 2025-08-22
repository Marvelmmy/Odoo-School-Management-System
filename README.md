# 📚 School Management System – Odoo 16

A modular **School Management System** built with **Odoo 16**, designed to handle teachers, students, classes, and invoicing.  
This project includes **database models, API endpoints, PDF reports, automation, and custom actions** for managing schools efficiently.

---

## ✨ Features

### 👨‍🏫 Teacher Management
- Store teacher info (name, address, phone number).
- Unique phone number validation (no duplicates allowed).
- Automatic calculation of total students taught.

### 🧑‍🎓 Student Management
- Add, edit, activate, and deactivate students.
- Linked to teachers and classes.

### 🏫 Class Management
- Relation between teacher, student, and class.
- Centralized structure for assignments.

### 🔌 API Integration (REST with Odoo API)
- `GET /api/guru` → Fetch teacher list (test via Postman).
- `GET /api/murid` → Fetch teacher list (test via Postman).
- `POST /api/murid/add` → Add a new student (test via Postman).

### 📝 Reports & Printouts
- PDF list of teachers with the students they teach.
- Invoice receipt (**kwitansi**) PDF – visible **only if invoice is Paid**.

### ⏰ Automation
- Monthly invoice scheduler for students.

---

## 📂 Project Structure
<img width="381" height="558" alt="image" src="https://github.com/user-attachments/assets/f4e2b51f-d9c8-48c7-b175-0475eb70a513" />


## ⚙️ Installation
git clone https://github.com/your-username/school-management-system.git

## 🚀 Usage
- Navigate to School Management module in Odoo
- Test APIs using Postman:
    GET /api/guru → Fetch teacher list
    GET /api/murid → Fetch teacher list
    POST /api/murid/add → Add a new student
- Generate reports
    Teacher-Student PDF List
    Invoice Receipt PDF (if invoice is Paid)
- Monthly invoices are generated automatically by the scheduler

## Example of Form View and PDF Printed Reports
  ### teachers form view
  <img width="1919" height="826" alt="image" src="https://github.com/user-attachments/assets/491858f5-84e2-415e-a112-ea53ad595d23" />
  
  ### students form view
  <img width="1917" height="818" alt="image" src="https://github.com/user-attachments/assets/c2dd7464-c1b5-4d69-8ab8-87cea3ba4638" />
  
  ### teacher student PDF report
  <img width="1185" height="648" alt="image" src="https://github.com/user-attachments/assets/3e4651df-9d56-4900-98b9-277fc93130b2" />
  
  ### PDF print invoice paid
  <img width="1108" height="722" alt="image" src="https://github.com/user-attachments/assets/45fa6ea7-898e-40e8-83f7-aeca9d2e1474" />


## 📌 Requirements
- Python 3.9 +
- Odoo 16
- Dependencies (install via pip) 

## 🤝 Contributing

Contributions are welcome! Please fork the repo and submit a pull request.
