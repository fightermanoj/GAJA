# run_reconstruction_client.py
import requests
import os
import time

# --- Configuration ---
# Replace with the public URL provided by Lightning AI for your running Flask app
SERVER_URL = "https://8080-01jt03by8spm9csq5dcmkfw4ge.cloudspaces.litng.ai" # e.g., "https://your-app-id.lightning.ai"
RECONSTRUCT_ENDPOINT = f"{SERVER_URL}/reconstruct"
HEALTH_CHECK_ENDPOINT = f"{SERVER_URL}/"

LOCAL_VIDEO_PATH = "chair.mp4" # Will be asked from the user
DOWNLOAD_DESTINATION_FOLDER = "E:\CBC"

# Optional parameters to send to the server for GLB generation
# These should match the defaults or desired values from your Gradio app / server
GLB_PARAMS = {
    "conf_thres": "3.0",      # Note: send as string if using multipart/form-data
    "frame_filter": "All",
    "mask_black_bg": "false",
    "mask_white_bg": "false",
    "show_cam": "true",
    "mask_sky": "false",
    "prediction_mode": "Depthmap and Camera Branch"
}
# --- End Configuration ---

def check_server_health(url):
    print(f"Checking server health at {url}...")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes
        print(f"Server is healthy: {response.json()}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Server health check failed: {e}")
        return False

def upload_and_reconstruct(video_path, glb_parameters):
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at '{video_path}'")
        return None

    os.makedirs(DOWNLOAD_DESTINATION_FOLDER, exist_ok=True)
    
    video_filename = os.path.basename(video_path)
    
    files = {'video': (video_filename, open(video_path, 'rb'), 'video/mp4')} # Specify content type
    # `glb_parameters` will be sent as form data
    
    print(f"\nUploading '{video_filename}' to {RECONSTRUCT_ENDPOINT} with parameters: {glb_parameters}")
    
    try:
        start_time = time.time()
        # Send GLB_PARAMS as `data` for form fields, `files` for file upload
        response = requests.post(RECONSTRUCT_ENDPOINT, files=files, data=glb_parameters, timeout=600) # Increased timeout for long processing
        end_time = time.time()
        print(f"Upload and server processing took {end_time - start_time:.2f} seconds.")

        response.raise_for_status() # Raises an HTTPError for bad responses (4XX or 5XX)

        # Determine filename for saving
        content_disposition = response.headers.get('Content-Disposition')
        if content_disposition:
            parts = content_disposition.split('filename=')
            if len(parts) > 1:
                output_filename = parts[1].strip('"')
            else:
                output_filename = f"reconstructed_{os.path.splitext(video_filename)[0]}.glb"
        else:
            output_filename = f"reconstructed_{os.path.splitext(video_filename)[0]}.glb"

        destination_path = os.path.join(DOWNLOAD_DESTINATION_FOLDER, output_filename)
        
        with open(destination_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Success! 3D model saved to: {destination_path}")
        return destination_path

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
    except requests.exceptions.ConnectionError:
        print(f"Connection Error: Could not connect to the server at {SERVER_URL}.")
        print("Please ensure the server is running and the URL is correct.")
    except requests.exceptions.Timeout:
        print("Request Timed Out: The server took too long to respond.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return None

if __name__ == "__main__":
    if SERVER_URL == "YOUR_LIGHTNING_AI_FLASK_APP_URL" or not SERVER_URL:
        print("ERROR: Please update the 'SERVER_URL' variable in the script with the public URL of your Lightning AI Flask app.")
    else:
        if check_server_health(HEALTH_CHECK_ENDPOINT):
            while True:
                LOCAL_VIDEO_PATH = input("Enter the full path to your local video file (or type 'exit' to quit): ")
                if LOCAL_VIDEO_PATH.lower() == 'exit':
                    break
                if os.path.isfile(LOCAL_VIDEO_PATH):
                    upload_and_reconstruct(LOCAL_VIDEO_PATH, GLB_PARAMS)
                else:
                    print(f"File not found: '{LOCAL_VIDEO_PATH}'. Please enter a valid path.")
            print("Client finished.")
        else:
            print("Cannot proceed without a healthy server. Please check the server status and URL.")