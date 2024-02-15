# install dependencies
sudo apt-get install -y libatlas-base-dev libjasper-dev libhdf5-dev python3-opencv nginx
# configure nginx to route web traffic to port where flask runs
sudo cp nginx-default /etc/nginx/sites-available/default
# configure service
sudo cp bbcam.service /etc/systemd/system/
# start service on startup
sudo systemctl enable bbcam
