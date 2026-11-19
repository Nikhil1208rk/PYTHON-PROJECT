
import matplotlib.pyplot as plt


def show_charts(marks, attendance):

    # Subject-wise Performance
    subjects = list(marks.keys())
    scores = list(marks.values())

    plt.figure(figsize=(8, 5))
    plt.bar(subjects, scores)

    plt.title("Subject-wise Performance")
    plt.xlabel("Subjects")
    plt.ylabel("Marks")
    plt.ylim(0, 100)

    plt.tight_layout()
    plt.show()

    # Attendance Analysis
    plt.figure(figsize=(6, 6))

    plt.pie(
        [attendance, 100 - attendance],
        labels=["Present", "Remaining"],
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Attendance Analysis")
    plt.tight_layout()
    plt.show()
