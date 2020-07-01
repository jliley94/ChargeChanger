import psutil
import requests
import request_tokens
import csv
import datetime

debugMode = True
action = "None"
statusCode = "None"

def plugRequest(switchState):
    json = {"method":"passthrough", "params": {"deviceId": request_tokens.deviceId, "requestData": "{\"system\":{\"set_relay_state\":{\"state\": "+ str(switchState) +" }}}" }}
    # print(json)
    response = requests.post(f"https://eu-wap.tplinkcloud.com/?token={request_tokens.token}", json = json)
    print("Request Sent...")
    statusCode = response.status_code

    
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