import sys
import json
from urllib import request as url_request
import os

def queue_prompt(image_path, width, height, processed_dir):
    try:
        # Load your existing processing configuration
        prompt_workflow = json.load(open('workflow11.json'))

        # Update workflow with the image path and dimensions
        prompt_workflow["12"]["inputs"]["image"] = image_path

        # Update the output path to include the processed directory
        prompt_workflow["42"]["inputs"]["output_path"] = processed_dir

        # Serialize the modified workflow and send it to your processing API
        data = json.dumps({"prompt": prompt_workflow}).encode('utf-8')
        headers = {'Content-Type': 'application/json'}
        req = url_request.Request("http://71.185.30.69:8188/prompt", data=data, headers=headers)
        response = url_request.urlopen(req)
        print("Response Status:", response.status)
        print("Response Body:", response.read().decode())
    except url_request.HTTPError as e:
        print("HTTP Error:", e.code, e.read().decode())

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python process_api_call.py <image_path> <width> <height> <processed_dir>")
        sys.exit(1)

    image_path = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    processed_dir = sys.argv[4]

    queue_prompt(image_path, width, height, processed_dir)