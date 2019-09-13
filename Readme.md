# Bone Shaker

## Requirements

Install Selenium's Python Module

```bash
sudo apt-get install python3-selenium
```

## Testing  with Selenium

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

## Testing Magento2 using Chrome

Run test script

```
cd magento2.windmaker.net && python3 test.py
/usr/lib/python3/dist-packages/selenium/webdriver/chrome/webdriver.py:50: DeprecationWarning: use options instead of chrome_options
  warnings.warn('use options instead of chrome_options', DeprecationWarning)
.
----------------------------------------------------------------------
Ran 1 test in 36.513s

OK
```
