from datetime import datetime
from config import SUBJECTS,MAX_MARKS,MIN_MARKS,PASSING_MARKS
from grade_calculator import calculate_grade, get_result_status, calculate_percentage


def create_student(roll_no,name,student_class,marks):
    total,percentage = calculate_percentage(marks)

    return {
        "roll_no":roll_no.upper(),
        "name":name.title(),
        "class":student_class.upper(),
        "marks":marks,
        "total":total,
        "percentage":percentage,
        "grade":calculate_grade(percentage),
        "result":get_result_status(marks),
        "created_date":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def add_student(students):
    roll_no = input("Roll Number: ").strip().upper()

    if not roll_no:
        print("Roll number can not be empty.")
        return

    if any(s["roll_no"]==roll_no for s in students):
        print(f"Roll number {roll_no} already exists.")
        return

    name = input("Enter the name: ").strip()
    student_class = input("Class: ").strip()

    marks = {}
    print(f"Enter the marks({MIN_MARKS}-{MAX_MARKS}) for each subject: ")
    for subject in SUBJECTS:
        while True:
            try:
                value = int(input(f"{subject}: "))
                if MIN_MARKS<=value <= MAX_MARKS:
                    marks[subject] = value
                    break
                else:
                    print(f"Must be between {MIN_MARKS} and {MAX_MARKS}")
            except ValueError:
                print("Enter the valid number.")

    student = create_student(roll_no,name,student_class,marks)
    students.append(student)

    print(f"Added: {student['name']} | {student['percentage']} | {student['grade']} | {student['result']}")

def view_all_students(students):
    if not students:
        print("No student found")
        return
    print(f"{'Roll No':<10}{'Name':<25}{'Class':<8}{'Total':<8}{'%':<8}{'Result'}")
    print("-"*70)

    for s in students:
        print(f"{s['roll_no']:<10}{s['name']:<25}{s['class']:<8}{s['total']:<8}{s['percentage']:<8}{s['grade']:<7}{s['result']}")

    print(f"\nTotal: {len(students)} students")

def search_student(students):
    if not students:
        print("No student found.")
        return

    query = input("Search by roll number or name: ").strip().lower()
    results = [s for s in students if query in s['roll_no'].lower() or query in s['name'].lower()]

    if not results:
        print("No match found")

    for s in results:
        print(f"\n{s['roll_no']} | {s['name']} | {s['class']}")
        for subject,marks in s ['marks'].items():
            print(f"{subject}: {marks}")

        print(f"Total: {s['total']} | {s['percentage']}% | {s['grade']} | {s['result']}")

def update_student(students):
    roll_no = input("Enter roll number to update:  ").strip().upper()

    for student in students:
        if student['roll_no'] == roll_no:
            print(f"Updating marks for {student['name']}. Press enter to keep current value")
            for subject in SUBJECTS:
                new_input = input(f"{subject} (current: {student['marks'][subject]})").strip()
                if new_input:
                    try:
                        value = int(new_input)
                        if MIN_MARKS<=value<=MAX_MARKS:
                            student['marks'][subject] = value

                        else:
                            print("Invalid range, keeping old value")

                    except ValueError:
                        print("Invalid input, Keeping old value")
            total,percentage = calculate_percentage(student['marks'])
            student['total'] = total
            student['percentage'] = percentage
            student['grade'] = calculate_grade(percentage)
            student['result'] = get_result_status(student['marks'])
            print(f"updated: {student['percentage']}% | {student['grade']} | {student['result']}")

            return
    print(f"No student with roll no: '{roll_no}'")

def delete_student(students):
    roll_no = input("Roll number to delete: ").strip().upper()

    for i,student in enumerate(students):
        if student['roll_no'] == roll_no:
            confirm = input(f"Delete '{student['name']}' ? (Yes/No): ").strip().lower()

            if confirm == "yes":
                students.pop(i)
                print(f"Deleted {student['name']}")
                return
            else:
                print("Cancelled.")
                return

    print(f"No student with roll number: {roll_no}")