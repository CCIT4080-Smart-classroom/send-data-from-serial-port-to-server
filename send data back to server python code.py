#Python script to read serial port data from arduino and send them to srever

import time
import requests
import serial


arduino = serial.Serial('COM3', 9600, timeout=1)  #configure serial port
print("Reading data from serial port.....");
time.sleep(2)
arduino.reset_input_buffer() # Delete stale data


def build_payload(data):
    payload = {"student_id": int(data)} # sending data
    return payload


def post_request(payload): # Creates the headers for the HTTP requests
    headers = {"Content-Type": "application/json"}
    req = requests.post("https://api.ccit4080.tylerl.cyou/attendance/checkin", headers=headers, json=payload)
    status = req.status_code
    print("Waitting for data transfer...")
    print(".")
    print("..")
    print("...")
    return True


def main(): 
    line = arduino.readline() # Reading all bytes available bytes till EOL
    if line:
        rxdata = line.decode()   # Converting Byte Strings into unicode strings
        sid = rxdata
        payload = build_payload(sid) #send collected data to cloud as a payload
        print(sid)
        del sid #clear received data
        print("Data transfer started")
        post_request(payload)
        print("Data Successfully sent to server")
        print("==================================")
        print("Reading data from serial port.....")


if __name__ == '__main__':
    while (True):
        main()
        time.sleep(1)
