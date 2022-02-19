from math import e
import time
from datetime import datetime
import pytz
from dateutil import parser
import os


LAST_CHECK_FILE_PATH = "last_check.txt"

if os.path.isfile(LAST_CHECK_FILE_PATH) == False:
    print("Creating last_check.txt")
    with open(LAST_CHECK_FILE_PATH, "w", encoding="utf-8") as f:
        f.write("1970-01-01")

def validateDate(date):
    try:
        print(parser.parse(date))
        return parser.parse(date).strftime('%Y-%m-%d')
    except Exception as e:
        print(e)
        return date

def periodic_task(time_string, timezone_string=None):
    """
    This function is called every minute.
    """
    while True:
        # string to datetime
        try:
            datetime_obj = datetime.strptime(time_string, "%H:%M:%S")
        except:
            try:
                datetime_obj = datetime.strptime(time_string, "%H:%M")
            except:
                try:
                    datetime_obj = datetime.strptime(time_string, "%H")
                except:
                    return False

        if timezone_string is not None:
            timezone = pytz.timezone('Europe/Berlin')
            current_time = datetime.now()
            current_time = current_time.replace(tzinfo=timezone)
        else:
            current_time = datetime.now()
        

        provided_hour = datetime_obj.hour
        provided_minute = datetime_obj.minute

   
        print("Periodic task is running")
        print(current_time)

        if current_time.hour == provided_hour and current_time.minute == provided_minute:
            with open(LAST_CHECK_FILE_PATH, "r", encoding="utf-8") as f:
                file_data = f.read()
            try:
                last_check = validateDate(file_data)
                if last_check == current_time.strftime('%Y-%m-%d'):
                    print("Already checked today")
                else:
                    # Work will be done here
                    # send_bulk_messages())
                    print(":")

                    with open(LAST_CHECK_FILE_PATH, "w", encoding="utf-8") as f:
                        f.write(current_time.strftime('%Y-%m-%d'))
                    print("Task done")
            except:
                if file_data.strip() == "":
                    last_check = "1970-01-01"
                
                with open(LAST_CHECK_FILE_PATH, "w", encoding="utf-8") as f:
                    f.write(last_check)            
        else:
            print("Not yet")
            time.sleep(60)
            current_time = datetime.now()

        time.sleep(30)

time_string = input("Enter the time to check in 24 hour format (HH:MM:SS): ")
periodic_task(time_string, "Asia/Dhaka")
# validateDate("1")