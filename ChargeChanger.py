import psutil
import requests
import request_tokens

def plugRequest(switchState):
    json = {"method":"passthrough", "params": {"deviceId": request_tokens.deviceId, "requestData": "{\"system\":{\"set_relay_state\":{\"state\": "+ str(switchState) +" }}}" }}
    # print(json)
    requests.post(f"https://eu-wap.tplinkcloud.com/?token={request_tokens.token}", json = json)
    print("Request Sent...")
    
battery = psutil.sensors_battery()
pluggedIn = battery.power_plugged
currentCharge = battery.percent
if pluggedIn==False: chargeState="Not Plugged In"
else: chargeState="Plugged In"
print( f"{str(currentCharge)}% | {chargeState}")

if (pluggedIn and currentCharge == 100):
    # unplug laptop
    print("Turning off plug")
    plugRequest(0)
elif (not pluggedIn and currentCharge < 70):
    # plug laptop in
    print("Turning on plug")
    plugRequest(1)