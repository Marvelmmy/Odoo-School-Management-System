📚 School Management System – Odoo 16

A modular School Management System built with Odoo 16, designed to handle teachers, students, classes, and invoicing.
This project includes database models, API endpoints, PDF reports, automation, and custom actions for managing schools efficiently.

✨ Features

👨‍🏫 Teacher Management

Store teacher info (name, address, phone number).

Unique phone number validation (no duplicates).

Automatic calculation of total students taught.

🧑‍🎓 Student Management

Add, edit, activate, and deactivate students.

Linked to teachers and classes.

🏫 Class Management

Relation between teacher, student, and class.

Centralized structure for assignments.

🔌 API Integration (REST with Odoo API)

Get teacher list (via Postman test).

Add new students (via Postman test).

📝 Reports & Printouts

PDF list of teachers with students they teach.

Invoice receipt (kwitansi) PDF – visible only if invoice is Paid.

⏰ Automation

Monthly invoice scheduler for students.

📂 Project Structure
school_management/
│── models/
│   ├── teacher.py
│   ├── student.py
│   ├── class.py
│── views/
│   ├── teacher_views.xml
│   ├── student_views.xml
│   ├── class_views.xml
│── reports/
│   ├── teacher_student_report.xml
│   ├── invoice_receipt_template.xml
│── controllers/
│   ├── api.py
│── data/
│   ├── scheduler.xml
│── __manifest__.py

⚙️ Installation

Clone this repository into your Odoo addons folder:

git clone https://github.com/your-username/school-management-system.git


Restart your Odoo server:

./odoo-bin -c odoo.conf -d your_database -u school_management


Activate the module in Odoo Apps.

🚀 Usage

Navigate to School Management module in Odoo.

Add teachers and students through the form view.

Test APIs using Postman:

GET /api/teachers → Fetch teacher list.

POST /api/students → Add a new student.

Generate reports:

Teacher-Student PDF List.

Invoice Receipt PDF (if invoice is Paid).

Monthly invoices are generated automatically by the scheduler.

📸 Screenshots

(Add your screenshots here, for example)

Teacher Form View

Student Form View

Teacher-Student PDF Report

Invoice Receipt (Paid Status)

📌 Requirements

Python 3.9+

Odoo 16

Dependencies (install via pip):

pip install -r requirements.txt

🤝 Contributing

Contributions are welcome! Please fork the repo and submit a pull request.
