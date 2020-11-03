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
    token = getToken()
    jsonRequest = {"method":"passthrough", "params": {"deviceId": request_tokens.deviceId, "requestData": "{\"system\":{\"set_relay_state\":{\"state\": "+ str(switchState) +" }}}" }}
    # print(jsonRequest)
    request("Plug", jsonRequest, f"https://eu-wap.tplinkcloud.com/?token={token}")

def getToken():
    token = None
    jsonRequest = {"method":"login", "params": {"appType": "Kasa_Android", "cloudUserName": "jliley94@gmail.com", "cloudPassword": request_tokens.userPass, "terminalUUID": "e7e88ca8-3582-4b14-b75b-b0d3d2bf9765" }}
    jsonResponse = request("Token", jsonRequest, "https://wap.tplinkcloud.com")

    if (json.loads(jsonResponse.text)["error_code"] == 0): 
        #No error occurred
        token = json.loads(jsonResponse.text)["result"]["token"]
    return token

def request(requestName, jsonRequest, url):
    response = requests.post(url, json = jsonRequest)
    print(f"{requestName} Request Sent...")
    statusCode = response.status_code
    if (statusCode != 200 or json.loads(response.text)["error_code"] != 0): 
        #Error occurred
        statusCode = "Error: " + json.loads(response.text)["msg"]
    else:
        statusCode = "Success"
    print(statusCode)
    return response


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
elif (not pluggedIn and currentCharge < 65):
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