#Python script to read serial port data and send them to UBIDOTS cloud
import time
import requests
import math
import random
import serial
TOKEN = "BBFF-ietNSqNZWKDcl7MsoIgp7YKYORLz9E"  # Put your TOKEN here
DEVICE_LABEL = "My_PC"  # Put your device label here 
VARIABLE_LABEL_1 = "student number"  # Put your first variable label here


#configure serial port
arduino = serial.Serial('COM3', 9600, timeout=1)
print("Reading data from serial port.....");
time.sleep(2)
arduino.reset_input_buffer() # Delete any stale data.

def build_payload(variable_1, data):
    # Creates two random values for sending data
    value_1 = int(data)
    payload = {variable_1: value_1}
    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    #print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("Device ID updated...wait for data transfer")
    return True


def main():
# Reading all bytes available bytes till EOL
    line = arduino.readline() 
    if line:
        # Converting Byte Strings into unicode strings
        rxdata = line.decode()  
        # Converting Unicode String into integer
        #num = int(rxdata) 
        #print(num)
        tmp = rxdata
        
        #send collected data to cloud as a payload
        payload = build_payload(VARIABLE_LABEL_1,tmp)
        print(tmp)
        del tmp #clear received data

        print("Data transfer started")
        post_request(payload)
        print("Data Successfully sent to cloud")
        print("\nReading data from serial port.....");


if __name__ == '__main__':
    while (True):
        main()
        time.sleep(1)
