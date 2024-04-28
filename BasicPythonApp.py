import json
from urllib import request, parse
import random

# This function sends a prompt workflow to the specified URL
# (http://127.0.0.1:8188/prompt) and queues it on the ComfyUI server
# running at that address.
def queue_prompt(prompt_wokflow):
    try:
        p = {"prompt": prompt_workflow}
        data = json.dumps(p).encode('utf-8')
        headers = {'Content-Type': 'application/json'}
        req = request.Request("http://127.0.0.1:8188/prompt", data=data, headers=headers)
        response = request.urlopen(req)
        print("Response Status:", response.status)
        print("Response Body:", response.read().decode())
    except request.HTTPError as e:
        print("HTTP Error:", e.code)
        print("Error Message:", e.read().decode())

# Load workflow api data from file and convert it into a dictionary
# assign to var prompt_workflow
prompt_workflow = json.load(open('workflow_api.json'))

# Create a list of prompts
prompt_list = [
    "photo of a man sitting in a cafe",
    "photo of a woman standing in the middle of a busy street",
    "drawing of a cat sitting in a tree",
    "beautiful scenery nature glass bottle landscape, purple galaxy bottle"
]

# Give some easy-to-remember names to the nodes
chkpoint_loader_node = prompt_workflow["4"]
prompt_pos_node = prompt_workflow["6"]
empty_latent_img_node = prompt_workflow["5"]
ksampler_node = prompt_workflow["3"]
save_image_node = prompt_workflow["9"]

# Load the checkpoint that we want
chkpoint_loader_node["inputs"]["ckpt_name"] = "v1-5-pruned-emaonly.safetensors"

# Set image dimensions and batch size in EmptyLatentImage node
empty_latent_img_node["inputs"]["width"] = 512
empty_latent_img_node["inputs"]["height"] = 640
empty_latent_img_node["inputs"]["batch_size"] = 4

# Set the output directory for saved images
save_image_node["inputs"]["output_directory"] = "R:\\ComfyUI\\ComfyUI_windows_portable\\ComfyUI\\output"

# Process each prompt in the list
for index, prompt in enumerate(prompt_list):
    # Set the text prompt for positive CLIPTextEncode node
    prompt_pos_node["inputs"]["text"] = prompt

    # Set a random seed in KSampler node
    ksampler_node["inputs"]["seed"] = random.randint(1, 18446744073709551614)

    # If it is the last prompt, set latent image height to 768
    if index == 3:
        empty_latent_img_node["inputs"]["height"] = 768

    # Set filename prefix to be the same as prompt (truncate if necessary)
    fileprefix = prompt[:100]  # Truncate to first 100 characters
    save_image_node["inputs"]["filename_prefix"] = fileprefix

    # Everything set, add entire workflow to queue.
    queue_prompt(prompt_workflow)
