#!/usr/bin/env python

import cv2
import numpy as npconda
import math
import dill
import socket
import time 
from time import sleep
from forw_inv_k import *
import ast
import os
from pyzbar.pyzbar import decode

def IMG2W(col, row): # Beta = fx/zc = fy/zc, beta = pixels/meter
    #print("row,col",row,col)
    #x_pixel.append(row)
    #y_pixel.append(col)
    #print(x_pixel,y_pixel)
    #a = x_pixel[0]-x_pixel[1] #pixel difference in x-axis
    #b = y_pixel[0]-y_pixel[1] # in y_axis
    a = 469.2138977050781-464.6624450683594
    b= 942.4413452148438-544.2061157226562
#row,col 295.6769104003906 924.7911987304688
# 270.7358093261719 351.1553955078125
    theta = np.arctan(a/b) #camera frame to world frame rotation angle
    beta = ((a**2+b**2)**0.5)/0.100 #pixel/meter
#print("beta,theta",beta,theta/3.14159*180)
    theta = -theta
    Or = 640
    Oc = 360
    x = 469.2138977050781- Oc
    y = 942.4413452148438 - Or
    #tx = 0.1 - (x/beta*np.cos(theta) + y/beta*np.sin(theta)) #camera frame to world frame difference in x-axis
    #ty = 0.1 - (y/beta*np.cos(theta) - x/beta*np.sin(theta))  #camera frame to world frame difference in y_axis
    tx = 0.0734
    ty = 0.0237
    #print("txty",tx,ty)
#print("tan(theta) = ",np.tan(theta),a/b)
    x = (row-Oc)
    y = (col-Or)
    xxw = (x*np.cos(theta)+y*np.sin(theta))/beta+tx
    yyw = (y*np.cos(theta)-x*np.sin(theta))/beta+ty
    xw = xxw
    yw = yyw
    #print("xwyw",xw,yw)
    return [xw, yw]

def blob_search(image_raw, color):
    
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()
    params.minDistBetweenBlobs = 50  # Adjust to increase separation

    # ========================= Student's code starts here =========================

    params.filterByColor = False
    params.blobColor = 255

    # Filter by Area.
    params.filterByArea = False
    params.minArea = 500
    #params.maxArea = 1400
    # Filter by Circularity
    params.filterByCircularity = False
    params.minCircularity = 0.5
    #params.maxCircularity = 1
    # Filter by Inerita
    params.filterByInertia = True
    params.minInertiaRatio = 0.8
    params.maxInertiaRatio = 1
    # Filter by Convexity
    params.filterByConvexity = False
    params.minConvexity = 0.1
    params.maxConvexity = 0.9

    # ========================= Student's code ends here ===========================
    #cap = cv2.VideoCapture(0) 
    #cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    # Create a detector with the parameters

    yellow_upper = (70, 90,100)
    yellow_lower = (20, 10, 5)
    green_upper = (89, 255, 255)
    green_lower = (36, 50, 70)
    blue_upper = (255,255,255)
    blue_lower = (35,0,0)
    red_upper = (35,250,175)
    red_lower = (0,0,0)
    coat_upper = (45,255,255)
    coat_lower = (20,50,50)
    # Convert the image into the HSV color space
    #retries =255
    #block_position = None

    detector = cv2.SimpleBlobDetector_create(params)
    hsv_image = cv2.cvtColor(image_raw, cv2.COLOR_BGR2HSV)

    if color == "yellow":
        mask_image = cv2.inRange(hsv_image, yellow_lower, yellow_upper)
    elif color == "green":
        mask_image = cv2.inRange(hsv_image, green_lower, green_upper)
    elif color == "blue":
        mask_image = cv2.inRange(hsv_image,blue_lower, blue_upper)
    elif color == "red":
        mask_image = cv2.inRange(hsv_image,red_lower, red_upper)
    elif color == "exceptyellow":
        mask_image1 = cv2.inRange(hsv_image,blue_lower, blue_upper)
        mask_image2 = cv2.inRange(hsv_image,red_lower, red_upper)
        #mask_image3 = cv2.inRange(hsv_image,coat_lower, coat_upper)
        mask_image = cv2.bitwise_or(mask_image1, mask_image2)
        #mask_image = cv2.inRange(hsv_image,coat_lower, coat_upper)
        #print("wised")
    
    mask_image = cv2.blur(mask_image, (5,5))
    inverted_mask = cv2.bitwise_not(mask_image)
    mask_image = inverted_mask

    keypoints = detector.detect(mask_image)

    blob_image_center = []
    num_blobs = len(keypoints)
    for i in range(num_blobs):
        blob_image_center.append((keypoints[i].pt[0],keypoints[i].pt[1]))

 
    im_with_keypoints = cv2.drawKeypoints(image_raw, keypoints, mask_image)
        
    mask_path = "mask_image.png"
    cv2.imwrite(mask_path, mask_image)
    image_path = "center_image.png"
    cv2.imwrite(image_path, im_with_keypoints)


    xw_yw = []

    if(num_blobs == 0):
        h = 0
    else:
        for i in range(num_blobs):
            xw_yw.append(IMG2W(blob_image_center[i][0], blob_image_center[i][1]))
            
    cv2.imshow("Mask View", mask_image)
    #cv2.namedWindow("Keypoint View")
    cv2.imshow("Keypoint View", im_with_keypoints)
    cv2.waitKey(5)
    return xw_yw # xw_yw_G, xw_yw_Y

def find_yellow_block():
    
    cap = cv2.VideoCapture(1)
    cap.set(3, 1280)  # set the resolution
    cap.set(4, 720)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None  # Return None if the camera cannot open
    
    yellow_block_position = None
    mask_size = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
    
        yellow_block_position = blob_search(frame, "exceptyellow")
        
        qr_codes = decode(frame)
        for qr_code in qr_codes:
            qr_data = qr_code.data.decode('utf-8')

            # Write the QR data to a file
            with open("C:\\Users\\ZeZhuang\\UR3\\scripts\\qr_data.txt", "w") as file:
                file.write(qr_data)

        # Read the QR data for the script file and mask size
        qr_path = f"C:\\Users\\ZeZhuang\\UR3\\scripts\\qr_data.txt"
        with open(qr_path, "r") as file:
            qr_data = file.readlines()

        if len(qr_data) >= 3:
            script_file = qr_data[0].strip()
            mask_size = float(qr_data[1].strip())
            Circle_Angle = float(qr_data[2].strip())            
            SprayHeight = float(qr_data[3].strip())
        # If yellow block is found, break the loop
        if yellow_block_position:
            break
        
        cv2.imshow('Camera View', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if yellow_block_position:
        return yellow_block_position, mask_size, Circle_Angle, SprayHeight
    else:
        return None  # Return None if no yellow block found

def avg(lst):
    return sum(lst) / len(lst)
def find_c(position,mask_size):
    # Collect all x, y coordinates
    blob_x = [pos[0] for pos in position]
    blob_y = [pos[1] for pos in position]
    left_corner = np.array([0.22, 0.12])
    c = []
    # Determine the number of masks based on the range of blob_x values
    mask_num = 1
    #print("max",max(blob_x)-min(blob_x))
    for i in range(4):
        if max(blob_y) - min(blob_y) > (mask_size*i-0.5)/100:
            mask_num = i+1
            #print(max(blob_y) - min(blob_y),mask_num,mask_size)
    #print("mask_num",mask_num)
    blob_collect = []

    for i in range(1, mask_num + 1):
        left_corner = np.array([0.23, 0.4])+np.array([0, mask_size*(i-1)/100])
        #print("left_corner",left_corner)
        dist = [np.linalg.norm(np.array(blob) - left_corner) for blob in position]
        idx = np.argmin(dist)
        c.append(position[idx])
        #print("blob_center:", c)
    return c,mask_num

def txt_editor(C, Coating_Height):
    Robot_Posture = []
    for i in range(len(C)):
        print(len(C),"lenC")
        Robot_Posture.append(lab_invk(C[i][0], C[i][1], Coating_Height, 0))
        #print(Robot_Posture,"***************")
        #print(f"C{i}", Robot_Posture[-1])  # Print each posture as it's added
        
    return Robot_Posture

# Write all Robot_Postures with the naming convention c1_q, c2_q, etc.
#def part_position(Robot_Posture):
#    with open("part_position.txt", "w") as file:
#        for i, posture in enumerate(Robot_Posture):
#            file.write(f"{posture}\n")  # Write each posture with a unique label
#    return

def allposition(All_Robot_Posture):
    with open("all_position.txt", "w") as file:
        for i, posture in enumerate(All_Robot_Posture):
            file.write(f"{posture}\n")  # Write each posture with a unique label
    return

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

#x_2 = 30.91
#y_2 = -340.1

# Real Coordinates
#x2 = 183
#y2 = 31

# Coordinate Rotation from Real to TCP : tau
#theta1 = np.arctan((x3-x2)/(y3-y2))
#theta2 = np.arctan((x_3-x_2)/(y_3-y_2))
#tau = np.pi-theta1-theta2

# Coordinates in Rotated frame
#yc3 = y3*np.sin(np.pi/2-tau)-x3*np.cos(np.pi-tau)
#xc3 = (x3**2+y3**2)**0.5*np.cos(np.arctan(y3/x3)+np.pi/2-tau)

# Difference in x y Axis : tx ty
#tx = xc3-x_3

#Convert from Real to TCP frame Try x2 y2
def TCP_frame_convert(x,y,coating_height):
    z_tcp = (coating_height*1000-100)/1000
    #xc = (x**2+y**2)**0.5*np.cos(np.arctan(y/x)+np.pi/2-tau)
    #yc = y*np.sin(np.pi/2-tau)-x*np.cos(np.pi-tau)
    x_tcp = (y - tx)/1000
    y_tcp = (-x + ty)/1000
    #print(x_tcp,y_tcp)
    return(x_tcp,y_tcp,z_tcp)    


def tcp_coordinate(C,Coating_Height):
    tcp = []
    with open("tcp_coordinate.txt", "w") as file:
        for i in range(len(C)):
            #print(len(C),"lenC")
            x2 = C[i][0] * 1000
            y2 = C[i][1] * 1000
            #print("x2y2",x2,y2)
            [x_tcp, y_tcp,z_tcp] = TCP_frame_convert(x2, y2, Coating_Height)
            m = (f"[{x_tcp}, {y_tcp}, {z_tcp}, 0, 3.14159, 0]")
            tcp.append(m)
            #print("tcp",tcp)
        for i, tcp_points in enumerate(tcp):
            file.write(f"{tcp_points}\n")
    return tcp


def all_center_pq():
    script_file_path = f"C:\\Users\\ZeZhuang\\UR3\\Skip_Functions\\move_to_center.script"
    tcp_file_path = f"C:\\Users\\ZeZhuang\\UR3\\scripts\\all_centers.txt"
    modified_file_path = f"C:\\Users\\ZeZhuang\\UR3\\scripts\\move_modified.script"  
    robot_posture_path = f"C:\\Users\\ZeZhuang\\UR3\\scripts\\all_position.txt"

    # Read files
    with open(script_file_path, "r") as script_file:
        script_lines = script_file.readlines()
    with open(tcp_file_path, "r") as tcp_file:
        new_coordinates_p = tcp_file.readlines()
    with open(robot_posture_path, "r") as posture_file:
        new_coordinates_q = posture_file.readlines()

    # Update global cX_p variables
    coordinate_index = 0
    last_p_line = -1
    for i, line in enumerate(script_lines):
        if line.strip().startswith(f"global c{coordinate_index + 1}_p=p"):
            if coordinate_index < len(new_coordinates_p):
                new_coordinate_p = new_coordinates_p[coordinate_index].strip()
                script_lines[i] = f"  global c{coordinate_index + 1}_p=p{new_coordinate_p}\n"
                coordinate_index += 1
            last_p_line = i

    while coordinate_index < len(new_coordinates_p):
        new_coordinate_p = new_coordinates_p[coordinate_index].strip()
        script_lines.insert(last_p_line + 1, f"  global c{coordinate_index + 1}_p=p{new_coordinate_p}\n")
        last_p_line += 1
        coordinate_index += 1

    # Update global cX_q variables
    coordinate_index = 0
    last_q_line = -1
    for i, line in enumerate(script_lines):
        if line.strip().startswith(f"global c{coordinate_index + 1}_q="):
            if coordinate_index < len(new_coordinates_q):
                new_coordinate_q = new_coordinates_q[coordinate_index].strip()
                script_lines[i] = f"  global c{coordinate_index + 1}_q={new_coordinate_q}\n"
                coordinate_index += 1
            last_q_line = i

    while coordinate_index < len(new_coordinates_q):
        new_coordinate_q = new_coordinates_q[coordinate_index].strip()
        script_lines.insert(last_q_line + 1, f"  global c{coordinate_index + 1}_q={new_coordinate_q}\n")
        last_q_line += 1
        coordinate_index += 1

    # Update movej commands
    movej_start_index = None
    for i, line in enumerate(script_lines):
        if line.strip().startswith("movej(c1_q"):
            movej_start_index = i
            break

    if movej_start_index is not None:
        # Remove all existing movej commands for cX_q
        j = movej_start_index
        while j < len(script_lines) and "movej(c" in script_lines[j]:
            del script_lines[j]

        # Add new movej commands for updated cX_q
        for k in range(1, len(new_coordinates_q) + 1):
            movej_command = f"    movel(c{k}_q, a=1.2, v=0.25)\n"
            script_lines.insert(movej_start_index, movej_command)
            movej_start_index += 1

    # Write the modified script back to the file
    with open(modified_file_path, "w") as modified_script_file:
        modified_script_file.writelines(script_lines)
        print("Script updated successfully.")


def circle_all_pq():
    script_file_path = f"C:\\Users\\ZeZhuang\\UR3\\Skip_Functions\\circle_all_angles.script"
    tcp_file_path = f"C:\\Users\\ZeZhuang\\UR3\\scripts\\all_centers.txt"
    modified_file_path = f"C:\\Users\\ZeZhuang\\UR3\\scripts\\circle_modified.script"
    robot_posture_path = f"C:\\Users\\ZeZhuang\\UR3\\scripts\\all_position.txt"

    # Read the original script lines
    with open(script_file_path, "r") as script_file:
        script_lines = script_file.readlines()

    # Read new center positions and postures
    with open(tcp_file_path, "r") as tcp_file:
        new_coordinates_p = tcp_file.readlines()

    with open(robot_posture_path, "r") as posture_file:
        new_coordinates_q = posture_file.readlines()

    # Modify or append the centers (only cX_p)
    coordinate_index = 0
    last_p_line = -1
    for i, line in enumerate(script_lines):
        line_stripped = line.strip()
        if line_stripped.startswith(f"global c{coordinate_index + 1}_p=p"):
            if coordinate_index < len(new_coordinates_p):
                new_coordinate_p = new_coordinates_p[coordinate_index].strip()
                script_lines[i] = f"  global c{coordinate_index + 1}_p=p{new_coordinate_p}\n"
                coordinate_index += 1
            last_p_line = i

    # Insert additional cX_p variables if there are more coordinates
    while coordinate_index < len(new_coordinates_p):
        new_coordinate_p = new_coordinates_p[coordinate_index].strip()
        script_lines.insert(last_p_line + 1, f"  global c{coordinate_index + 1}_p=p{new_coordinate_p}\n")
        last_p_line += 1
        coordinate_index += 1

    # Modify or append the orientations (cX_q) to match cX_p
    coordinate_index = 0
    last_q_line = -1
    for i, line in enumerate(script_lines):
        line_stripped = line.strip()
        if line_stripped.startswith(f"global c{coordinate_index + 1}_q="):
            if coordinate_index < len(new_coordinates_q):
                new_coordinate_q = new_coordinates_q[coordinate_index].strip()
                script_lines[i] = f"  global c{coordinate_index + 1}_q={new_coordinate_q}\n"
                coordinate_index += 1
            last_q_line = i

    # Insert additional cX_q variables if there are more coordinates
    while coordinate_index < len(new_coordinates_q):
        new_coordinate_q = new_coordinates_q[coordinate_index].strip()
        script_lines.insert(last_q_line + 1, f"  global c{coordinate_index + 1}_q={new_coordinate_q}\n")
        last_q_line += 1
        coordinate_index += 1

    # Locate the position to insert additional movej commands
    movej_index = -1
    for i, line in enumerate(script_lines):
        if line.strip().startswith("movej(get_inverse_kin("):
            movej_index = i
            break

    # Ensure movej and circle_all_angle are added correctly for c1 first
    if movej_index != -1:
        commands = []
        for j in range(1, len(new_coordinates_q) + 1):  # Loop through all cX_q
            movej_command = f"  movel(c{j}_p, a=1.2, v=0.25)\n"
            assign_command = f"  global c = c{j}_p\n"
            circle_command = f"  CircleAllangles()\n"
            commands.extend([movej_command, assign_command, circle_command])

        # Insert all commands starting from the first movej position
        script_lines = script_lines[:movej_index] + commands + script_lines[movej_index + 1:]

    # Write the modified script back to the file
    with open(modified_file_path, "w") as modified_script_file:
        modified_script_file.writelines(script_lines)
        print("Script updated successfully.")

def update_circle_angle_a(spray_angle):
    script_file_path = f"C:\\Users\\ZeZhuang\\UR3\\Skip_Functions\\circle_all_angles.script"
    # Calculate the new value for A
    new_a = spray_angle * 3.141592657 / 180  # Convert SprayAngle from degrees to radians

    # Read the script file
    with open(script_file_path, 'r') as script_file:
        script_lines = script_file.readlines()

    # Update the line defining A
    updated_lines = []
    for line in script_lines:
        if line.strip().startswith("global A="):  # Look for the line defining A
            updated_line = f"  global A={new_a:.6f}\n"  # Update the value of A
            updated_lines.append(updated_line)
        else:
            updated_lines.append(line)

    # Write the updated lines back to the script file
    with open(script_file_path, 'w') as script_file:
        script_file.writelines(updated_lines)


x_pixel = []
y_pixel = []
#position,mask_size,Circle_Angle,SprayHeight = find_yellow_block()
#C,mask_num = find_c(position,mask_size)
#Coating_Height = (SprayHeight+51)/1000
#print("CH",Coating_Height)
#Robot_Posture = txt_editor(C, Coating_Height)
#All_Robot_Posture = txt_editor(position, Coating_Height)
#print(All_Robot_Posture)
#part_position(Robot_Posture)
#allposition(All_Robot_Posture)
#all_center_pq()
#circle_all_pq()
x_3 = 70.88
y_3 = -347.41
x3 = 187.75
y3 = 68.97
ty = x3+y_3
tx = y3-x_3
#tcp_coordinate(position,Coating_Height)