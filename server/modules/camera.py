#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This scrtipt script..

import cv2 as cv
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
from datetime import datetime
import numpy as np

class VideoCamera(object):
    def __init__(self, flip = False, file_type  = ".jpg", photo_string= "stream_photo"):
        resolution = (800, 608)
        self.vs = PiVideoStream(resolution=resolution, framerate=30).start()
        # self.vs = PiVideoStream().start()
        self.flip = flip # Flip frame vertically
        self.file_type = file_type # image type i.e. .jpg
        self.photo_string = photo_string # Name to save the photo
        self.indicator_state = 0

        self.width, self.height = resolution
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read()).copy()
        self.indicator_state = (self.indicator_state + 1) % 10
        gray_value = int(self.indicator_state * 255 / 9)  # Map to [0, 255]

        frame[self.height - 10:self.height, 0:10] = [gray_value, gray_value, gray_value]
        
        ret, jpeg = cv.imencode(self.file_type, frame)
        self.previous_frame = jpeg
        return jpeg.tobytes()

    # Take a photo, called by camera button
    def take_picture(self):
        frame = self.flip_if_needed(self.vs.read())
        ret, image = cv.imencode(self.file_type, frame)
        today_date = datetime.now().strftime("%m%d%Y-%H%M%S") # get current time
        # cv.imwrite(str(self.photo_string + "_" + today_date + self.file_type), frame)
        return f"bbcam_{today_date}", image.tobytes()
