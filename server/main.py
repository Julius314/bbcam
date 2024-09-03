import logging
from flask import Flask, render_template, Response, request, send_from_directory
from flask_socketio import SocketIO
import RPi.GPIO as GPIO
from modules.camera import VideoCamera
import os
import time

# Configure logging to output to a file
logging.basicConfig(filename='app.log', level=logging.DEBUG,
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
    logger.info("Rendering index page.")
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    logger.info("Video feed requested.")
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Take a photo when pressing camera button
@app.route('/picture')
def take_picture():
    logger.info("Picture requested.")
    picture_name, picture_data = pi_camera.take_picture()
    logger.info(f"Picture taken: {picture_name}")
    return Response(picture_data, mimetype='image/png', headers={'Content-Disposition': f'attachment;filename={picture_name}.png'})


@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    logger.info(f"Static file requested: {path}")
    return send_from_directory('./static/', path)


## socket connections
@socketio.on('connect')
def handle_connect():
    global n_clients
    n_clients += 1
    logger.info(f"Client connected. Total clients: {n_clients}")
    GPIO.output(IR_GPIO, GPIO.HIGH)
    logger.debug("IR LED turned ON.")

@socketio.on('disconnect')
def handle_disconnect():
    global n_clients
    n_clients -= 1
    logger.info(f"Client disconnected. Total clients: {n_clients}")
    if n_clients == 0:
        logger.info("No clients connected, turning off IR LED.")
        GPIO.output(IR_GPIO, GPIO.LOW)
        logger.debug("IR LED turned OFF.")

if __name__ == '__main__':
    logger.info("Starting Flask app on host 0.0.0.0, port 5005")
    app.run(host='0.0.0.0', debug=False, port=5005)
