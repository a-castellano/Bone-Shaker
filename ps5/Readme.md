# PS5 Availability in multiple online shops

Simple wrapper that checks Playstation 5 Availability un various online shops.

## Requirements

Install docker:
```
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker $USER
```


Create virtaulenv and install Requirements:
```
sudo apt-get install python3-pip python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements
```

Preapare selenium hub and firefox container:
```
docker run -d -p 4444:4444 --name selenium-hub selenium/hub
docker run -d --link selenium-hub:hub selenium/node-firefox
```

Run wrapper
```
CONFIG_FILE=/location_of/config.toml python wrapper.py
```
