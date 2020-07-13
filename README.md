# ChargeChanger
Python script to check battery level and turn on smart plug

### What is this
This solution periodically checks the battery level and charging status of my laptop (utilising windows task scheduler to run the batch file)
- If the laptop needs charging a switch on request is sent to my tp-link plug
- If the laptop is fully charged a switch off request is sent to my tp-link plug

### Requirements 
pip3 install --user psutil
pip install requests

### Note
request_tokens.py has been ommited as it contains tokens for the api connection
```
import os

token = '' # my account token
deviceId = '' # my smart plugs device id
```

### References: 
https://itnerd.space/2017/06/19/how-to-authenticate-to-tp-link-cloud-api/
