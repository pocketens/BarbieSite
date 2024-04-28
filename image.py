import json
import random
import tkinter as tk
from tkinter import filedialog
from urllib import request


# Function to get image input from the user
def get_image_input():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select an image file",
        filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png"), ("all files", "*.*"))
    )
    print("File selected:", file_path)  # Confirm file selection
    return file_path


# This function sends a prompt workflow to the specified URL
def queue_prompt(prompt_workflow):
    try:
        p = {"prompt": prompt_workflow}
        data = json.dumps(p).encode('utf-8')
        headers = {'Content-Type': 'application/json'}
        req = request.Request("http://71.185.30.69:8188/prompt", data=data, headers=headers)
        print("Sending data to server...")  # Indicate data is being sent
        response = request.urlopen(req)
        print("Response Status:", response.status)  # Print response status
        print("Response Body:", response.read().decode())  # Print response body
    except request.HTTPError as e:
        print("HTTP Error:", e.code)
        print("Error Message:", e.read().decode())


# Load workflow api data from file and convert it into a dictionary
prompt_workflow = json.load(open('1workflow.json'))

# Get image input from the user
image_path = get_image_input()
img_input = prompt_workflow["12"]
img_input["inputs"]["image"] = image_path

# Create a list of prompts
prompt_list = [
    "a barbie doll, photorealistic, sharp image, masterpiece,35mm f4"
]

# Assign nodes to variables for easier access
node_keys = ["3", "4", "5", "6", "7", "8", "12", "14", "16", "21", "23", "35"]
nodes = {key: prompt_workflow[key] for key in node_keys}

# Set parameters and update settings
for key, node in nodes.items():
    print(f"Processing node {key}: {node['class_type']}")  # Display current node info
    if key == "12":
        node["inputs"]["image"] = image_path  # Set image input

# Load checkpoint, set dimensions, and output directory
nodes["4"]["inputs"]["ckpt_name"] = "sd_xl_1.0.safetensors"
print("Checkpoint loaded:", nodes["4"]["inputs"]["ckpt_name"])

nodes["5"]["inputs"]["width"] = 1024
nodes["5"]["inputs"]["height"] = 1250
nodes["5"]["inputs"]["batch_size"] = 1
print("Image dimensions set: 512x640")

nodes["35"]["inputs"]["output_directory"] = "C:/Users/pocke/PycharmProjects/pythonProject/outputs"
nodes["35"]["inputs"]["filename_prefix"] = "Barbified"
print("Output directory set:", nodes["35"]["inputs"]["output_directory"])

# Process each prompt
for index, prompt in enumerate(prompt_list):
    print("Processing prompt:", prompt)
    nodes["6"]["inputs"]["text"] = prompt
    nodes["3"]["inputs"]["seed"] = random.randint(1, 18446744073709551614)

    if index == 3:
        nodes["5"]["inputs"]["height"] = 768

    fileprefix = prompt[:100]
    fileprefixafteredit = random.randint(1, 5500)
    nodes["35"]["inputs"]["filename_prefix"] = fileprefixafteredit
    queue_prompt(prompt_workflow)

print("All prompts processed.")
