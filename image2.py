from flask import Flask, request, render_template, redirect, url_for
import os
import json

app = Flask(__name__)

# Ensure there's a folder to save uploaded images and outputs
UPLOAD_FOLDER = 'uploads/'
OUTPUT_FOLDER = 'outputs/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Your existing functions to process the image
def process_image(image_path):
    # Load workflow api data from file and convert it into a dictionary
    with open('1workflow.json', 'r') as f:
        prompt_workflow = json.load(f)

    # Here you would integrate your existing Python logic
    # For now, just an example of how you might adjust the image path
    prompt_workflow["12"]["inputs"]["image"] = image_path

    # Assume processing happens here and maybe save some output
    output_path = os.path.join(OUTPUT_FOLDER, 'result.jpg')
    # Fake processing, in reality, you would call your existing function
    # For demonstration, just copy the uploaded file to output
    import shutil
    shutil.copy(image_path, output_path)

    return output_path

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filename)
            processed_file = process_image(filename)
            return redirect(url_for('uploaded_file', filename=processed_file))
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return f'Result saved in: {filename}'

if __name__ == '__main__':
    app.run(debug=True)
