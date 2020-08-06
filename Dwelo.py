from selenium import webdriver
import  getpass
import time
import schedule
from login_creds import login_creds
from helper_functions import rand_sleep
import os.path
from datetime import datetime
import pickle


class Dwelo:
    def __init__(self):
        self.base_url = 'https://web.dwelo.com/'
        self.DRIVER_PATH = "/home/justin/program_files/chromedriver"
        
    def launch_chrome(self, headless = False):
        """Launches a chrome browser."""
        if headless:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox") # linux only
            chrome_options.add_argument("--headless")
            self.driver = webdriver.Chrome(self.DRIVER_PATH, options = chrome_options)
        else:
            self.driver = webdriver.Chrome(self.DRIVER_PATH)
        
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
        login_id, password = login_creds()
        self.open("login")
        rand_sleep()
        self.enter_email(login_id)
        rand_sleep()
        self.enter_password(password)
        rand_sleep()
        self.click_login_button()
        
    def load_cookies(self, user = 0): 
        """Loads cookies from the pickle cookies file. Browser needs to exist already"""
        user = login_creds()[0]
        self.open("")
        cookies = pickle.load(open(f"cookies_{user.lower()}.pkl", "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.open("")
        
    def save_cookies(self): # HERE
        """Saves the current cookies."""
        self.open("")
        user = login_creds()[0].lower()
        pickle.dump( self.driver.get_cookies() , open(f"cookies_{user}.pkl","wb"))
        
    def click_cool_button(self):
        self.find_element("""/html/body/div[1]/div[1]/div[2]/div[3]/div[2]/div[2]/div/div/dw-thermostat-selector/div/div[2]/div/button[2]""").click()
        
    def current_set_temp(self): #HERE
        """Returns the cool temp that the system is already sent to"""
        try:
            set_temp_element = self.find_element("""/html/body/div[1]/div[1]/div[2]/div[3]/div[2]/div[2]/div/div/dw-thermostat-selector/div/div[1]/span""")
            self.set_temp_int = int(set_temp_element.text[:2])
            return self.set_temp_int
        except:
            rand_sleep()
            self.click_cool_button()
            rand_sleep()
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
        
    def set_ac(self, desired_temp):
        time.sleep(5) # Time for the page to load
        self.open("units/278070?community=180")
        time.sleep(5)
        self.click_cool_button()
        time.sleep(5) # Time for the set temp to change to numbers
        # Browser clicks on the up or down temp arrow until the set temp is the desired temp
        for num in range(abs(self.temp_difference())):
            if self.set_temp < self.desired_temp: # If set temp is lower than desired
                self.click_up_button()
            elif set_temp > desired_temp: # If set temp is lower than desired
                self.click_down_button()
            elif set_temp == desired_temp:
                pass
        print(f"Turned AC to {self.desired_temp} at {self.current_time()}")
        time.sleep(5)
        
    def quit(self):
        self.driver.quit()
        
    def initiate_driver_set_ac(self,desired_temp):
        try:
            self.set_ac(desired_temp)
            self.quit()
        except Exception as e:
            print(e)
    

##################################################################################

# Set schedule to run
# schedule.every().minute.do(initiate_driver_set_ac, 65) # Test
# schedule.every().day.at("20:30").do(initiate_driver_set_ac, 66) # Sets AC to 66 degrees at 8:30 PM
# schedule.every().day.at("06:30").do(initiate_driver_set_ac, 72) # Sets AC to 72 degrees at 6:30 AM

# while True:
#     schedule.run_pending()
#     time.sleep(1)