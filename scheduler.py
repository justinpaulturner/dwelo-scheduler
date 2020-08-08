from Dwelo import Dwelo
import schedule
import time

##################################################################################

d = Dwelo()
d.launch_chrome(headless = True)
d.load_cookies()

schedule.every().day.at("19:30").do(d.set_cool, 66) # Sets AC to 66 degrees at 7:30 PM
schedule.every().day.at("06:30").do(d.set_cool, 73) # Sets AC to 73 degrees at 6:30 AM

while True:
    try:
        time.sleep(1)
        schedule.run_pending()
        time.sleep(1)
    except:
        d.quit()
        time.sleep(1)
        d.launch_chrome()
        time.sleep(1)
        d.load_cookies()
        time.sleep()