import psutil
import requests
import request_tokens
import csv
import datetime
import json

debugMode = True
action = "No Action"
statusCode = "No Request Made"

def plugRequest(switchState):
    # print(json)
    event = "Laptop_battery_on" if (switchState) else "Laptop_battery_off"
    response = requests.post(f"https://maker.ifttt.com/trigger/{event}/with/key/{request_tokens.webhookId}")
    print("Request Sent...")
    statusCode = response.status_code
    if (statusCode != 200): 
        #Error occurred
        statusCode = "Error: "
    else:
        statusCode = "Success"

    
battery = psutil.sensors_battery()
pluggedIn = battery.power_plugged
currentCharge = battery.percent
if pluggedIn==False: chargeState="Not Plugged In"
else: chargeState="Plugged In"
print( f"{str(currentCharge)}% | {chargeState}")

if (pluggedIn and currentCharge == 100):
    # unplug laptop
    print("Turning off plug")
    action = "Turn Off"
    plugRequest(0)
elif (not pluggedIn and currentCharge < 70):
    # plug laptop in
    print("Turning on plug")
    action = "Turn On"
    plugRequest(1)

if (debugMode):
    print("Debugging Mode On - writing to log file")
    dateTime = datetime.datetime.now()

    with open('log.csv', mode='a') as log_file:
        log_writer = csv.writer(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Date,    Time,    Battery Level,   ChargeState,    Action,    Status Code
        log_writer.writerow([f"{dateTime.day}/{dateTime.month}/{dateTime.year}", dateTime.strftime("%X"), f"{str(currentCharge)}%", chargeState, action, statusCode])