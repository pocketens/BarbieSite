import os
import random
import re
import subprocess
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'C:/Users/pocke/PycharmProjects/pythonProject/uploads'
PROCESSED_FOLDER = 'C:/Users/pocke/PycharmProjects/pythonProject/processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return filename.lower().endswith(('.jpg', '.png', '.jpeg'))

def generate_filename(original_filename):
    """Generate a new filename with a 'Barbify' prefix and a random number."""
    ext = original_filename.rsplit('.', 1)[1]
    new_name = f"Barbify_{random.randint(1000, 9999)}.{ext}"
    return new_name

@app.route('/', methods=['GET'])
def index():
    """Render the main page with the file upload form."""
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads and trigger the processing script."""
    if 'file' not in request.files:
        return jsonify(message="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(message="No selected file"), 400
    if file and allowed_file(file.filename):
        new_filename = generate_filename(file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(image_path)

        # Open the image to get dimensions
        with Image.open(image_path) as img:
            width, height = img.size

        # Run the processing script and pass width and height
        subprocess.run(['python', 'process_api_call.py', image_path, str(width), str(height)], check=True)

        return redirect(url_for('display_image', filename=new_filename))
    else:
        return jsonify(message="Invalid file type"), 400

@app.route('/display_image/<filename>')
def display_image(filename):
    """Display the page for viewing the processed image."""
    return render_template('display_image.html', filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/processed/<filename>')
def processed_file(filename):
    """Serve processed files."""
    try:
        return send_from_directory(app.config['PROCESSED_FOLDER'], filename)
    except FileNotFoundError:
        return "File not found", 404  # Handling file not found to return a clearer message

@app.route('/next-filename')
def next_filename():
    """Determine the next expected processed filename based on existing files."""
    files = os.listdir(app.config['PROCESSED_FOLDER'])
    highest_number = 0
    for file in files:
        match = re.match(r"Barbify_(\d+)\.png", file)
        if match:
            number = int(match.group(1))
            if number > highest_number:
                highest_number = number
    next_filename = f"Barbify_{highest_number + 1}.png"
    return jsonify(next_filename=next_filename)

if __name__ == '__main__':
    app.run(debug=True)
