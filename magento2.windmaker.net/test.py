import os
import datetime
import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select

class Example(unittest.TestCase):

    def setUp(self):

        current_location = os.getcwd()
        self.img_folder = current_location + '/images/'
        self.dt_format = '%Y%m%d_%H%M%S'
        self.photo_id=0;

        if not os.path.exists(self.img_folder):
            os.mkdir(self.img_folder)

        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        self.driver =webdriver.Chrome( chrome_options=options)
        self.driver.get('https://magento2.windmaker.net/')

        self.driver.set_window_size(1920, 1080)

    def take_snapshot(self):

        cdt = datetime.datetime.fromtimestamp(time.time()).strftime(self.dt_format)
        picture = "{}{:02d}_{}.png".format(self.img_folder,self.photo_id, cdt)
        self.driver.save_screenshot(picture)

        self.photo_id += 1

    def test_something(self):

        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "ui-id-4")))

        menu_bar_women_button=self.driver.find_element_by_id("ui-id-4")
        ActionChains(self.driver).move_to_element(menu_bar_women_button).perform()
        menu_bar_women_button.click()

        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, "info")))

        self.take_snapshot()

        items_to_shop = self.driver.find_elements_by_class_name('product-item-info')

        for ii in items_to_shop:

            self.driver.execute_script("arguments[0].scrollIntoView();", ii)
            ActionChains(self.driver).move_to_element(ii).perform()
            self.take_snapshot()

        items_to_shop[0].click() #product-addtocart-button

        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "product_addtocart_form")))

        self.take_snapshot()

        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, "product-options-bottom")))

        self.take_snapshot()

        # Choose size and color
        self.driver.find_element_by_id("option-label-size-141-item-172").click()

        self.take_snapshot()

        self.driver.find_element_by_id("option-label-color-93-item-50").click()

        self.take_snapshot()

        self.driver.find_element_by_id("product-addtocart-button").click()

        WebDriverWait(self.driver, 30).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "messages"), "You added Deirdre Relaxed-Fit Capri to your shopping cart."))

        self.take_snapshot()

        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, "counter-number")))

        self.driver.find_element_by_class_name("counter-number").click()

        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "top-cart-btn-checkout")))

        self.take_snapshot()

        self.driver.find_element_by_id("top-cart-btn-checkout").click()

        self.driver.find_element_by_id("checkout-loader").click()

        self.take_snapshot()

        # Checkout

        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, "step-title")))
        email = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.ID, "customer-email")))
        firstname = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.NAME, "firstname")))
        lastname = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.NAME, "lastname")))
        street = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.NAME, "street[0]")))
        city = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.NAME, "city")))
        country = Select(WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.NAME, "country_id"))))
        province = Select(WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.NAME, "region_id"))))
        telephone = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.NAME, "telephone")))
        postcode = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.NAME, "postcode")))
        shipping = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.NAME, "ko_unique_2")))#Fails

        shipping_buttons = self.driver.find_elements_by_xpath("//button")
        nextStepButton = None

        for button in shipping_buttons:

            if button.text == "Next":

                nextStepButton = button

        self.take_snapshot()

        cdt = datetime.datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")

        email.send_keys("user_{}@test.com".format(cdt))

        self.take_snapshot()

        firstname.send_keys("jhon_{}".format(cdt))

        self.take_snapshot()

        lastname.send_keys("Doe")

        self.take_snapshot()

        street.send_keys("Wrong street {}".format(cdt))

        self.take_snapshot()

        city.send_keys("Bone City")

        self.take_snapshot()

        country.select_by_value('ES')

        self.take_snapshot()

        province.select_by_value("130")

        self.take_snapshot()

        telephone.send_keys("666666666")

        self.take_snapshot()

        postcode.send_keys("15001")

        self.take_snapshot()

        shipping.click()

        self.take_snapshot()


        nextStepButton.click()

        self.take_snapshot()
        #self.driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(10)
        nextStepButton.click()

        self.take_snapshot()
        self.driver.execute_script("window.scrollTo(0, 0)")

        time.sleep(5)
        placeOrder = self.driver.find_element_by_xpath('//*[@title="Place Order"]')

        self.take_snapshot()

        action = ActionChains(self.driver)
        action.move_to_element(placeOrder)
        action.click()
        action.perform()

        self.take_snapshot()

        EC.text_to_be_present_in_element((By.CLASS_NAME, "base"), "Thank you for your purchase!")

        self.take_snapshot()

    def tearDown(self):

        self.driver.quit()


if __name__ == "__main__":

    unittest.main(verbosity=1)
