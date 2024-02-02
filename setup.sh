sudo apt-get install -y libatlas-base-dev libjasper-dev libhdf5-dev python3-opencv
sudo cp bbcam.service /etc/systemd/system/
sudo systemctl enable bbcam
