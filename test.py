import psutil
import requests
import request_tokens
import csv
import datetime

debugMode = True
action = "None"
statusCode = "None"
    
battery = psutil.sensors_battery()
pluggedIn = battery.power_plugged
currentCharge = battery.percent
if pluggedIn==False: chargeState="Not Plugged In"
else: chargeState="Plugged In"
print( f"{str(currentCharge)}% | {chargeState}")
print(battery)
if (not chargeState):
    print("yes")