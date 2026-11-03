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
