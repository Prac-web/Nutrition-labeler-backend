from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from weasyprint import HTML, CSS
import tempfile
import uuid
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home() :
    return "<h1>Hello World</h1>"

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.get_json()
        html = data.get("html", "")
        width = data.get("width", "210mm")
        height = data.get("height", "297mm")

        print("HTML Received:", html)
        print(f"Using custom PDF size: {width} x {height}")

        # CSS to remove margins and fix page size
        custom_css = f"""
        @page {{ size: {width} {height}; margin: 0mm; }}
        html, body {{ margin: 0; padding: 0; }}
        """

        # Generate a unique filename in a temporary directory
        unique_filename = f"label_{uuid.uuid4().hex}.pdf"
        temp_path = os.path.join(tempfile.gettempdir(), unique_filename)

        # Generate the PDF file
        HTML(string=html).write_pdf(temp_path, stylesheets=[CSS(string=custom_css)])

        print(f"✅ PDF created at {temp_path}")

        # Send the PDF as a file download
        return send_file(temp_path, as_attachment=True, download_name=unique_filename)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
