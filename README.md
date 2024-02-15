# BBCam

Code to operate a Raspberry Pi Zero with a NoIR camera. Uses flask to serve the videostream and take a picture.

The `sys` folder includes files to run configure nginx to reverse proxy traffic from port `80` to `5555`, and to create a linux service to run the server on startup.

## Setup

- while inside the `sys` folder, run the `setup.sh` script
- install python dependencies (`pip install -r requirements.txt`)
- reboot your system (`sudo reboot now`)
