import os
import random
import re
import subprocess
import logging
import time
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
from PIL import Image
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

UPLOAD_FOLDER = 'C:/Users/pocke/PycharmProjects/pythonProject/uploads'
PROCESSED_FOLDER = 'C:/Users/pocke/PycharmProjects/pythonProject/processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        logger.error("No file part in the request")
        return jsonify(message="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        logger.error("No selected file")
        return jsonify(message="No selected file"), 400
    if file and allowed_file(file.filename):
        new_filename = generate_filename(file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(image_path)
        logger.info(f"Uploaded image: {new_filename}")

        # Create a directory under 'processed' with the new filename (without extension)
        processed_dir = os.path.join(app.config['PROCESSED_FOLDER'], new_filename.split('.')[0])
        os.makedirs(processed_dir, exist_ok=True)

        # Open the image to get dimensions
        with Image.open(image_path) as img:
            width, height = img.size

        # Run the processing script and pass width and height
        logger.info(f"Running processing script for image: {new_filename}")
        subprocess.run(['python', 'process_api_call.py', image_path, str(width), str(height), processed_dir], check=True)

        return redirect(url_for('display_image', filename=new_filename))
    else:
        logger.error("Invalid file type")
        return jsonify(message="Invalid file type"), 400

@app.route('/display_image/<filename>')
def display_image(filename):
    """Display the page for viewing the processed image."""
    return render_template('display_image.html', filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/processed/<path:filename>')
def processed_file(filename):
    """Serve processed files."""
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

@app.route('/poll_processed/<filename>')
def poll_processed(filename):
    """Poll for the processed image file."""
    processed_dir = os.path.join(app.config['PROCESSED_FOLDER'], filename.split('.')[0])
    while True:
        for file in os.listdir(processed_dir):
            if file.lower().endswith(('.jpg', '.png', '.jpeg')):
                return jsonify(filename=file)
        time.sleep(1)  # Wait for 1 second before checking again

if __name__ == '__main__':
    socketio.run(app, debug=True)