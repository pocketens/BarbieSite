import sys
import json
from urllib import request as url_request


def queue_prompt(image_path, width, height):
    """Send the image to the API server and handle the response with width and height adjustments."""
    try:
        # Load your existing processing configuration
        prompt_workflow = json.load(open('2workflow.json'))

        # Update workflow with the image path and dimensions
        prompt_workflow["5"]["inputs"]["width"] = width  # Set width from passed parameter
        prompt_workflow["5"]["inputs"]["height"] = height  # Set height from passed parameter
        prompt_workflow["12"]["inputs"]["image"] = image_path


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
    # Check for proper command line arguments
    if len(sys.argv) < 4:
        print("Usage: python process_api_call.py <image_path> <width> <height>")
        sys.exit(1)

    image_path = sys.argv[1]
    # Convert width and height to integer
    width = int(sys.argv[2])
    height = int(sys.argv[3])

    queue_prompt(image_path, width, height)
