
# ============================================================
# GRADING MONITORING SYSTEM
# ============================================================

students = []

SUBJECTS = [
    "ITE 366",
    "ITE 260",
    "PED 30",
    "ETHIC",
    "MATH",
    "SSP",
    "PURPOSIVE"
]

TEACHER_PASSWORD = "admin"


# ============================================================
# GRADE CALCULATION
# ============================================================

def calculate_letter_grade(score):
    if score >= 90:
        return "A", 4.0
    elif score >= 80:
        return "B", 3.0
    elif score >= 70:
        return "C", 2.0
    elif score >= 60:
        return "D", 1.0
    else:
        return "F", 0.0


# ============================================================
# FIND STUDENT
# ============================================================

def find_student(student_id):
    for student in students:
        if student["id"] == student_id:
            return student
    return None


# ============================================================
# INPUT VALIDATION
# ============================================================

def get_valid_id(prompt):
    while True:
        student_id = input(prompt).strip()

        if student_id.isdigit():
            return student_id

        print("[ERROR] Student ID must contain numbers only.")


def get_valid_name(prompt):
    while True:
        name = input(prompt).strip()

        cleaned = name.replace(" ", "").replace(".", "").replace("-", "'")

        if name and cleaned.replace("'", "").isalpha():
            return name

        print("[ERROR] Enter a valid name using letters only.")


def get_choice(prompt, valid_options):
    while True:
        choice = input(prompt).strip()

        if choice in valid_options:
            return choice

        print(
            "[ERROR] Invalid choice. Choose: "
            + ", ".join(valid_options)
        )


# ============================================================
# REGISTER STUDENT
# ============================================================

def register_student(student_id, name):
    if find_student(student_id):
        print(
            f"\n[ERROR] Student ID {student_id} "
            "already exists. Registration blocked."
        )
        return False

    students.append({
        "id": student_id,
        "name": name,
        "grades": {}
    })

    print(
        f"\n[SUCCESS] Student {name} "
        f"(ID: {student_id}) registered."
    )
    return True


# ============================================================
# DISPLAY STUDENT LIST
# ============================================================

def display_student_list():
    if not students:
        print("\nNo students registered yet.")
        return

    print("\n" + "=" * 55)
    print("REGISTERED STUDENTS")
    print("=" * 55)
    print(f"{'NO.':<6}{'STUDENT ID':<15}{'STUDENT NAME'}")
    print("-" * 55)

    for number, student in enumerate(students, 1):
        print(
            f"{number:<6}"
            f"{student['id']:<15}"
            f"{student['name']}"
        )

    print("-" * 55)
    print(f"Total students: {len(students)}")


# ============================================================
# SELECT SUBJECT
# ============================================================

def select_subject():
    print("\n" + "=" * 45)
    print("AVAILABLE SUBJECTS")
    print("=" * 45)

    for number, subject in enumerate(SUBJECTS, 1):
        print(f"[{number}] {subject}")

    choice = get_choice(
        f"Select subject (1-{len(SUBJECTS)}): ",
        [str(i) for i in range(1, len(SUBJECTS) + 1)]
    )

    return SUBJECTS[int(choice) - 1]


# ============================================================
# RECORD / UPDATE GRADE
# ============================================================

def record_grade(student_id, subject, score):
    student = find_student(student_id)

    if student is None:
        print(f"\n[ERROR] Student ID {student_id} is not registered.")
        return False

    if subject not in SUBJECTS:
        print("\n[ERROR] Invalid subject.")
        return False

    if not 0 <= score <= 100:
        print("\n[ERROR] Score must be between 0 and 100.")
        return False

    letter, gpa = calculate_letter_grade(score)
    old_grade = student["grades"].get(subject)

    student["grades"][subject] = {
        "score": score,
        "letter": letter,
        "gpa": gpa
    }

    if old_grade:
        print(
            f"\n[SUCCESS] Grade updated for {student['name']}: "
            f"{subject} | {old_grade['score']:.1f} "
            f"-> {score:.1f}"
        )
    else:
        print(
            f"\n[SUCCESS] Grade recorded for {student['name']}: "
            f"{subject} | {score:.1f}"
        )

    print(f"Letter Grade: {letter}")
    print(f"GPA: {gpa:.1f}")

    return True


def enter_or_update_grade():
    if not students:
        print("\n[ERROR] Register a student first.")
        return

    display_student_list()
    student_id = get_valid_id("\nEnter Student ID: ")

    student = find_student(student_id)

    if student is None:
        print(f"\n[ERROR] Student ID {student_id} is not registered.")
        return

    print(f"\nSelected Student: {student['name']}")
    subject = select_subject()

    previous = student["grades"].get(subject)

    if previous:
        print(f"\nPrevious Score: {previous['score']:.1f}")
        print(f"Previous Grade: {previous['letter']}")
        print(f"Previous GPA: {previous['gpa']:.1f}")
    else:
        print("\nNo grade recorded for this subject yet.")

    while True:
        try:
            score = float(input("Enter Score (0-100): "))

            if 0 <= score <= 100:
                break

            print("[ERROR] Score must be between 0 and 100.")

        except ValueError:
            print("[ERROR] Please enter a valid numeric score.")

    record_grade(student_id, subject, score)


# ============================================================
# CALCULATE OVERALL GPA
# ============================================================

def calculate_overall_gpa(student):
    grades = student["grades"]

    if not grades:
        return None

    total_gpa = sum(data["gpa"] for data in grades.values())
    return total_gpa / len(grades)


# ============================================================
# VIEW INDIVIDUAL STUDENT REPORT
# ============================================================

def view_student_report(student_id):
    student = find_student(student_id)

    if student is None:
        print(f"\n[ERROR] Student ID {student_id} is not registered.")
        return

    print("\n" + "=" * 65)
    print("STUDENT GRADE REPORT")
    print("=" * 65)
    print(f"STUDENT ID   : {student['id']}")
    print(f"STUDENT NAME : {student['name']}")
    print("-" * 65)
    print(f"{'SUBJECT':<16}{'SCORE':<12}{'GRADE':<12}{'GPA':<10}")
    print("-" * 65)

    for subject in SUBJECTS:
        data = student["grades"].get(subject)

        if data:
            print(
                f"{subject:<16}"
                f"{data['score']:<12.1f}"
                f"{data['letter']:<12}"
                f"{data['gpa']:<10.1f}"
            )
        else:
            print(
                f"{subject:<16}"
                f"{'N/A':<12}"
                f"{'N/A':<12}"
                f"{'N/A':<10}"
            )

    print("-" * 65)

    overall_gpa = calculate_overall_gpa(student)

    print(
        f"SUBJECTS GRADED: "
        f"{len(student['grades'])}/{len(SUBJECTS)}"
    )

    if overall_gpa is not None:
        print(f"OVERALL GPA    : {overall_gpa:.2f}")
    else:
        print("OVERALL GPA    : N/A (No grades recorded)")

    print("=" * 65)


# ============================================================
# DISPLAY ALL STUDENTS SUMMARY
# ============================================================

def display_grade_report():
    # Display all students using the same subject/score/grade/GPA
    # layout as the individual Student Grade Report.
    print("\n" + "=" * 90)
    print("ALL STUDENTS GRADE SUMMARY")
    print("=" * 90)

    if not students:
        print("No student records available.")
        return

    for student in students:
        print(f"STUDENT ID   : {student['id']}")
        print(f"STUDENT NAME : {student['name']}")
        print("-" * 90)

        print(
            f"{'SUBJECT':<16}"
            f"{'SCORE':<12}"
            f"{'GRADE':<12}"
            f"{'GPA':<10}"
        )
        print("-" * 90)

        for subject in SUBJECTS:
            data = student["grades"].get(subject)

            if data:
                score_text = f"{data['score']:.1f}"
                grade_text = data["letter"]
                gpa_text = f"{data['gpa']:.1f}"
            else:
                score_text = "N/A"
                grade_text = "N/A"
                gpa_text = "N/A"

            print(
                f"{subject:<16}"
                f"{score_text:<12}"
                f"{grade_text:<12}"
                f"{gpa_text:<10}"
            )

        print("-" * 90)

        overall_gpa = calculate_overall_gpa(student)

        if overall_gpa is not None:
            print(f"SUBJECTS GRADED: {len(student['grades'])}/{len(SUBJECTS)}")
            print(f"OVERALL GPA    : {overall_gpa:.2f}")
        else:
            print(f"SUBJECTS GRADED: 0/{len(SUBJECTS)}")
            print("OVERALL GPA    : N/A (No grades recorded)")

        print("=" * 90)


# ============================================================
# DELETE STUDENT
# ============================================================

def delete_student():
    if not students:
        print("\n[ERROR] No students registered yet.")
        return

    display_student_list()
    student_id = get_valid_id("\nEnter Student ID to delete: ")

    student = find_student(student_id)

    if student is None:
        print(f"\n[ERROR] Student ID {student_id} not found.")
        return

    confirm = input(
        f"Delete {student['name']} (ID: {student_id})? (y/n): "
    ).strip().lower()

    if confirm == "y":
        students.remove(student)
        print(f"\n[SUCCESS] Student {student['name']} deleted.")
    else:
        print("\nDeletion canceled.")


# ============================================================
# TEACHER MENU
# ============================================================

def teacher_menu():
    while True:
        print("\n" + "=" * 50)
        print(" TEACHER MENU")
        print("=" * 50)
        print("[1] Register Student")
        print("[2] Record / Update Grade")
        print("[3] View Student Grade Report")
        print("[4] Display All Students Summary")
        print("[5] Delete Student")
        print("[6] Back to Main Menu")
        print("=" * 50)

        choice = get_choice(
            "Select an option [1-6]: ",
            ["1", "2", "3", "4", "5", "6"]
        )

        if choice == "1":
            # Keep asking for Student ID until a new ID is entered.
            while True:
                student_id = get_valid_id("Enter Student ID: ")

                if find_student(student_id):
                    print(
                        f"\n[ERROR] Student ID {student_id} "
                        "already exists. Registration blocked."
                    )
                    print("[INFO] Please enter a different Student ID.\n")
                    continue

                # Only ask for the name after a unique Student ID is entered.
                name = get_valid_name("Enter Student Name: ")
                register_student(student_id, name)
                break

        elif choice == "2":
            enter_or_update_grade()

        elif choice == "3":
            student_id = get_valid_id("Enter Student ID: ")
            view_student_report(student_id)

        elif choice == "4":
            display_grade_report()

        elif choice == "5":
            delete_student()

        elif choice == "6":
            return


# ============================================================
# STUDENT MENU
# ============================================================

def student_menu():
    print("\n" + "=" * 50)
    print(" STUDENT PORTAL")
    print("=" * 50)

    student_id = get_valid_id("Enter your Student ID: ")
    view_student_report(student_id)


# ============================================================
# MAIN MENU
# ============================================================

def main():
    while True:
        print("\n" + "=" * 50)
        print(" STUDENT GRADE MANAGEMENT SYSTEM")
        print("=" * 50)
        print("[1] Teacher")
        print("[2] Student")
        print("[3] Exit")
        print("=" * 50)

        choice = get_choice(
            "Select an option [1-3]: ",
            ["1", "2", "3"]
        )

        if choice == "1":
            # Teacher login
            # input() is used instead of getpass() so it works correctly in OnlineGDB.
            while True:
                print()
                password = input("Enter Teacher Password: ").strip()

                if password == TEACHER_PASSWORD:
                    print("\n[SUCCESS] Teacher login successful.")
                    teacher_menu()
                    break

                print("\n[ERROR] Incorrect password.")
                print("[INFO] Please enter the password again.")

        elif choice == "2":
            student_menu()

        elif choice == "3":
            print(
                "\nThank you for using the "
                "Student Grade Management System. Goodbye!"
            )
            break


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()