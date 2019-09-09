import os
import datetime
import time
import unittest
from selenium import webdriver


class Example(unittest.TestCase):

    def setUp(self):

        self.driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities={
                'browserName': 'firefox',
                'javascriptEnabled': True
            }
        )

        self.driver.get('http://softwaretester.info/')

    def test_something(self):

        dt_format = '%Y%m%d_%H%M%S'
        cdt = datetime.datetime.fromtimestamp(time.time()).strftime(dt_format)
        current_location = os.getcwd()
        img_folder = current_location + '/images/'

        if not os.path.exists(img_folder):
            os.mkdir(img_folder)

        picture = img_folder + cdt + '.png'
        self.driver.save_screenshot(picture)

    def tearDown(self):

        self.driver.quit()


if __name__ == "__main__":

    unittest.main(verbosity=1)
