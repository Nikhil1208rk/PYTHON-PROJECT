
from flask import Flask, render_template, request, make_response

app = Flask(__name__)

SUBJECT_COLORS = {
    "Python": "#8b5cf6",
    "Web Development": "#34d399",
    "DSA": "#f59e0b",
    "Calculus": "#38bdf8"
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        name = request.form.get("name", "").strip()
        enrollment = request.form.get("enrollment", "").strip()

        marks = {
            "Python": int(request.form.get("python", "")),
            "Web Development": int(request.form.get("webdev", "")),
            "DSA": int(request.form.get("dsa", "")),
            "Calculus": int(request.form.get("calculus", ""))
        }

        study_hours = float(request.form.get("study_hours", ""))
        attendance = float(request.form.get("attendance", ""))
        sleep_hours = float(request.form.get("sleep_hours", ""))

    except (ValueError, TypeError):
        return "Please enter valid numeric values in all fields.", 400

    if not name or not enrollment:
        return "Name and enrollment number are required.", 400

    if any(score < 0 or score > 100 for score in marks.values()):
        return "Marks must be between 0 and 100.", 400

    if not 0 <= attendance <= 100:
        return "Attendance must be between 0 and 100.", 400

    if not 0 <= study_hours <= 24 or not 0 <= sleep_hours <= 24:
        return "Study and sleep hours must be between 0 and 24.", 400

    # Calculate total and percentage
    total_marks = sum(marks.values())
    max_total_marks = 400
    average = total_marks / len(marks)
    overall_percentage = round(total_marks / max_total_marks * 100, 2)

    # Highest and lowest scoring subjects
    highest_subject = max(marks, key=marks.get)
    lowest_subject = min(marks, key=marks.get)

    highest_marks = marks[highest_subject]
    lowest_marks = marks[lowest_subject]

    # Overall status
    if average >= 80:
        status = "Excellent Performance"
    elif average >= 60:
        status = "Good Performance"
    elif average >= 40:
        status = "Average Performance"
    else:
        status = "Needs Improvement"

    # Recommendations
    recommendations = []

    for subject, score in marks.items():
        if score < 40:
            recommendations.append(
                f"{subject}: Revise the basics and practise questions daily."
            )
        elif score < 60:
            recommendations.append(
                f"{subject}: Focus on weaker topics and solve more questions."
            )
        elif score >= 80:
            recommendations.append(
                f"{subject}: Great work! Continue regular revision."
            )
        else:
            recommendations.append(
                f"{subject}: Keep practising to improve your score."
            )

    if attendance < 75:
        recommendations.append(
            "Your attendance is below 75%. Try to attend classes regularly."
        )
    else:
        recommendations.append(
            "Your attendance is satisfactory. Keep attending classes."
        )

    if study_hours < 2:
        recommendations.append(
            "Gradually increase your focused study time."
        )
    elif study_hours >= 6:
        recommendations.append(
            "Take regular breaks and maintain a balanced study routine."
        )
    else:
        recommendations.append(
            "Maintain your daily study routine and revise regularly."
        )

    if sleep_hours < 7:
        recommendations.append(
            "Try to get sufficient sleep and maintain a regular sleep schedule."
        )
    elif sleep_hours > 9:
        recommendations.append(
            "Maintain a consistent sleep schedule and review your daily routine."
        )
    else:
        recommendations.append(
            "Keep maintaining a consistent sleep schedule."
        )

    return render_template(
        "result.html",
        name=name,
        enrollment=enrollment,
        marks=marks,
        total_marks=total_marks,
        max_total_marks=max_total_marks,
        average=round(average, 2),
        overall_percentage=overall_percentage,
        highest_subject=highest_subject,
        highest_marks=highest_marks,
        lowest_subject=lowest_subject,
        lowest_marks=lowest_marks,
        status=status,
        study_hours=study_hours,
        attendance=attendance,
        sleep_hours=sleep_hours,
        recommendations=recommendations
    )


@app.route("/dashboard.css")
def dashboard_css():
    # Read and validate values used by the chart stylesheet.
    def read_number(key, default=0.0):
        try:
            value = float(request.args.get(key, default))
        except (ValueError, TypeError):
            value = default

        if not 0 <= value <= 100:
            value = default

        return value

    attendance = read_number("attendance")
    scores = {
        "Python": read_number("python"),
        "Web Development": read_number("webdev"),
        "DSA": read_number("dsa"),
        "Calculus": read_number("calculus")
    }

    total = sum(scores.values())
    percentage = round(total / 4, 2)

    # Attendance chart
    attendance_css = (
        "conic-gradient("
        f"#34d399 0% {attendance}%, "
        f"#334155 {attendance}% 100%)"
    )

    # Subject marks chart
    if total > 0:
        segments = []
        start = 0.0

        for subject, score in scores.items():
            end = start + (score / total) * 100
            color = SUBJECT_COLORS[subject]
            segments.append(f"{color} {start:.4f}% {end:.4f}%")
            start = end

        subject_css = "conic-gradient(" + ", ".join(segments) + ")"
    else:
        subject_css = "conic-gradient(#334155 0% 100%)"

    css = f"""
    .progress-fill {{
        width: {percentage}%;
    }}

    .attendance-chart {{
        background: {attendance_css};
    }}

    .subject-chart {{
        background: {subject_css};
    }}
    """

    response = make_response(css)
    response.headers["Content-Type"] = "text/css; charset=utf-8"
    response.headers["Cache-Control"] = "no-store"

    return response


if __name__ == "__main__":
    app.run(debug=True)
