import os
import uuid
import cv2
import numpy as np
import google.generativeai as genai
import pandas as pd
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

# Flask App Initialization
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov'}

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# API Key for Gemini
GEMINI_API_KEY = "AIzaSyDqv1F3J6cb6BIT2Y_fghQRksBdxvJ8E-0"

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
gemini_vision_model = genai.GenerativeModel("models/gemini-2.0-flash")

# CSV File for Location Data Storage
LOCATION_CSV_FILE = "location_data.csv"

# Ensure CSV File Exists
if not os.path.exists(LOCATION_CSV_FILE):
    df = pd.DataFrame(columns=["UUID", "Video Path", "Image Path", "Location Description", 
                              "Coordinates", "Confidence Score", "Timestamp"])
    df.to_csv(LOCATION_CSV_FILE, index=False)

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

### VIDEO FRAME EXTRACTION ###
def extract_video_frames(video_path, output_frame_path):
    """Extract key frames from video for analysis"""
    video = cv2.VideoCapture(video_path)
    
    # Save middle frame
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    middle_frame = total_frames // 2
    video.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)
    success, frame = video.read()
    
    if success:
        cv2.imwrite(output_frame_path, frame)
        video.release()
        return True
    
    video.release()
    return False

### ANALYZE LOCATION DATA ###
def analyze_location_data(video_path, image_path):
    """Analyze drone video and satellite image to determine location"""
    # Extract a frame from the video
    video_frame_path = os.path.join(app.config['UPLOAD_FOLDER'], 'video_frame.jpg')
    frame_extracted = extract_video_frames(video_path, video_frame_path)
    
    if not frame_extracted:
        return {"error": "Failed to extract frame from video"}
    
    # Read files as binary for Gemini Vision
    with open(video_frame_path, "rb") as v_file, open(image_path, "rb") as i_file:
        video_frame_data = v_file.read()
        satellite_image_data = i_file.read()
    
    # Create multimodal prompt for Gemini
    prompt = """
    I'm providing two images:
    1. A frame from a drone video
    2. A satellite/aerial image
    
    Please analyze both images and:
    1. Determine potential location based on visual features
    2. Identify any matching landmarks, terrain patterns, or structures
    3. Provide coordinates (approximate) where the drone video might have been taken within the satellite image
    4. Provide a confidence score (1-10) for this location match
    5. Describe the specific point where the drone video was likely taken
    
    Format the coordinates as x,y percentages of the image dimensions where (0,0) is top-left
    and (100,100) is bottom-right of the satellite image.
    """
    
    response = gemini_vision_model.generate_content([
        prompt, 
        {"mime_type": "image/jpeg", "data": video_frame_data},
        {"mime_type": "image/jpeg", "data": satellite_image_data}
    ])
    
    # Extract coordinates from response
    analysis = response.text
    
    # Parsing logic for coordinates and confidence
    coordinates = "50,50"  # Default to center
    confidence = 5  # Default medium confidence
    
    for line in analysis.split('\n'):
        if "coordinates" in line.lower() and "%" in line:
            # Try to extract coordinates in format like "coordinates: 35,62"
            try:
                coordinates = line.split(":")[1].strip()
                # Clean up any extra text, keeping just the x,y values
                coordinates = coordinates.split('(')[0].strip()
                if "%" in coordinates:
                    coordinates = coordinates.replace("%", "").strip()
            except:
                pass
        elif "confidence" in line.lower() and any(str(i) in line for i in range(10)):
            # Try to extract confidence score
            try:
                confidence = int(line.split(":")[1].strip().split('/')[0].strip())
            except:
                pass
    
    # Parse coordinates
    try:
        x_coord, y_coord = coordinates.split(',')
        x_percentage = float(x_coord.strip())
        y_percentage = float(y_coord.strip())
    except:
        x_percentage, y_percentage = 50, 50  # Default to center if parsing fails
    
    # Ensure values are within 0-100 range
    x_percentage = max(0, min(100, x_percentage))
    y_percentage = max(0, min(100, y_percentage))
    
    # Save analysis to CSV
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    location_uuid = str(uuid.uuid4())
    
    df = pd.read_csv(LOCATION_CSV_FILE)
    new_entry = pd.DataFrame([{
        "UUID": location_uuid,
        "Video Path": video_path,
        "Image Path": image_path,
        "Location Description": analysis,
        "Coordinates": f"{x_percentage},{y_percentage}",
        "Confidence Score": confidence,
        "Timestamp": timestamp
    }])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(LOCATION_CSV_FILE, index=False)
    
    # Return analysis and coordinates
    return {
        "uuid": location_uuid,
        "description": analysis,
        "coordinates": f"{x_percentage},{y_percentage}",
        "confidence": confidence,
        "video_frame": os.path.basename(video_frame_path),
        "satellite_image": os.path.basename(image_path)
    }

### FLASK ROUTES ###
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload_location_data', methods=['POST'])
def upload_location_data():
    if 'video' not in request.files or 'image' not in request.files:
        return jsonify({"error": "Both video and image files are required"}), 400
        
    video_file = request.files['video']
    image_file = request.files['image']
    
    if video_file.filename == '' or image_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if not (allowed_file(video_file.filename) and allowed_file(image_file.filename)):
        return jsonify({"error": "File type not allowed"}), 400
    
    # Save files
    video_filename = secure_filename(f"{uuid.uuid4()}_{video_file.filename}")
    image_filename = secure_filename(f"{uuid.uuid4()}_{image_file.filename}")
    
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    
    video_file.save(video_path)
    image_file.save(image_path)
    
    # Analyze location
    result = analyze_location_data(video_path, image_path)
    
    return jsonify(result)

@app.route('/get_location_data', methods=['GET'])
def get_location_data():
    if os.path.exists(LOCATION_CSV_FILE):
        df = pd.read_csv(LOCATION_CSV_FILE)
        if not df.empty:
            latest_entry = df.iloc[-1].to_dict()
            return jsonify(latest_entry)
    
    return jsonify({"message": "No location data available"})

@app.route('/get_all_locations', methods=['GET'])
def get_all_locations():
    if os.path.exists(LOCATION_CSV_FILE):
        df = pd.read_csv(LOCATION_CSV_FILE)
        return jsonify(df.to_dict(orient='records'))
    
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)