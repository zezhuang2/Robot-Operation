import cv2
from pyzbar.pyzbar import decode
from time import sleep
import dill
import time 
import socket
import os
import struct
#from blob_search import *

dill.settings['recurse'] = True
urscript_command = "set_digital_out(1, True)"
# Creates new line
new_line = "\n"
robotIP = "192.168.50.52"
PRIMARY_PORT = 30001
SECONDARY_PORT = 30002
REALTIME_PORT = 30003
PI = 3.1415926
new_line = "\n"

def move_to_center():
    with open(f"C:/Users/ZeZhuang/UR3/Skip_Functions/circle_all_angles.script","rb") as file:
        script = file.read()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((robotIP, PRIMARY_PORT))
        s.sendall(script)
    except BrokenPipeError:
        print("Broken pipe error: unable to send the script.")
    finally:
        s.close()

move_to_center()