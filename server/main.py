import logging
from flask import Flask, render_template, Response, request, send_from_directory
from flask_socketio import SocketIO
import RPi.GPIO as GPIO
from modules.camera import VideoCamera
import os
import time

# Configure logging to output to a file
logging.basicConfig(filename='bbcam_app.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

logger.info("Starting Flask application...")

pi_camera = VideoCamera(flip=False)  # flip pi camera if upside down.

# App Globals (do not edit)
app = Flask(__name__)
socketio = SocketIO(app)

IR_GPIO = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_GPIO, GPIO.OUT)
GPIO.output(IR_GPIO, GPIO.LOW)

n_clients = 0

def gen(camera):
    # Get camera frame
    while True:
        try:
            frame = camera.get_frame()
            logger.debug("Frame generated successfully.")
        except Exception as e:
            logger.error(f"Error generating frame: {e}")
            frame = camera.get_error_frame()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        time.sleep(0.2)

@app.route('/')
def index():
