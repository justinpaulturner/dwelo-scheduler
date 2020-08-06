from selenium import webdriver
import  getpass
import time
import schedule
from login_creds import login_id, password

def set_cool(desired_temp = 68):
    # Signs into dwelo
    ## Checks the system username to state the selenium driver location (I have two computers I go back and forth with)
    if getpass.getuser() == 'Justin_Turner':
        DRIVER_PATH = "/Users/Justin_Turner/opt/selenium_drivers/chromedriver"
    elif getpass.getuser() == "justin":
        DRIVER_PATH = "/home/justin/program_files/chromedriver"

    driver = webdriver.Chrome(DRIVER_PATH)
    login_url = "https://web.dwelo.com/login"

    # Browser logs into dwelo or has user do it while it waits. 
    try:
        driver.get(login_url) # Visit login URL
        time.sleep(1)
        login_element = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div/form/input[1]")
        login_element.send_keys(login_id())
        time.sleep(1)
        password_element = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div/form/input[2]")
        password_element.send_keys(password())
        time.sleep(1)
        button_to_log_in_element = driver.find_element_by_xpath("""/html/body/div[1]/div[1]/div[2]/div/div/form/div/button""")
        button_to_log_in_element.click()
    except:
        print("Error logging in")
        driver.quit()

    # Starts clicking
    try:

        time.sleep(10)

        off_button = driver.find_element_by_xpath("""/html/body/div[1]/div[1]/div[2]/div[3]/div[2]/div[2]/div/div/dw-thermostat-selector/div/div[2]/div/button[1]""")
        off_button.click()

        cool_button = driver.find_element_by_xpath("""/html/body/div[1]/div[1]/div[2]/div[3]/div[2]/div[2]/div/div/dw-thermostat-selector/div/div[2]/div/button[2]""")
        cool_button.click()

        time.sleep(5) # Time for the set temp to change to numbers

        set_temp_element = driver.find_element_by_xpath("""/html/body/div[1]/div[1]/div[2]/div[3]/div[2]/div[2]/div/div/dw-thermostat-selector/div/div[1]/span""")
        set_temp = int(set_temp_element.text[:2])
        temp_difference = set_temp - desired_temp
        # Browser clicks on the up or down temp arrow until the set temp is the desired temp
        for num in range(abs(temp_difference)):
            if set_temp < desired_temp: # If set temp is lower than desired
                up_button = driver.find_element_by_xpath("""/html/body/div[1]/div[1]/div[2]/div[3]/div[2]/div[2]/div/div/dw-thermostat-selector/div/div[1]/div/button[1]""")
                up_button.click()
            elif set_temp > desired_temp: # If set temp is lower than desired
                down_button = driver.find_element_by_xpath("""/html/body/div[1]/div[1]/div[2]/div[3]/div[2]/div[2]/div/div/dw-thermostat-selector/div/div[1]/div/button[2]""")
                down_button.click()
            elif set_temp == desired_temp:
                pass
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")  
        print(f"Turned AC to {desired_temp} at {current_time}")
        time.sleep(5)
        driver.quit()
    
    except:
        driver.quit()
        
def turn_ac_off():
    # Signs in
    ## Checks the system username to state the selenium driver location (I have two computers I go back and forth with)
    if getpass.getuser() == 'Justin_Turner':
        DRIVER_PATH = "/Users/Justin_Turner/opt/selenium_drivers/chromedriver"
    elif getpass.getuser() == "justin":
        DRIVER_PATH = "/home/justin/program_files/chromedriver"

    driver = webdriver.Chrome(DRIVER_PATH)
    login_url = "https://web.dwelo.com/login"

    login_id = "justin@justinpturner.com"
    password = "#4bgGGnxYYa!V4Z"

    # Browser logs into dwelo or has user do it while it waits. 
    try:
        driver.get(login_url) # Visit login URL
        time.sleep(1)
        login_element = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div/form/input[1]")
        login_element.send_keys(login_id)
        time.sleep(1)
        password_element = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div/form/input[2]")
        password_element.send_keys(password)
        time.sleep(1)
        button_to_log_in_element = driver.find_element_by_xpath("""/html/body/div[1]/div[1]/div[2]/div/div/form/div/button""")
        button_to_log_in_element.click()
        
    except:
        input("Error logging in")
        driver.quit()

    # Starts clicking

    time.sleep(5)
    
    try:
        off_button = driver.find_element_by_xpath("""/html/body/div[1]/div[1]/div[2]/div[3]/div[2]/div[2]/div/div/dw-thermostat-selector/div/div[2]/div/button[1]""")
        off_button.click()
        
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")  
        print(f"Turned AC off at {current_time}")
        
        time.sleep(5)
        driver.quit()
        
    except:
        driver.quit()
        print("Error when turning AC off")

##################################################################################

# Set schedule to run

schedule.every().day.at("20:30").do(set_cool, 66) # Sets AC to 66 degrees at 8:30 PM
schedule.every().day.at("06:30").do(set_cool, 72) # Sets AC to 72 degrees at 6:30 AM

while True:
    schedule.run_pending()
    time.sleep(1)