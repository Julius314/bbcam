sudo apt-get install -y libatlas-base-dev libjasper-dev libhdf5-dev python3-opencv nginx
sudo mv nginx-default /etc/nginx/sites-available/default
sudo cp bbcam.service /etc/systemd/system/
sudo systemctl enable bbcam
