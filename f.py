import sqlite3
import pandas as pd
from datetime import datetime

def setup_database():
    conn = sqlite3.connect("healthcare_dataset.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        glucose REAL,
        blood_pressure REAL,
        bmi REAL,
        outcome TEXT,
        date_added TEXT
    )
    """)
    conn.commit()
    conn.close()
    print("Healthcare dataset initialized successfully!")

def add_record():
    print("\nAdd New Patient Record")
    name = input("Enter patient name: ")
    age = int(input("Enter age: "))
    gender= input("Enter gender :M/F/O")
    glucose = float(input("Enter glucose level: "))
    bp = float(input("Enter blood pressure: "))
    bmi = float(input("Enter BMI: "))
    outcome_input = input("Outcome (D = Diabetic, N = Non-Diabetic): ").strip().upper()
    outcome = "Diabetic" if outcome_input == "D" else "Non-Diabetic"
    conn = sqlite3.connect("healthcare_dataset.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO records (name, age, gender,glucose, blood_pressure, bmi, outcome, date_added)
        VALUES (?, ?, ?, ?, ?, ?, ?,?)
    """, (name, age, gender,glucose, bp, bmi, outcome, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    print(f"Record for {name} added successfully!\n")

def view_records():
    conn = sqlite3.connect("healthcare_dataset.db")
    df = pd.read_sql_query("SELECT * FROM records ORDER BY id ASC", conn)
    conn.close()
    if df.empty:
        print("\nNo records found.\n")
    else:
        print("\n--- All Patient Records ---")
        print(df)
        print("\nTotal Records:", len(df), "\n")

def delete_record():
    print("""
Delete Record Options:
1. Delete by ID
2. Delete by Name
3. Delete ALL Records
""")
    choice = input("Enter your choice: ")
    conn = sqlite3.connect("healthcare_dataset.db")
    c = conn.cursor()

    if choice == '1':
        record_id = input("Enter record ID to delete: ")
        c.execute("DELETE FROM records WHERE id = ?", (record_id,))
    elif choice == '2':
        name = input("Enter patient name to delete: ")
        c.execute("DELETE FROM records WHERE name = ?", (name,))
    elif choice == '3':
        confirm = input("Are you sure you want to delete ALL records? (yes/no): ").strip().lower()
        if confirm == "yes":
            c.execute("DELETE FROM records")
            c.execute("DELETE FROM sqlite_sequence WHERE name='records'")
            print("All records have been deleted and ID counter reset!")
        else:
            print("Delete All operation cancelled.")
            conn.close()
            return
    else:
        print("Invalid option.")
        conn.close()
        return

    conn.commit()
    deleted = conn.total_changes
    conn.close()
    if choice in ['1', '2']:
        if deleted > 0:
            print("Record deleted successfully!\n")
        else:
            print("No matching record found.\n")

def filter_records():
    print("""
Filter Options:
1. Filter by Glucose
2. Filter by Age
3. Filter by BMI
4. Filter by Blood Pressure
5. Filter by Outcome (Diabetic / Non-Diabetic)
6. Filter Gender
7. Advanced Filter
""")
    choice = input("Enter filter type: ")
    conn = sqlite3.connect("healthcare_dataset.db")
    df = pd.read_sql_query("SELECT * FROM records", conn)
    conn = sqlite3.connect("healthcare_dataset.db")
    if choice == '1':
        val = float(input("Show patients with Glucose > "))
        query = "SELECT * FROM records WHERE glucose > ?"
    elif choice == '2':
        val = int(input("Show patients with Age > "))
        query = "SELECT * FROM records WHERE age > ?"
    elif choice == '3':
        val = float(input("Show patients with BMI > "))
        query = "SELECT * FROM records WHERE bmi > ?"
    elif choice == '4':
        val = float(input("Show patients with Blood Pressure > "))
        query = "SELECT * FROM records WHERE blood_pressure > ?"
    elif choice == '5':
        val = input("Show patients with Outcome = (Diabetic / Non-Diabetic): ").strip().capitalize()
        query = "SELECT * FROM records WHERE outcome like ?"
    elif choice == '6':
        val = input("Show patients with Gender (M/F/O): ").strip().upper()
        filtered = df[df['gender'].str.upper() == val]
    elif choice == '7':
        print("\nAdvanced Filter")
        gender = input("Enter Gender (M/F/O ): ").strip().upper()
        outcome = input("Enter Outcome (Diabetic/Non-Diabetic): ").strip().lower()
        min_age = input("Minimum Age: ").strip()
        min_glucose = input("Minimum Glucose Level: ").strip()
        min_bmi = input("Minimum BMI: ").strip()
        min_bp = input("Minimum Blood Pressure: ").strip()
        filtered =df.copy()
        if gender:
            filtered = filtered[filtered['gender'].str.upper() == gender]
        if outcome:
            filtered = filtered[filtered['outcome'].str.lower() == outcome]
        if min_age:
            filtered = filtered[filtered['age'] >= float(min_age)]
        if min_glucose:
            filtered = filtered[filtered['glucose'] >= float(min_glucose)]
        if min_bmi:
            filtered = filtered[filtered['bmi'] >= float(min_bmi)]
        if min_bp:
            filtered = filtered[filtered['blood_pressure'] >= float(min_bp)]
    else:
        print("Invalid choice!")
        return
    if filtered.empty:
        print("\nNo matching records found.\n")
    else:
        print("\n Filtered Records ")
        print(filtered.to_string(index=False))
        print()

def generate_report():
    conn = sqlite3.connect("healthcare_dataset.db")
    df = pd.read_sql_query("SELECT * FROM records", conn)
    conn.close()
    if df.empty:
        print("\nNo data to summarize.\n")
        return
    total = len(df)
    diabetic = len(df[df['outcome'] == 'Diabetic'])
    non_diabetic = len(df[df['outcome'] == 'Non-Diabetic'])
    avg_glucose = round(df['glucose'].mean(), 2)
    avg_bmi = round(df['bmi'].mean(), 2)
    avg_bp = round(df['blood_pressure'].mean(), 2)
    avg_age = round(df['age'].mean(), 1)
    print("\n--- Health Summary Report ---")
    print(f"Total Patients: {total}")
    print(f"Diabetic Patients: {diabetic}")
    print(f"Non-Diabetic Patients: {non_diabetic}")
    print(f"Average Glucose: {avg_glucose}")
    print(f"Average BMI: {avg_bmi}")
    print(f"Average Blood Pressure: {avg_bp}")
    print(f"Average Age: {avg_age}\n")

def main_menu():
    setup_database()
    while True:
        print("""
==============================
  HEALTHCARE DATASET TRACKER
==============================
1. Add New Patient Record
2. View All Records
3. Delete Records
4. Filter Records
5. Generate Summary Report
6. Exit
""")
        choice = input("Enter your choice: ")
        if choice == '1':
            add_record()
        elif choice == '2':
            view_records()
        elif choice == '3':
            delete_record()
        elif choice == '4':
            filter_records()
        elif choice == '5':
            generate_report()
        elif choice == '6':
            print("\nExiting Healthcare Tracker. Goodbye!\n")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main_menu()
