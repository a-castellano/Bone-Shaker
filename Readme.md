# Bone Shaker

## Requirements

Install Selenium's Python Module

```bash
sudo apt-get install python3-selenium
```

## Testing Selenium

Run selenium

```bash
docker run -d -p 4444:4444 --name selenium-hub selenium/hub
docker run -d --link selenium-hub:hub selenium/node-chrome
docker run -d --link selenium-hub:hub selenium/node-firefox
```

Run test script

```
cd Examples/  && python3 softwaretester_example.py
```
