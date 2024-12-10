import cv2
from pyzbar.pyzbar import decode
from time import sleep
import dill
import time 
import socket


dill.settings['recurse'] = True

# initialize variables
robotIP = "192.168.50.53"
PRIMARY_PORT = 30001
SECONDARY_PORT = 30002
REALTIME_PORT = 30003

PI = 3.1415926
urscript_command = "set_digital_out(1, True)"
new_line = "\n"
run_port = 29999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((robotIP, run_port))

cap = cv2.VideoCapture(0)
start_time = time.time()
duration = 3  # seconds

while True:


    # Capture frame-by-frame
    ret, frame = cap.read()

    # If frame is captured correctly, proceed
    if not ret:
        print("Failed to grab frame")
        break

    # Decode the QR codes in the frame
    qr_codes = decode(frame)
    #time.sleep(5)
    for qr_code in qr_codes:
        # Decode the QR code data
        qr_data = qr_code.data.decode('utf-8')
        print(f"Decoded QR code data: {qr_data}")

        # Write the QR data to a file
        with open("qr_data.txt", "w") as file:
            file.write(qr_data)

    # Display the frame with the rectangle and data
    cv2.imshow('QR Code Scanner', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if time.time() - start_time > duration:
        print("3 seconds have passed. Stopping the camera.")
        break


cap.release()
cv2.destroyAllWindows()

with open("qr_data.txt", "r") as file:
        qr_data = file.read()

print(f"QR code data from file: {qr_data}")
commands = f"load {qr_data}\n"

print(qr_data)

s.send((commands).encode())
response = s.recv(1024).decode('utf-8')
print(f"Load program response: {response}")
s.send(("programstate"+"\n").encode())
response = s.recv(1024).decode('utf-8')
print(f"programstate response: {response}")
s.send("unlock protective stop\n".encode())
response = s.recv(1024).decode('utf-8', errors='ignore')
print(f"Unlock protective stop response: {response}")

s.send(("safetystatus"+"\n").encode())
response = s.recv(1024).decode('utf-8', errors='ignore')
print(f"Safety status response: {response}")
s.send("robotmode\n".encode())
response = s.recv(1024).decode('utf-8', errors='ignore')
print(f"Robot mode response: {response}")

s.send(("play"+"\n").encode())
response = s.recv(1024).decode('utf-8')
print(f"Play program response: {response}")

s.close()
    
time.sleep(10)



#send_urscript_command("movej([1.57, -1.57, 1.57, -1.57, 1.57, 0], a=0.5, v=0.5)")
#send_urscript_command("load /programs/clean.urp")
#send_urscript_command("play")