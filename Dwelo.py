from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from helper_functions import rand_sleep
from pathlib import Path
import subprocess
import time
import schedule
import pickle
from datetime import datetime


class Dwelo:
    def __init__(self):
        self.base_url = 'https://web.dwelo.com/'
        self.current_dir = Path(__file__).parent.absolute()
        self.driver_pkl_file_path = self.current_dir / "driver_path.pkl"
        self.cookies_pkl_file_path = self.current_dir / "cookies.pkl"
        if self.driver_pkl_file_path.exists():
            self.load_driver_path()

    def launch_chrome(self, headless = False):
        """Launches a chrome browser."""
        if headless:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox") # linux only
            chrome_options.add_argument("--headless")
            self.driver = webdriver.Chrome(self.driver_path, options = chrome_options)
        else:
            self.driver = webdriver.Chrome(self.driver_path)

    def find_element(self, x_path):
        """Returns the element if it exists. If it does not exist, it waits 2 seconds and tries again."""
        if self.exists_by_xpath(x_path):
            return self.driver.find_element_by_xpath(x_path)
        else:
            time.sleep(2)
            return self.driver.find_element_by_xpath(x_path)

    def exists_by_xpath(self, x_path):
        """Returns bool on if the element given exists"""
        try:
            self.driver.find_element_by_xpath(x_path)
        except NoSuchElementException:
            return False
        return True

    def open(self, url):
        url = self.base_url + url
        self.driver.get(url)

    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url

    def hover(self, x_path):
        element = self.find_element(x_path)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()

    def enter_email(self, email):
        self.find_element("""/html/body/div[1]/div[1]/div[2]/div/div/form/input[1]""").send_keys(email)

    def enter_password(self, password):
        self.find_element("""/html/body/div[1]/div[1]/div[2]/div/div/form/input[2]""").send_keys(password)

    def click_login_button(self):
        self.find_element("""/html/body/div[1]/div[1]/div[2]/div/div/form/div/button""").click()

    def login(self):
        """Different method of logging in."""
        login_id, password = login_creds()
        self.open("login")
        rand_sleep()
        self.enter_email(login_id)
        rand_sleep()
        self.enter_password(password)
        rand_sleep()
        self.click_login_button()
        time.sleep(5)
        self.open("")

    def find_file(self, file_name):
        command = ['locate'+ ' ' + file_name]
        output = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]
        output = output.decode()
        self.search_results = output.split('\n')
        return self.search_results

    def save_driver_path(self):
        """Saves the driver path string object as a pkl file."""
        print("Trying to find the path to your chromedriver. See the list below:")
        try:
            self.find_file('chromedriver')
            for path in self.search_results:
                print(path)
        except:
            print('Search function to find a chromedriver on your system failed. This search only works on linux.')
        self.driver_path = input("What is the path to your chromedriver?\n")
        pickle.dump( self.driver_path , open(self.driver_pkl_file_path,"wb"))

    def load_driver_path(self):
        """Loads the driver path string object from the pkl file."""
        self.driver_path = pickle.load(open(self.driver_pkl_file_path, "rb"))

    def load_cookies(self):
        """Loads cookies from the pickle cookies file. Browser needs to exist already"""
        self.open("")
        cookies = pickle.load(open(self.cookies_pkl_file_path, "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.open("")
        
    def save_cookies(self):
        """Saves the current cookies. Use this after you log in for the first time."""
        self.open("")
        pickle.dump( self.driver.get_cookies() , open(self.cookies_pkl_file_path,"wb"))
                    
    def save_url(self):
        """Saves the url page that the user needs to go to."""
        pass

    def click_cool_button(self):
        self.find_element("""/html/body/div[1]/div[1]/div[2]/div[3]/div[2]/div[2]/div/div/dw-thermostat-selector/div/div[2]/div/button[2]""").click()

    def current_set_temp(self): #HERE
        """Returns the cool temp that the system is already sent to"""
        self.click_cool_button()
        time.sleep(1)
        set_temp_element = self.find_element("""/html/body/div[1]/div[1]/div[2]/div[3]/div[2]/div[2]/div/div/dw-thermostat-selector/div/div[1]/span""")
        self.set_temp_int = int(set_temp_element.text[:2])
        return self.set_temp_int

    def temp_difference(self):
        self.temp_diff_int = self.current_set_temp() - self.desired_temp
        return self.temp_diff_int

    def click_up_button(self):
        self.find_element("""/html/body/div[1]/div[1]/div[2]/div[3]/div[2]/div[2]/div/div/dw-thermostat-selector/div/div[1]/div/button[1]""").click()

    def click_down_button(self):
        self.find_element("""/html/body/div[1]/div[1]/div[2]/div[3]/div[2]/div[2]/div/div/dw-thermostat-selector/div/div[1]/div/button[2]""").click()

    def current_time(self):
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def set_cool(self, desired_temp):
        """Sets the ac to the desired temp on cool."""
        self.desired_temp = desired_temp
        time.sleep(1) # Time for the page to load
        self.click_cool_button() # Ensures that cool is on
        time.sleep(2.5) # Time for the set temp to change to numbers
        # Browser clicks on the up or down temp arrow until the set temp is the desired temp
        for num in range(abs(self.temp_difference())): # temp_difference function initilizes the self.set_temp variable
            if self.set_temp_int < self.desired_temp: # If set temp is lower than desired
                self.click_up_button()
            elif self.set_temp_int > desired_temp: # If set temp is lower than desired
                self.click_down_button()
            elif self.set_temp_int == desired_temp:
                pass
        print(f"{self.current_time()} | Turned AC to {self.desired_temp}.")
        time.sleep(1)

    def quit(self):
        self.driver.quit()

