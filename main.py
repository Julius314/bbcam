#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This web application serves a motion JPEG stream
# main.py
# import the necessary packages
from flask import Flask, render_template, Response, request, send_from_directory
from flask_socketio import SocketIO
import RPi.GPIO as GPIO
from modules.camera import VideoCamera
import os

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

# App Globals (do not edit)
app = Flask(__name__)
socketio = SocketIO(app)

IR_GPIO = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_GPIO, GPIO.OUT)
GPIO.output(IR_GPIO, GPIO.LOW)

n_clients = 0

def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Take a photo when pressing camera button
@app.route('/picture')
def take_picture():
    picture_name, picture_data = pi_camera.take_picture()
    return Response(picture_data, mimetype='image/png', headers={'Content-Disposition': f'attachment;filename={picture_name}.png'})

@socketio.on('connect')
def handle_connect():
    global n_clients
    GPIO.output(IR_GPIO, GPIO.HIGH)
    n_clients += 1


@socketio.on('disconnect')
def handle_disconnect():
    global n_clients
    n_clients -= 1
    if n_clients == 0:
        print("no clientes, turn off IR")
        GPIO.output(IR_GPIO, GPIO.LOW)

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False, port=5005)
