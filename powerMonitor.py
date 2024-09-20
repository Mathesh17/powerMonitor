import utime
import network
from machine import Pin,ADC
import urequests
import random

wlan=network.WLAN(network.STA_IF)
wlan.active(True)
ssid="Oh"
password="12tony34"
wlan.connect(ssid,password)

def realtimedata():
    reading=0
    analog_value=machine.ADC(26)
    volt=analog_value.read_u16()
    Vout=(volt*3.3)/65535
    Vin=Vout/0.13
    Cin=(Vin/1110)
        
    return {'Voltage1':Vin,'Current1':Cin}
        

firebase_url="https://powermonitor-f4846-default-rtdb.asia-southeast1.firebasedatabase.app"
auth_data={
            "email":"projectpowermonitor@gmail.com",
             "password":"Qwerty@123",
             "returnSecureToken":True
          }
auth_response=urequests.post("https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyCfX34GJkkr5TMBRgnufy283Y67tK6doIU",json=auth_data)
auth_response_data=auth_response.json()
print(auth_response_data)
auth_response.close()
local_id=auth_response_data.get('localId')
print(local_id)

response=urequests.get(firebase_url)
arr = []
i = 0
while(True):
    Data=realtimedata()
    arr.append(Data)
    response=urequests.put(firebase_url + '/val.json',json=Data)
    response.close()
    response=urequests.put(firebase_url + '/'+ str(i) +'/.json',json=Data)
    response.close()
    print(Data)
    i += 1
    utime.sleep(1)
