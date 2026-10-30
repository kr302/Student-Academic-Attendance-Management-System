from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import date

app = Flask(__name__)

DATA_FILE = "students_data.json"


def load_students():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        students = json.load(file)

    for s in students:
        s.setdefault("attendance_log", [])
        s["total_classes"] = len(s["attendance_log"])
        s["present_count"] = sum(
            1 for a in s["attendance_log"] if a["status"] == "Present"
        )
        s["attendance"] = (
            round(s["present_count"] / s["total_classes"] * 100)
            if s["total_classes"] else 0
        )

    return students


def save_students(students):
    with open(DATA_FILE, "w") as file:
        json.dump(students, file, indent=4)


@app.route("/")
def home():
    students = load_students()
    save_students(students)

    total = len(students)
    low_attendance = sum(
        1 for s in students if s["attendance"] < 75
    )

    query = request.args.get("search", "").lower()

    if query:
        students = [
            s for s in students
            if query in s["name"].lower()
            or query in s["roll"].lower()
        ]

    return render_template(
        "index.html",
        students=students,
        total=total,
        low_attendance=low_attendance
    )


@app.route("/add", methods=["POST"])
def add_student():
    students = load_students()

    roll = request.form["roll"].strip()
    name = request.form["name"].strip()
    course = request.form["course"].strip()
    email = request.form["email"].strip()

    if not all([roll, name, course, email]):
        return "Please fill all fields", 400

    if any(s["roll"] == roll for s in students):
        return "Roll number already exists", 400

    students.append({
        "roll": roll,
        "name": name,
        "course": course,
        "email": email,
        "attendance_log": [],
        "total_classes": 0,
        "present_count": 0,
        "attendance": 0
    })

    save_students(students)
    return redirect(url_for("home"))


@app.route("/attendance/<roll>/<status>", methods=["POST"])
def mark_attendance(roll, status):
    if status not in ["Present", "Absent"]:
        return "Invalid attendance status", 400

    students = load_students()
    today = date.today().isoformat()

    for s in students:
        if s["roll"] == roll:
            record = next(
                (a for a in s["attendance_log"]
                 if a["date"] == today),
                None
            )

            if record:
                record["status"] = status
            else:
                s["attendance_log"].append({
                    "date": today,
                    "status": status
                })

            break

    save_students(students)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)