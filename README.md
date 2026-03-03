# Py-HRIS-System-with-SQL-Databases
mini HRIS System Connected with SQL databases

This project is an enhanced version of the previous implementation. Previously, the application was not integrated with an SQL database, meaning that all data updates were stored temporarily in memory (RAM). Consequently, any changes were lost once the terminal session was terminated. In this improved version, the system is fully integrated with an SQL database, allowing data to be stored persistently and ensuring reliability across sessions.

**Features**
1. Login & Role-Based Access (Super Admin & User)
2. Account Request & Approval System
3. Employee Management (CRUD)
4. Add Employee
5. View Employee
6. Update Employee
7. Delete Employee
8. Search Employee by NIP or Name
9. Duplicate NIP Validation
10. Persistent Data Storage using MySQL

**Tech Stack**
1. Python 3
2. MySQL
3. mysql-connector-python
4. Tabulate (for table display)

**Improvement From Previous Menu**

1. **Then :** Data Stored in RAM, **Now :** Data Stored in MySQL
2.  **Then :** Data lost after terminal closed, **Now :** Persistent storage
3.  **Then :** No database integration, **Now :** Full SQL integration
4.  **Then :** Basic structure, **Now :** Structured CRUD system


