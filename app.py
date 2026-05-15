from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import resend
import os
import traceback
import base64

app = Flask(__name__)

# Secret Key
app.secret_key = "financial_planner_secret_2026"

# Allow frontend access
CORS(app, origins=["*"])

# =========================
# RESEND CONFIGURATION
# =========================
resend.api_key = os.environ.get("RESEND_API_KEY")

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

        # Get uploaded files
        pdf_file = request.files.get("pdf")
        excel_file = request.files.get("excel")

        # Validate files
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

        # Read file data
        pdf_data = pdf_file.read()
        excel_data = excel_file.read()

        # Convert to Base64
        pdf_base64 = base64.b64encode(pdf_data).decode("utf-8")
        excel_base64 = base64.b64encode(excel_data).decode("utf-8")

        print("Sending email using Resend...")

        # Send Email
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": ["ansh.shah.1502@gmail.com"],
            "subject": "New Financial Planning Form Submission",
            "html": """
            <h2>New Financial Planning Form Submitted</h2>
            <p>PDF and Excel files are attached.</p>
            """,
            "attachments": [
                {
                    "filename": "Financial_Planning_Form.pdf",
                    "content": pdf_base64
                },
                {
                    "filename": "Financial_Planning_Form.xlsx",
                    "content": excel_base64
                }
            ]
        })

        print("Email sent successfully!")

        return jsonify({
            "success": True,
            "message": "Email sent successfully"
        })

    except Exception as e:
        print("\n========== ERROR ==========")
        traceback.print_exc()
        print("===========================\n")

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)