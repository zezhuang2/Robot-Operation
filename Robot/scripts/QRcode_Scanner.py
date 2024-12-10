import dill
import struct
import rtde_receive
from blob_search import *

dill.settings['recurse'] = True
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
def move_home():
    send_urscript_command("movej([1.57, -1.57, 0, -1.57, 0, 0], a=0.5, v=2.5)")
    wait_time(2)
    tcp_speed = rtde_tcp_speed()
    tcp_speed = np.linalg.norm(tcp_speed)
    while tcp_speed>1e-4:
        tcp_speed = rtde_tcp_speed()
        tcp_speed = np.linalg.norm(tcp_speed)
        wait_time(1)
robotIP = "192.168.50.52"
PRIMARY_PORT = 30001
SECONDARY_PORT = 30002
REALTIME_PORT = 30003
PI = 3.1415926
new_line = "\n"
def wait_time(time_threshold):
    start_time = time.time()
    last_check_time = 0
    check_interval = 0.1  # Check every 100ms
    while time.time() - start_time < time_threshold:
        current_time = time.time()
def rtde_tcp_speed():
    rtde_r = rtde_receive.RTDEReceiveInterface(robotIP)
    try:
        while True:
            tcp_speed = rtde_r.getActualTCPSpeed()
            #print(f"TCPSpeed:{tcp_speed}")
            return tcp_speed
    except Exception as e:
        print(f"Error: {e}")

def turntable():
    with open(f"C:/Users/ZeZhuang/UR3/Skip_Functions/turntable.script","rb") as file:
        script = file.read()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((robotIP, PRIMARY_PORT))
        s.sendall(script)
        wait_time(2)
        tcp_speed = rtde_tcp_speed()
        tcp_speed = np.linalg.norm(tcp_speed)
        while tcp_speed>1e-4:
            tcp_speed = rtde_tcp_speed()
            tcp_speed = np.linalg.norm(tcp_speed)
            wait_time(1)
    except BrokenPipeError:
        print("Broken pipe error: unable to send the script.")
    finally:
        s.close()


def center_q():
    with open("part_position.txt") as file:
        q = len(file.readlines())
        #print("q",q)
    return q

def center_p():
    with open("tcp_coordinate.txt") as file:
        p = len(file.readlines())
    return p

def move_to_center(j):
    with open(f"C:/Users/ZeZhuang/UR3/Skip_Functions/Side{j}_Collected_Points.txt","rb") as file:
        data = file.read()
    with open(f"C:/Users/ZeZhuang/UR3/scripts/all_position.txt","wb") as file:
        file.write(data)
    with open(f"C:/Users/ZeZhuang/UR3/Skip_Functions/Side{j}_Collected_tcp.txt","rb") as file:
        data = file.read()
    with open(f"C:/Users/ZeZhuang/UR3/scripts/all_centers.txt","wb") as file:
        file.write(data)
    circle_all_pq()
    all_center_pq()
    with open(f"C:/Users/ZeZhuang/UR3/scripts/move_modified.script","rb") as file:
        script = file.read()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((robotIP, PRIMARY_PORT))
        s.sendall(script)
        wait_time(2)
        tcp_speed = rtde_tcp_speed()
        tcp_speed = np.linalg.norm(tcp_speed)
        while tcp_speed>1e-4:
            tcp_speed = rtde_tcp_speed()
            tcp_speed = np.linalg.norm(tcp_speed)
            wait_time(1)
    except BrokenPipeError:
        print("Broken pipe error: unable to send the script.")
    finally:
        s.close()

def circle_all_center(j):
    with open(f"C:/Users/ZeZhuang/UR3/Skip_Functions/Side{j}_Collected_tcp.txt","rb") as file:
        data = file.read()
    with open(f"C:/Users/ZeZhuang/UR3/scripts/all_centers.txt","wb") as file:
        file.write(data)
    with open(f"C:/Users/ZeZhuang/UR3/Skip_Functions/Side{j}_Collected_Points.txt","rb") as file:
        data = file.read()
    with open(f"C:/Users/ZeZhuang/UR3/scripts/all_position.txt","wb") as file:
        file.write(data)
    circle_all_pq()
    all_center_pq()
    with open(f"C:/Users/ZeZhuang/UR3/scripts/circle_modified.script","rb") as file:
        script = file.read()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((robotIP, REALTIME_PORT))
        s.sendall(script)
        wait_time(2)
        tcp_speed = rtde_tcp_speed()
        tcp_speed = np.linalg.norm(tcp_speed)
        while tcp_speed>1e-4:
            tcp_speed = rtde_tcp_speed()
            tcp_speed = np.linalg.norm(tcp_speed)
            wait_time(1)
    except BrokenPipeError:
        print("Broken pipe error: unable to send the script.")
    finally:
        s.close()


def clean():
    with open(f"C:/Users/ZeZhuang/UR3/Skip_Functions/clean.script","rb") as file:
        script = file.read()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((robotIP, REALTIME_PORT))
        s.sendall(script)
        wait_time(2)
        tcp_speed = rtde_tcp_speed()
        tcp_speed = np.linalg.norm(tcp_speed)
        while tcp_speed>1e-4:
            tcp_speed = rtde_tcp_speed()
            tcp_speed = np.linalg.norm(tcp_speed)
            wait_time(1)
    except BrokenPipeError:
        print("Broken pipe error: unable to send the script.")
    finally:
        s.close()

def spraychip():
    with open(f"C:/Users/ZeZhuang/UR3/Skip_Functions/spraychip.script","rb") as file:
        script = file.read()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((robotIP, REALTIME_PORT))
        s.sendall(script)
        wait_time(2)
        tcp_speed = rtde_tcp_speed()
        tcp_speed = np.linalg.norm(tcp_speed)
        while tcp_speed>1e-4:
            tcp_speed = rtde_tcp_speed()
            tcp_speed = np.linalg.norm(tcp_speed)
            wait_time(1)
    except BrokenPipeError:
        print("Broken pipe error: unable to send the script.")
    finally:
        s.close()

def set_on():
    with open(f"C:/Users/ZeZhuang/UR3/Skip_Functions/set_on.script","rb") as file:
        script = file.read()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((robotIP, PRIMARY_PORT))
        s.sendall(script)
    except BrokenPipeError:
        print("Broken pipe error: unable to send the script.")
    finally:
        s.close()

def set_off():
    with open(f"C:/Users/ZeZhuang/UR3/Skip_Functions/set_off.script","rb") as file:
        script = file.read()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((robotIP, PRIMARY_PORT))
        s.sendall(script)
    except BrokenPipeError:
        print("Broken pipe error: unable to send the script.")
    finally:
        s.close()

def collect_centers(j):
    move_home()
    result = find_yellow_block()
    
    if result is None:
        print("No yellow block found or mask size missing.")
        return  # Safely handle the case with no block found

    position, mask_size, SprayAngle, SprayHeight = result
    update_circle_angle_a(SprayAngle)
    #print(position)
    #print(C,mask_num,"C,masknum")
    Coating_Height = (SprayHeight+51+150)/1000
    #print("CH",Coating_Height)
    #Robot_Posture = txt_editor(C, Coating_Height)
    All_Robot_Posture = txt_editor(position, Coating_Height) #Returns Robot poseture for each joint not generating txt file
    #print(All_Robot_Posture,"************")
    allposition(All_Robot_Posture)
    print(All_Robot_Posture)
    all_center_pq()
    circle_all_pq()
    alltcp = tcp_coordinate(position,Coating_Height)
    with open(f"C:/Users/ZeZhuang/UR3/Skip_Functions/Side{j}_Collected_Points.txt", "w") as file: #Store joint positions in txt for each side
        for posture in All_Robot_Posture:
            #print(posture)
            file.write(f"{posture}\n")
    with open(f"C:/Users/ZeZhuang/UR3/Skip_Functions/Side{j}_Collected_tcp.txt", "w") as file: #Store joint positions in txt for each side
        for tcp in alltcp:
            #print(posture)
            file.write(f"{tcp}\n")

    print(f"collected{j}")

def take_centers():
    #turntable()
    side_num = 0
    #collect_centers(side_num)
    cap = cv2.VideoCapture(1)
    cap.set(3, 1280) # set the resolution
    cap.set(4, 720)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None
    #cv2.imshow('QR Code Scanner', frame)

    # Capture frame-by-frame
    round = 0
    Circle_Angle = 0
    cen_q = []
    cen_p = []
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            print("Failed to grab frame. Reinitializing the camera...")
            cap.release()
            cap = cv2.VideoCapture(1)
            cap.set(3, 1280)
            cap.set(4, 720)
            continue

        qr_codes = decode(frame)
        if not qr_codes:  # No QR codes detected
            print("No QR codes found in the frame.")

        for qr_code in qr_codes:
        # Decode the QR code data
            qr_data = qr_code.data.decode('utf-8')
            print(f"Decoded QR code data: {qr_data}")

        # Write the QR data to a file
            with open("qr_data.txt", "w") as file:
                file.write(qr_data)
        if qr_codes is True:
            side_num += 1
            print("sidenum qr",side_num)
            for qr_code in qr_codes:
                qr_data = qr_code.data.decode('utf-8')
                if len(qr_data) >= 3:
                    Circle_Angle = float(qr_data[2].strip())            
            round += 1

            if round > 1:
                break
            #start_with_qr(frame)
            collect_centers(side_num)
            cen_q.append(center_q())
            cen_p.append(center_p())
            print("pq",cen_p,cen_q)
            turntable()
            move_home()
            #return
        else:
            side_num += 1
            if side_num > 6:
                break
            #print(side_num)
            #start_with_qr(frame) # store center values in part_position and tcp_coordinate in additional new lines
            collect_centers(side_num)
            cen_q.append(center_q())
            #print("111111111111111",cen_q)
            cen_p.append(center_p())
            turntable()
            print("pq",cen_p,cen_q,side_num)
            #print(movingstat,"printed movingstat")
            move_home()
            #return
    cap.release()
    cv2.destroyAllWindows()
    print(cen_q,cen_p,Circle_Angle)
    return cen_q, cen_p, Circle_Angle

def store_centers():
    cen_q, cen_p, Circle_Angle = take_centers()
    with open("last_pqc.txt","w") as file:
        file.write(f"{cen_p}\n{cen_q}\n{Circle_Angle}")

def coat_all_sides():
    with open("last_pqc.txt","rb") as file:
        cen_p, cen_q, Circle_Angle = file.readlines()
    side_num = 1
    round = 1
    coatnum = 1
    clean()
    spraychip()
    while True:
        print("start coating")
        print("loopsidenum",side_num)
        #print("finish cleaning")
        if side_num == 7:
            side_num = 1
            print("side7",side_num)
            round += 1
            if round > coatnum:
                print(f"Complete! Coating Number = {coatnum}")
                break

        else:
            #coat cen_q,cen_p[side_num]
            #print(cen_p[side_num],cen_q[side_num],side_num)
            #set_on()
            if Circle_Angle == 0:
                move_to_center(side_num)
                print("moved to center")
            else:
                circle_all_center(side_num)
                #move_to_center(side_num)
                print("moved to center and circled")
            #set_off()
            turntable()
            side_num += 1

        
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#position,mask_size = find_yellow_block()
#take_centers()
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.close()
store_centers()
coat_all_sides()
#clean()
#turntable()