
import dill
import socket
import time 
from time import sleep
import ast
#from blob_search import *
# initialize variables
robotIP = "192.168.50.52"
PRIMARY_PORT = 30001
SECONDARY_PORT = 30002
REALTIME_PORT = 30003

dill.settings['recurse'] = True
# URScript command being sent to the robot
urscript_command = "set_digital_out(1, True)"

# Creates new line
new_line = "\n"

def send_urscript_command(command: str):
    try:
        # Create a socket connection with the robot IP and port number defined above
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((robotIP, PRIMARY_PORT))

        # Appends new line to the URScript command (the command will not execute without this)
        command = command+new_line
        
        # Send the command
        s.sendall(command.encode('utf-8'))
        
        # Close the connection
        s.close()

    except Exception as e:
        print(f"An error occurred: {e}")

#with open("part_position.txt", "r") as file:
#    Robot_Posture = file.read()
#    print(f"part postion: {Robot_Posture}")

#Robot_Posture = ast.literal_eval(Robot_Posture)

#print(Robot_Posture)

#theta_str = f"[{Robot_Posture[0]}, {Robot_Posture[1]}, {Robot_Posture[2]}, {Robot_Posture[3]}, {Robot_Posture[4]}, {Robot_Posture[5]}]"
#print(theta_str)
#send_urscript_command(f"movej({theta_str}, a=0.5, v=1)")

send_urscript_command("movej([1.57, -1.57, 0, -1.57, -1.57, 0], a=0.5, v=2.5)")
