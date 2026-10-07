import sqlite3
import sys

# Database Initialization & Configuration

DB_NAME = "student_management.db"

def init_db():
    """Initializes the SQLite database and creates the students table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            matric_no TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            department TEXT NOT NULL,
            cgpa REAL NOT NULL CHECK(cgpa >= 0.0 AND cgpa <= 5.0)
        )
    ''')
    conn.commit()
    conn.close()

# Core CRUD Operations

def add_student(matric_no, name, dept, cgpa):
    """Inserts a new student record into the database."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO students (matric_no, full_name, department, cgpa)
            VALUES (?, ?, ?, ?)
        ''', (matric_no, name, dept, cgpa))
        conn.commit()
        print(f"\n[SUCCESS] Student record for '{name}' added successfully!")
    except sqlite3.IntegrityError:
        print(f"\n[ERROR] Matric number '{matric_no}' already exists in the system.")
    finally:
        conn.close()

def view_all_students():
    """Retrieves and displays all student records."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    records = cursor.fetchall()
    conn.close()

    if not records:
        print("\n[INFO] No student records found.")
        return

    print("\n" + "="*60)
    print(f"{'MATRIC NO':<15} | {'FULL NAME':<20} | {'DEPT':<10} | {'CGPA':<5}")
    print("="*60)
    for row in records:
        print(f"{row[0]:<15} | {row[1]:<20} | {row[2]:<10} | {row[3]:<5.2f}")
    print("="*60)

def search_student(matric_no):
    """Searches for a specific student by Matric Number."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE matric_no = ?', (matric_no,))
    record = cursor.fetchone()
    conn.close()

    if record:
        print("\n[RESULT FOUND]")
        print(f"Matric No : {record[0]}")
        print(f"Name      : {record[1]}")
        print(f"Department: {record[2]}")
        print(f"CGPA      : {record[3]:.2f}")
    else:
        print(f"\n[INFO] No record found matching Matric No: '{matric_no}'.")

def delete_student(matric_no):
    """Deletes a student record by Matric Number."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE matric_no = ?', (matric_no,))
    if cursor.rowcount > 0:
        conn.commit()
        print(f"\n[SUCCESS] Record for '{matric_no}' deleted successfully.")
    else:
        print(f"\n[INFO] No record found with Matric No: '{matric_no}'.")
    conn.close()

# CLI Menu Interface

def main():
    init_db()
    while True:
        print("\n--- STUDENT RECORDS MANAGEMENT SYSTEM ---")
        print("1. Add New Student")
        print("2. View All Students")
        print("3. Search Student by Matric No")
        print("4. Delete Student Record")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ").strip()

        if choice == '1':
            matric = input("Enter Matric No: ").strip().upper()
            name = input("Enter Full Name: ").strip()
            dept = input("Enter Department: ").strip()
            try:
                cgpa = float(input("Enter CGPA (0.0 - 5.0): "))
                if 0.0 <= cgpa <= 5.0:
                    add_student(matric, name, dept, cgpa)
                else:
                    print("\n[ERROR] CGPA must be between 0.0 and 5.0.")
            except ValueError:
                print("\n[ERROR] Invalid CGPA input. Please enter a decimal number.")

        elif choice == '2':
            view_all_students()

        elif choice == '3':
            matric = input("Enter Matric No to Search: ").strip().upper()
            search_student(matric)

        elif choice == '4':
            matric = input("Enter Matric No to Delete: ").strip().upper()
            delete_student(matric)

        elif choice == '5':
            print("\nExiting system. Goodbye!")
            sys.exit()

        else:
            print("\n[ERROR] Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()