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

    def show_sites(self):

        for site in self._config['sites'].keys():
            print(site)

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

    def setCookie(self,name,value):

        self.driver.add_cookie({"name": name, "value": value});

    def take_snapshot(self):

        cdt = datetime.datetime.fromtimestamp(time.time()).strftime(self.dt_format)
        picture = "{}{:02d}_{}.png".format(self.img_folder,self.photo_id, cdt)
        self.driver.save_screenshot(picture)

        self.photo_id += 1
        return picture

    def check_availability(self,site,debug):

        
        site_info = self._config['sites'][site]
        self.setUp(site_info['url'])
        if 'cookies' in site_info.keys():
            for cookie_name in site_info['cookies'].keys():
                self.setCookie(cookie_name,site_info['cookies'][cookie_name])

        time.sleep(5)

        if debug:
            picture=self.take_snapshot()
            self.notify(msg="Debug - {}.".format(site_info['name']), image=picture)

        try:
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@class='{}']".format(site_info['nameof_element_to_find']))))

        except:
            print("{} failed.".format(site_info['name']),file=sys.stderr)
            self.tearDown()
            sys.exit(1)

        price=self.driver.find_element_by_class_name(site_info['nameof_element_with_price']).text

        if price!=site_info['not_available_text']:
            picture=self.take_snapshot()
            self.notify(msg="PS5 seems to be available in {}.".format(site_info['name']), image=picture)
            self.notify(msg=site_info['url'])

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

    monitor = Moniotor(config_file)

    if list_sites:
        monitor.show_sites()
    else:
        if site == "":
            print("Wrapper needs a config file.",file=sys.stderr)
            sys.exit(2)
        else:
            monitor.check_availability(site,debug)
