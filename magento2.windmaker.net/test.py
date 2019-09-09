import os
import datetime
import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class Example(unittest.TestCase):

    def setUp(self):

        current_location = os.getcwd()
        self.img_folder = current_location + '/images/'

        if not os.path.exists(self.img_folder):
            os.mkdir(self.img_folder)


        self.driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities={
                'browserName': 'chrome',
                'javascriptEnabled': True
            }
        )

        self.driver.set_window_size(1920, 1080)
        self.driver.get('https://magento2.windmaker.net/')


    def test_something(self):

        dt_format = '%Y%m%d_%H%M%S'

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "ui-id-4")))
        cdt = datetime.datetime.fromtimestamp(time.time()).strftime(dt_format)

        picture = self.img_folder + cdt + '.png'
        self.driver.save_screenshot(picture)

        menu_bar_women_button=self.driver.find_element_by_id("ui-id-4")
        ActionChains(self.driver).move_to_element(menu_bar_women_button).perform()
        menu_bar_women_button.click()

        products_grid_grid=WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "info")))

        cdt = datetime.datetime.fromtimestamp(time.time()).strftime(dt_format)

        picture = self.img_folder + cdt + '.png'
        self.driver.save_screenshot(picture)

        time.sleep(3)

        items_to_shop = self.driver.find_elements_by_class_name('product-item-info')
        for ii in items_to_shop:
            self.driver.execute_script("arguments[0].scrollIntoView();", ii)
            ActionChains(self.driver).move_to_element(ii).perform()

            cdt = datetime.datetime.fromtimestamp(time.time()).strftime(dt_format)

            picture = self.img_folder + cdt + '.png'
            self.driver.save_screenshot(picture)

        items_to_shop[0].click() #product-addtocart-button

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "product_addtocart_form")))

        cdt = datetime.datetime.fromtimestamp(time.time()).strftime(dt_format)
        picture = self.img_folder + cdt + '.png'
        self.driver.save_screenshot(picture)

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "product-options-bottom")))

        cdt = datetime.datetime.fromtimestamp(time.time()).strftime(dt_format)
        picture = self.img_folder + cdt + '.png'
        self.driver.save_screenshot(picture)

        # Choose size and color

    def tearDown(self):

        self.driver.quit()


if __name__ == "__main__":

    unittest.main(verbosity=1)
