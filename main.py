
import tkinter as tk
from tkinter import messagebox, ttk

from charts import show_charts
from database import (
    save_student,
    search_student,
    delete_student,
    get_all_students
)

# ================= MAIN WINDOW =================

root = tk.Tk()
root.title("Smart Student Performance Analyzer")
root.geometry("1000x850")
root.configure(bg="#1e1e2f")
root.resizable(False, False)

BG = "#1e1e2f"
CARD = "#2b2b40"
ACCENT = "#6c63ff"
WHITE = "#ffffff"

subjects = ["Python", "Web Development", "DSA", "Calculus"]


# ================= HEADING =================

tk.Label(
    root,
    text="SMART STUDENT PERFORMANCE ANALYZER",
    font=("Arial", 22, "bold"),
    bg=BG,
    fg=WHITE
).pack(pady=(15, 5))

tk.Label(
    root,
    text="Analyze your academic performance and improve yourself!",
    font=("Arial", 11),
    bg=BG,
    fg="#c5c5d6"
).pack(pady=(0, 10))


# ================= STUDENT DETAILS =================

form_frame = tk.Frame(root, bg=BG)
form_frame.pack(pady=5)

details_frame = tk.LabelFrame(
    form_frame,
    text="Student Details",
    font=("Arial", 13, "bold"),
    bg=CARD,
    fg=WHITE,
    padx=20,
    pady=12
)

details_frame.grid(row=0, column=0, padx=12, sticky="n")

tk.Label(
    details_frame,
    text="Student Name",
    bg=CARD,
    fg=WHITE
).grid(row=0, column=0, sticky="w", pady=6)

name_entry = tk.Entry(details_frame, width=27, font=("Arial", 11))
name_entry.grid(row=1, column=0, pady=5)

tk.Label(
    details_frame,
    text="Enrollment Number",
    bg=CARD,
    fg=WHITE
).grid(row=2, column=0, sticky="w", pady=6)

enroll_entry = tk.Entry(details_frame, width=27, font=("Arial", 11))
enroll_entry.grid(row=3, column=0, pady=5)


# ================= SUBJECT MARKS =================

marks_frame = tk.LabelFrame(
    form_frame,
    text="Subject Marks (Out of 100)",
    font=("Arial", 13, "bold"),
    bg=CARD,
    fg=WHITE,
    padx=20,
    pady=12
)

marks_frame.grid(row=0, column=1, padx=12, sticky="n")

mark_entries = {}

for i, subject in enumerate(subjects):

    tk.Label(
        marks_frame,
        text=subject,
        bg=CARD,
        fg=WHITE
    ).grid(row=i, column=0, sticky="w", pady=8)

    entry = tk.Entry(marks_frame, width=20, font=("Arial", 11))
    entry.grid(row=i, column=1, padx=10, pady=6)

    mark_entries[subject] = entry


# ================= STUDY HABITS =================

habits_frame = tk.LabelFrame(
    root,
    text="Study Habits",
    font=("Arial", 13, "bold"),
    bg=CARD,
    fg=WHITE,
    padx=25,
    pady=10
)

habits_frame.pack(pady=10)

tk.Label(
    habits_frame,
    text="Attendance (%)",
    bg=CARD,
    fg=WHITE
).grid(row=0, column=0, padx=15, pady=7)

attendance_entry = tk.Entry(habits_frame, width=18, font=("Arial", 11))
attendance_entry.grid(row=0, column=1, padx=15)

tk.Label(
    habits_frame,
    text="Daily Study Hours",
    bg=CARD,
    fg=WHITE
).grid(row=1, column=0, padx=15, pady=7)

study_entry = tk.Entry(habits_frame, width=18, font=("Arial", 11))
study_entry.grid(row=1, column=1, padx=15)

tk.Label(
    habits_frame,
    text="Daily Sleep Hours",
    bg=CARD,
    fg=WHITE
).grid(row=2, column=0, padx=15, pady=7)

sleep_entry = tk.Entry(habits_frame, width=18, font=("Arial", 11))
sleep_entry.grid(row=2, column=1, padx=15)


# ================= RESULT SECTION =================

result_frame = tk.LabelFrame(
    root,
    text="Performance Analysis",
    font=("Arial", 13, "bold"),
    bg=CARD,
    fg=WHITE,
    padx=12,
    pady=8
)

result_box = tk.Text(
    result_frame,
    font=("Consolas", 10),
    bg="#252538",
    fg=WHITE,
    relief="flat",
    padx=15,
    pady=10,
    wrap="word"
)

result_box.pack(fill="both", expand=True)
result_box.config(state="disabled")


# ================= COLLECT INPUT DATA =================

def collect_data():

    name = name_entry.get().strip()
    enrollment = enroll_entry.get().strip()

    if not name or not enrollment:
        raise ValueError("Enter student name and enrollment number.")

    data = {
        "name": name,
        "enrollment": enrollment
    }

    for subject, entry in mark_entries.items():

        value = float(entry.get())

        if not 0 <= value <= 100:
            raise ValueError(
                f"{subject} marks must be between 0 and 100."
            )

        data[subject] = value

    data["attendance"] = float(attendance_entry.get())
    data["study_hours"] = float(study_entry.get())
    data["sleep_hours"] = float(sleep_entry.get())

    if not 0 <= data["attendance"] <= 100:
        raise ValueError("Attendance must be between 0 and 100.")

    if not 0 <= data["study_hours"] <= 24:
        raise ValueError("Study hours must be between 0 and 24.")

    if not 0 <= data["sleep_hours"] <= 24:
        raise ValueError("Sleep hours must be between 0 and 24.")

    return data


# ================= PERFORMANCE ANALYSIS =================

def display_report(data, display_graphs=False):

    marks = {
        subject: data[subject]
        for subject in subjects
    }

    total = sum(marks.values())
    percentage = total / len(subjects)

    if percentage >= 85:
        performance = "Excellent"
    elif percentage >= 70:
        performance = "Good"
    elif percentage >= 50:
        performance = "Average"
    else:
        performance = "Needs Improvement"

    recommendations = []

    weakest_subject = min(marks, key=marks.get)

    if marks[weakest_subject] < 70:
        recommendations.append(
            f"Focus more on {weakest_subject}."
        )

    if data["attendance"] < 75:
        recommendations.append("Improve your attendance.")

    if data["study_hours"] < 2:
        recommendations.append("Increase your daily study hours.")

    if data["sleep_hours"] < 7:
        recommendations.append("Try to maintain 7-9 hours of sleep.")

    if not recommendations:
        recommendations.append(
            "Great work! Maintain your current routine."
        )

    report = f"""
STUDENT PERFORMANCE REPORT

========================================

Name: {data['name']}
Enrollment: {data['enrollment']}

SUBJECT-WISE MARKS

----------------------------------------
"""

    for subject, value in marks.items():
        report += f"\n{subject}: {value}/100"

    report += f"""

----------------------------------------

Total Marks: {total}/400
Percentage: {percentage:.2f}%
Performance: {performance}

Attendance: {data['attendance']}%
Daily Study: {data['study_hours']} hours
Daily Sleep: {data['sleep_hours']} hours

----------------------------------------

PERSONALIZED RECOMMENDATIONS

"""

    for i, recommendation in enumerate(recommendations, 1):
        report += f"\n{i}. {recommendation}"

    result_box.config(state="normal")
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, report)
    result_box.config(state="disabled")

    if display_graphs:
        show_charts(marks, data["attendance"])


# ================= ANALYZE BUTTON =================

def analyze_performance():

    try:
        data = collect_data()
        display_report(data, display_graphs=True)

    except ValueError as error:
        messagebox.showerror("Invalid Input", str(error))


# ================= SAVE BUTTON =================

def save_record():

    try:
        data = collect_data()
        save_student(data)

        messagebox.showinfo(
            "Success",
            "Student record saved successfully!"
        )

    except ValueError as error:
        messagebox.showerror("Invalid Input", str(error))

    except Exception as error:
        messagebox.showerror("Database Error", str(error))


# ================= SEARCH BUTTON =================

def search_record():

    enrollment = enroll_entry.get().strip()

    if not enrollment:
        messagebox.showwarning(
            "Missing Information",
            "Enter enrollment number to search."
        )
        return

    try:
        student = search_student(enrollment)

        if student is None:
            messagebox.showinfo(
                "Not Found",
                "No student record found."
            )
            return

        name_entry.delete(0, tk.END)
        name_entry.insert(0, student[1])

        for index, subject in enumerate(subjects, start=2):
            mark_entries[subject].delete(0, tk.END)
            mark_entries[subject].insert(
                0, str(student[index])
            )

        attendance_entry.delete(0, tk.END)
        attendance_entry.insert(0, str(student[6]))

        study_entry.delete(0, tk.END)
        study_entry.insert(0, str(student[7]))

        sleep_entry.delete(0, tk.END)
        sleep_entry.insert(0, str(student[8]))

        data = {
            "enrollment": student[0],
            "name": student[1],
            "Python": student[2],
            "Web Development": student[3],
            "DSA": student[4],
            "Calculus": student[5],
            "attendance": student[6],
            "study_hours": student[7],
            "sleep_hours": student[8]
        }

        display_report(data)

        messagebox.showinfo(
            "Success",
            "Student record found and loaded!"
        )

    except Exception as error:
        messagebox.showerror("Database Error", str(error))


# ================= CLEAR FUNCTION =================

def clear_fields():

    name_entry.delete(0, tk.END)
    enroll_entry.delete(0, tk.END)

    for entry in mark_entries.values():
        entry.delete(0, tk.END)

    attendance_entry.delete(0, tk.END)
    study_entry.delete(0, tk.END)
    sleep_entry.delete(0, tk.END)

    result_box.config(state="normal")
    result_box.delete("1.0", tk.END)
    result_box.config(state="disabled")


# ================= DELETE BUTTON =================

def delete_record():

    enrollment = enroll_entry.get().strip()

    if not enrollment:
        messagebox.showwarning(
            "Missing Information",
            "Enter enrollment number to delete."
        )
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Delete record for enrollment {enrollment}?"
    )

    if confirm:

        try:
            deleted = delete_student(enrollment)

            if deleted:
                clear_fields()

                messagebox.showinfo(
                    "Deleted",
                    "Student record deleted successfully!"
                )

            else:
                messagebox.showinfo(
                    "Not Found",
                    "No record found for this enrollment number."
                )

        except Exception as error:
            messagebox.showerror("Database Error", str(error))


# ================= STUDENT RECORDS DASHBOARD =================

def show_dashboard():

    dashboard = tk.Toplevel(root)
    dashboard.title("Student Records Dashboard")
    dashboard.geometry("850x550")
    dashboard.configure(bg=BG)
    dashboard.resizable(False, False)

    tk.Label(
        dashboard,
        text="STUDENT RECORDS DASHBOARD",
        font=("Arial", 20, "bold"),
        bg=BG,
        fg=WHITE
    ).pack(pady=15)

    # Summary section

    summary_frame = tk.Frame(dashboard, bg=BG)
    summary_frame.pack(fill="x", padx=20, pady=10)

    total_label = tk.Label(
        summary_frame,
        text="Total Students: 0",
        font=("Arial", 12, "bold"),
        bg=CARD,
        fg=WHITE,
        padx=20,
        pady=12
    )
    total_label.pack(side="left", padx=10)

    average_label = tk.Label(
        summary_frame,
        text="Class Average: 0%",
        font=("Arial", 12, "bold"),
        bg=CARD,
        fg=WHITE,
        padx=20,
        pady=12
    )
    average_label.pack(side="left", padx=10)

    # Records table

    table_frame = tk.Frame(dashboard, bg=BG)
    table_frame.pack(fill="both", expand=True, padx=20, pady=15)

    columns = (
        "enrollment",
        "name",
        "percentage",
        "grade"
    )

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=12
    )

    table.heading("enrollment", text="Enrollment Number")
    table.heading("name", text="Student Name")
    table.heading("percentage", text="Percentage")
    table.heading("grade", text="Performance")

    table.column("enrollment", width=180, anchor="center")
    table.column("name", width=220, anchor="center")
    table.column("percentage", width=150, anchor="center")
    table.column("grade", width=150, anchor="center")

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=table.yview
    )

    table.configure(yscrollcommand=scrollbar.set)

    table.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Refresh records

    def refresh_records():

        for item in table.get_children():
            table.delete(item)

        try:
            records = get_all_students()
            percentages = []

            for student in records:

                marks = student[2:6]
                percentage = sum(marks) / 4

                if percentage >= 85:
                    grade = "Excellent"
                elif percentage >= 70:
                    grade = "Good"
                elif percentage >= 50:
                    grade = "Average"
                else:
                    grade = "Needs Improvement"

                percentages.append(percentage)

                table.insert(
                    "",
                    "end",
                    values=(
                        student[0],
                        student[1],
                        f"{percentage:.2f}%",
                        grade
                    )
                )

            total_label.config(
                text=f"Total Students: {len(records)}"
            )

            if percentages:
                average = sum(percentages) / len(percentages)
            else:
                average = 0

            average_label.config(
                text=f"Class Average: {average:.2f}%"
            )

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                str(error),
                parent=dashboard
            )

    # Open selected student

    def open_selected_student(event):

        selected = table.selection()

        if not selected:
            return

        values = table.item(selected[0], "values")
        enrollment = values[0]

        try:
            student = search_student(enrollment)

            if student is None:
                messagebox.showinfo(
                    "Not Found",
                    "Student record no longer exists.",
                    parent=dashboard
                )
                refresh_records()
                return

            name_entry.delete(0, tk.END)
            name_entry.insert(0, student[1])

            enroll_entry.delete(0, tk.END)
            enroll_entry.insert(0, student[0])

            for index, subject in enumerate(subjects, start=2):
                mark_entries[subject].delete(0, tk.END)
                mark_entries[subject].insert(
                    0, str(student[index])
                )

            attendance_entry.delete(0, tk.END)
            attendance_entry.insert(0, str(student[6]))

            study_entry.delete(0, tk.END)
            study_entry.insert(0, str(student[7]))

            sleep_entry.delete(0, tk.END)
            sleep_entry.insert(0, str(student[8]))

            data = {
                "enrollment": student[0],
                "name": student[1],
                "Python": student[2],
                "Web Development": student[3],
                "DSA": student[4],
                "Calculus": student[5],
                "attendance": student[6],
                "study_hours": student[7],
                "sleep_hours": student[8]
            }

            display_report(data)
            dashboard.destroy()

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                str(error),
                parent=dashboard
            )

    table.bind("<Double-1>", open_selected_student)

    tk.Button(
        dashboard,
        text="Refresh Records",
        font=("Arial", 10, "bold"),
        bg=ACCENT,
        fg=WHITE,
        padx=15,
        pady=8,
        cursor="hand2",
        command=refresh_records
    ).pack(pady=10)

    refresh_records()


# ================= BUTTONS =================

button_frame = tk.Frame(root, bg=BG)
button_frame.pack(pady=10)

buttons = [
    ("Analyze", ACCENT, analyze_performance),
    ("Save Record", "#16865c", save_record),
    ("Search", "#2866b2", search_record),
    ("Delete", "#b94343", delete_record),
    ("Dashboard", "#805ad5", show_dashboard),
    ("Clear All", "#45455c", clear_fields)
]

for i, (label, color, action) in enumerate(buttons):

    tk.Button(
        button_frame,
        text=label,
        font=("Arial", 9, "bold"),
        bg=color,
        fg=WHITE,
        activeforeground=WHITE,
        padx=9,
        pady=9,
        cursor="hand2",
        command=action
    ).grid(row=0, column=i, padx=3)


# ================= SHOW RESULT SECTION =================

result_frame.pack(
    padx=30,
    pady=8,
    fill="both",
    expand=True
)


# ================= RUN APPLICATION =================

root.mainloop()
