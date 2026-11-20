
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import csv
import io
from urllib.parse import urlparse


HOST = "localhost"
PORT = 8000

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")


# ---------------------------------
# PERFORMANCE CALCULATION
# ---------------------------------

def calculate_performance(marks):

    total = round(sum(marks.values()), 2)
    maximum = len(marks) * 100
    percentage = (total / maximum) * 100

    strongest = max(marks, key=marks.get)
    weakest = min(marks, key=marks.get)

    if percentage >= 85:
        status = "Excellent"
    elif percentage >= 70:
        status = "Good"
    elif percentage >= 50:
        status = "Average"
    else:
        status = "Needs Improvement"

    return {
        "total": total,
        "maximum": maximum,
        "percentage": round(percentage, 2),
        "strongest": strongest,
        "weakest": weakest,
        "status": status
    }


# ---------------------------------
# STUDY HABIT ANALYSIS
# ---------------------------------

def analyze_habits(attendance, study_hours, sleep_hours):

    habits = []

    if attendance >= 85:
        habits.append("Excellent attendance.")
    else:
        habits.append("Try to improve your attendance.")

    if study_hours >= 4:
        habits.append("Good daily study routine.")
    else:
        habits.append("Increase your daily study time.")

    if sleep_hours >= 7:
        habits.append("Your sleep duration is healthy.")
    else:
        habits.append("Try to get at least 7 hours of sleep.")

    return habits


# ---------------------------------
# RECOMMENDATIONS
# ---------------------------------

def generate_recommendations(marks):

    recommendations = []

    for subject, score in marks.items():

        if score < 40:
            recommendations.append(
                f"{subject}: Immediate improvement required."
            )

        elif score < 60:
            recommendations.append(
                f"{subject}: Practice more questions."
            )

        elif score < 75:
            recommendations.append(
                f"{subject}: Revise regularly to improve."
            )

        else:
            recommendations.append(
                f"{subject}: Great performance. Keep it up!"
            )

    return recommendations


# ---------------------------------
# REQUEST HANDLER
# ---------------------------------

class StudentHandler(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            directory=STATIC_DIR,
            **kwargs
        )

    def send_json(self, data, status=200):

        response = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header(
            "Content-Type",
            "application/json"
        )
        self.send_header(
            "Content-Length",
            str(len(response))
        )
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

        self.wfile.write(response)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # ---------------------------------
    # GET REQUESTS
    # ---------------------------------

    def do_GET(self):

        path = urlparse(self.path).path

        if path == "/":
            self.path = "/index.html"
            return super().do_GET()

        return super().do_GET()

    # ---------------------------------
    # POST REQUESTS
    # ---------------------------------

    def do_POST(self):

        path = urlparse(self.path).path

        if path == "/analyze":

            try:
                content_length = int(
                    self.headers.get("Content-Length", 0)
                )

                body = self.rfile.read(content_length)

                data = json.loads(body.decode("utf-8"))

                name = str(data.get("name", "")).strip()
                enrollment = str(
                    data.get("enrollment", "")
                ).strip()

                if not name or not enrollment:
                    raise ValueError(
                        "Name and enrollment are required."
                    )

                subjects = [
                    "Python",
                    "Web Development",
                    "DSA",
                    "Calculus"
                ]

                marks = {}

                for subject in subjects:

                    value = float(data[subject])

                    if not 0 <= value <= 100:
                        raise ValueError(
                            f"{subject} marks must be between 0 and 100."
                        )

                    marks[subject] = value

                attendance = float(data["attendance"])
                study_hours = float(data["study_hours"])
                sleep_hours = float(data["sleep_hours"])

                if not 0 <= attendance <= 100:
                    raise ValueError(
                        "Attendance must be between 0 and 100."
                    )

                if not 0 <= study_hours <= 24:
                    raise ValueError(
                        "Study hours must be between 0 and 24."
                    )

                if not 0 <= sleep_hours <= 24:
                    raise ValueError(
                        "Sleep hours must be between 0 and 24."
                    )

                performance = calculate_performance(marks)

                habits = analyze_habits(
                    attendance,
                    study_hours,
                    sleep_hours
                )

                recommendations = generate_recommendations(
                    marks
                )

                result = {
                    "name": name,
                    "enrollment": enrollment,
                    "marks": marks,
                    "attendance": attendance,
                    "study_hours": study_hours,
                    "sleep_hours": sleep_hours,
                    "performance": performance,
                    "habits": habits,
                    "recommendations": recommendations
                }

                self.send_json({
                    "success": True,
                    "result": result
                })

            except (ValueError, KeyError, TypeError, json.JSONDecodeError) as error:

                self.send_json({
                    "success": False,
                    "error": str(error)
                }, 400)

        else:

            self.send_json({
                "success": False,
                "error": "Endpoint not found."
            }, 404)


# ---------------------------------
# START SERVER
# ---------------------------------

if __name__ == "__main__":

    server = HTTPServer(
        (HOST, PORT),
        StudentHandler
    )

    print("-----------------------------------")
    print(" SMART STUDENT PERFORMANCE ANALYZER")
    print("-----------------------------------")
    print(f"Server running at http://{HOST}:{PORT}")
    print("Press CTRL + C to stop the server.")

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nServer stopped.")

        server.server_close()
