from flask import Flask, render_template, request, send_from_directory, redirect, url_for, jsonify
import os
import pandas as pd
import logging
from resume_extractor import process_resume, save_to_excel

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "uploads"
EXCEL_FILE = "resume_data.xlsx"
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/resume_container", endpoint="resume_builder")
def build_resume():
    return render_template("index.html")

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded!"}), 400

    file = request.files["file"]

    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file format!"}), 400

    filename = file.filename
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    try:
        extracted_data = process_resume(file_path)
        if not extracted_data:
            return jsonify({"error": "Extraction failed!"}), 500
        save_to_excel(extracted_data)
    except Exception as e:
        logging.error(f"Resume processing failed: {e}")
        return jsonify({"error": "Resume extraction failed!"}), 500

    return redirect(url_for("upload_success", filename=filename))

@app.route("/upload_success/<filename>")
def upload_success(filename):
    return render_template("upload_success.html", filename=filename)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)
