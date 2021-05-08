import os
import sys
import datetime
import time
import toml
import telegram
import getopt

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select

class Moniotor():

    def __init__(self, config_file_path):

        self._config, read_error=self._read_config(config_file_path)
        if read_error!="":
            sys.stderr.write(read_error)
            sys.exit(1)
        self.bot = telegram.Bot(token=self._config['telegram']['bot_token'])

    def _read_config(self,config_file_path):

        error = ""
        config = dict()

        if not os.path.isfile(config_file_path):

            error="{} not found or not a file.".format(config_file_path)
            return config,error

        else:

            config = toml.load(config_file_path)

        return config,error

    def notify(self,msg,image=""):

        for chat_id in self._config['telegram']['users_to_notify']:
            self.bot.sendMessage(chat_id=chat_id, text=msg)
        if image!="":
            for chat_id in self._config['telegram']['users_to_notify']:
                self.bot.send_photo(chat_id=chat_id, photo=open(image, 'rb'))

    def setUp(self,url):

        current_location = os.getcwd()
        self.img_folder = current_location + '/images/'
        self.dt_format = '%Y%m%d_%H%M%S'
        self.photo_id=0;

        if not os.path.exists(self.img_folder):
            os.mkdir(self.img_folder)

        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        # Bypass Cloudflare
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities={
                'browserName': 'firefox',
                'javascriptEnabled': True
            }
        )

        self.driver.get(url)


    def take_snapshot(self):

        cdt = datetime.datetime.fromtimestamp(time.time()).strftime(self.dt_format)
        picture = "{}{:02d}_{}.png".format(self.img_folder,self.photo_id, cdt)
        self.driver.save_screenshot(picture)

        self.photo_id += 1
        return picture

    def check_availability(self):

        self.setUp('https://www.amazon.es/Playstation-Consola-PlayStation-5/dp/B08KKJ37F7/')
        time.sleep(5)
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@class='a-color-price a-text-bold']")))

        price=self.driver.find_element_by_class_name("a-color-price").text

        if price!="No disponible.":
            picture=self.take_snapshot()
            self.notify(msg="PS5 seems to be available in Amazon ES.", image=picture)
            self.notify(msg="https://www.amazon.es/Playstation-Consola-PlayStation-5/dp/B08KKJ37F7/")

        self.tearDown()


        self.setUp('https://www.game.es/HARDWARE/CONSOLA/PLAYSTATION-5/CONSOLA-PLAYSTATION-5/183224')
        time.sleep(5)

        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@class='buy--type']")))

        price=self.driver.find_element_by_class_name("buy--type").text

        if price!="PRODUCTO NO DISPONIBLE":
            picture=self.take_snapshot()
            self.notify(msg="PS5 seems to be available in game.es.", image=picture)
            self.notify(msg="https://www.game.es/HARDWARE/CONSOLA/PLAYSTATION-5/CONSOLA-PLAYSTATION-5/183224")

        self.tearDown()

        self.setUp('https://www.carrefour.es/playstation-5-825gb/VC4A-11998176/p')
        time.sleep(5)

        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@class='add-to-cart-button']")))

        price=self.driver.find_element_by_class_name("add-to-cart-button").text

        if price!="Agotado temporalmente":
            picture=self.take_snapshot()
            self.notify(msg="PS5 seems to be available in www.carrefour.es.", image=picture)
            self.notify(msg="https://www.carrefour.es/playstation-5-825gb/VC4A-11998176/p")

        self.tearDown()

        self.setUp('https://www.pccomponentes.com/sony-playstation-5')
        time.sleep(5)

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@class='priceBlock']")))

        price=self.driver.find_element_by_class_name("priceBlock").text
        if price!="No disponible":
            picture=self.take_snapshot()
            self.notify(msg="PS5 seems to be available in PC Componentes", image=picture)
            self.notify(msg="https://www.pccomponentes.com/sony-playstation-5")


        self.tearDown()



        self.setUp('https://www.fnac.es/Consola-PlayStation-5-Videoconsola-Consola/a7724798')
        time.sleep(5)

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@class='f-buyBox-infos']")))

        price=self.driver.find_element_by_class_name("f-buyBox-infos").text
        if price!="Artículo no disponible en web":
            picture=self.take_snapshot()
            self.notify(msg="PS5 seems to be available in FNAC", image=picture)
            self.notify(msg="https://www.pccomponentes.com/sony-playstation-5")


        self.tearDown()


    def tearDown(self):

        self.driver.quit()

def usage():

    usage_text=""
    usage_text+="Wrapper options:\n"
    usage_text+="\n"
    usage_text+="-h --help               Displays this message.\n"
    usage_text+="--config=CONFIG_FILE    Specifies where config file is placed (required).\n"
    usage_text+="--list-sites            List available sites readed from config file.\n"
    usage_text+="--site=SITE_NAME        Launch wrapper on specified site.\n"
    usage_text+="--debug                 Sends debug screeshots.\n"
    print(usage_text)

if __name__ == "__main__":

    config_file = ""
    site = ""
    list_sites=False
    debug=False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "list-sites", "site=" ,"debug", "config="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err,file=sys.stderr)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    for option_name, option_value in opts:
        if option_name in ("-h", "--help"):
            usage()
            sys.exit()
        elif option_name == "--config":
            config_file=option_value
        elif option_name == "--site":
            site = option_value
        elif option_name == "--debug":
            debug = True
        elif option_name == "--list-sites":
            list_sites=True

    if config_file == "":

        print("Wrapper needs a config file.",file=sys.stderr)
        sys.exit(2)

    config_file_path = os.getenv('CONFIG_FILE')
    monitor = Moniotor(config_file_path)
    monitor.check_availability()
