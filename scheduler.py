from Dwelo import Dwelo
import schedule
import time

##################################################################################

d = Dwelo()

schedule.every().day.at("19:30").do(d.login_and_set_cool, 66) # Sets AC to 66 degrees at 7:30 PM
schedule.every().day.at("06:30").do(d.login_and_set_cool, 73) # Sets AC to 73 degrees at 6:30 AM
schedule.every().minute.do(d.print_update) # prints a waiting indicator with current time

while True:
    schedule.run_pending()
    time.sleep(1)