import logging
import cv2 as cv
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
from datetime import datetime
import numpy as np

# Configure logging
logger = logging.getLogger()

class VideoCamera(object):
    def __init__(self, flip=False, file_type=".jpg", photo_string="stream_photo"):
        resolution = (800, 608)
        logger.info("Initializing camera...")
        self.vs = PiVideoStream(resolution=resolution, framerate=30).start()
        self.flip = flip  # Flip frame vertically
        self.file_type = file_type  # image type i.e. .jpg
        self.photo_string = photo_string  # Name to save the photo
        self.indicator_state = 0

        self.width, self.height = resolution
        time.sleep(2.0)
        logger.info("Camera initialized successfully.")

        # Generate a simple error image for fallback
        self.error_image = self.create_error_image()

    def __del__(self):
        logger.info("Stopping camera...")
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            logger.debug("Flipping frame.")
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        try:
            frame = self.flip_if_needed(self.vs.read()).copy()
            #logger.debug("Frame read from camera.")
            self.indicator_state = (self.indicator_state + 1) % 10
            gray_value = int(self.indicator_state * 255 / 9)  # Map to [0, 255]

            frame[self.height - 10:self.height, 0:10] = [gray_value, gray_value, gray_value]

            ret, jpeg = cv.imencode(self.file_type, frame)
            #logger.debug("Frame encoded to JPEG format.")
            return jpeg.tobytes()
        except Exception as e:
            logger.error(f"Error getting frame: {e}")
            raise

    def get_error_frame(self):
        """Return a pre-generated error image if frame capture fails."""
        logger.debug("Returning error image.")
        return self.error_image

    def create_error_image(self):
        """Create a simple error image."""
        error_img = np.zeros((self.height, self.width, 3), np.uint8)
        error_img[:] = (0, 0, 0)  # Black background
        text = "Error loading frame"
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(error_img, text, (50, self.height // 2), font, 1, (255, 255, 255), 2, cv.LINE_AA)
        ret, jpeg = cv.imencode(self.file_type, error_img)
        return jpeg.tobytes()

    # Take a photo, called by camera button
    def take_picture(self):
        try:
            frame = self.flip_if_needed(self.vs.read())
            logger.info("Taking a picture.")
            ret, image = cv.imencode(self.file_type, frame)
            today_date = datetime.now().strftime("%m%d%Y-%H%M%S")  # get current time
            logger.info(f"Picture taken at {today_date}.")
            return f"bbcam_{today_date}", image.tobytes()
        except Exception as e:
            logger.error(f"Error taking picture: {e}")
            raise
