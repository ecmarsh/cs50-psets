import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Redirect main page to form


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")

# Render form page


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")

# Post form data on submit


@app.route("/form", methods=["POST"])
def post_form():
    if not request.form.get("name") or not request.form.get("email") or not request.form.get("about"):
        return render_template("error.html", message="Sorry 😓 an error occured!")

    with open('survey.csv', 'a', newline='') as file:
        fieldnames = ['name', 'email', 'difficulty', 'score', 'about', 'agree']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({
            'name': request.form.get("name"),
            'email': request.form.get("email"),
            'difficulty': request.form.get("difficulty"),
            'score': request.form.get("score"),
            'about': request.form.get("about"),
            'agree': request.form.get("agree")
        })
    return redirect("/sheet")

# Route to data sheet


@app.route("/sheet", methods=["GET"])
def get_sheet():
    with open("survey.csv", newline='') as file:
        reader = csv.DictReader(file)
        return render_template("sheet.html", answers=reader)
    return render_template("error.html", message="Error rendering sheet 🙀")

