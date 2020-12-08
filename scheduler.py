from Dwelo import Dwelo
import schedule
import time

##################################################################################

d = Dwelo()

schedule.every().day.at("22:30").do(d.login_and_lock_door) # Locks door at 10:30 PM
schedule.every().day.at("06:30").do(d.login_and_set_cool, 75) # Sets AC to 73 degrees at 6:30 AM
schedule.every().minute.do(d.print_update) # prints a waiting indicator with current time

while True:
    schedule.run_pending()
    time.sleep(1)