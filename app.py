from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
from flask_cors import CORS
import os
import traceback

app = Flask(__name__)

app.secret_key = "financial_planner_secret_2026"

# Allow frontend access
CORS(app, origins=["*"])

# =========================
# MAIL CONFIGURATION
# =========================
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True

# Environment Variables from Render
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")

mail = Mail(app)

# =========================
# ROOT ROUTE
# =========================
@app.route("/")
def home():
    return render_template("index.html")

# =========================
# SEND EMAIL ROUTE
# =========================
@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        print("Request received...")

        pdf_file = request.files.get("pdf")
        excel_file = request.files.get("excel")

        if pdf_file is None:
            return jsonify({
                "success": False,
                "message": "PDF file missing"
            }), 400

        if excel_file is None:
            return jsonify({
                "success": False,
                "message": "Excel file missing"
            }), 400

        msg = Message(
            subject="New Financial Planning Form Submission",
            sender=app.config["MAIL_USERNAME"],
            recipients=["support@inxits.com"]
        )

        msg.body = """
A new financial planning form has been submitted.

PDF and Excel files are attached.
"""

        msg.attach(
            "Financial_Planning_Form.pdf",
            "application/pdf",
            pdf_file.read()
        )

        msg.attach(
            "Financial_Planning_Form.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            excel_file.read()
        )

        mail.send(msg)

        return jsonify({
            "success": True,
            "message": "Email sent successfully"
        })

    except Exception as e:
        traceback.print_exc()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)