#!/usr/bin/env python

import cv2
import numpy as np


## Place two objects at world coordinate (7, 8.8) and (7, 20) in unit of cm

x_pixel = []
y_pixel = []

def IMG2W(col, row): 
    global x_pixel, y_pixel
    
    # Append the current row and column values to the lists
    x_pixel.append(row)
    print("x_pixel",x_pixel,len(x_pixel))
    y_pixel.append(col)
    print("y_pixel",y_pixel)


    # Ensure there are at least two points before computing differences
    if len(x_pixel) < 2 or len(y_pixel) < 2:
        print("Not enough points to calculate differences.")
        return None  # Or handle this case appropriately

    # Calculate pixel differences in x and y axes
    a = x_pixel[0] - x_pixel[1]  # pixel difference in x-a
    b = y_pixel[0] - y_pixel[1]  # pixel difference in y-axis

    # Calculate rotation angle and pixel-to-world conversion (beta)
    theta = np.arctan(a / b)  # camera frame to world frame rotation angle
    beta = ((a**2 + b**2)**0.5) / 0.100  # pixels/meter

    theta = -theta
    Or = 640
    Oc = 360

    x = row - Oc
    y = col - Or

    tx = 0.069 - (x / beta * np.cos(theta) + y / beta * np.sin(theta))  # x-axis
    ty = -0.088 - (y / beta * np.cos(theta) - x / beta * np.sin(theta))  # y-axis

    xxw = (x * np.cos(theta) + y * np.sin(theta)) / beta + tx
    yyw = (y * np.cos(theta) - x * np.sin(theta)) / beta + ty
    xw = -yyw
    yw = xxw
    print(tx,ty)
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
    blue_lower = (45,0,0)
    red_upper = (30,255,255)
    red_lower = (0,0,0)
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

    mask_image = cv2.blur(mask_image, (5,5))
    inverted_mask = cv2.bitwise_not(mask_image)
    mask_image = inverted_mask

    keypoints = detector.detect(mask_image)

    blob_image_center = []
    num_blobs = len(keypoints)
    for i in range(num_blobs):
        blob_image_center.append((keypoints[i].pt[0],keypoints[i].pt[1]))

 
    im_with_keypoints = cv2.drawKeypoints(image_raw, keypoints, mask_image)
        
    #mask_path = "mask_image.png"
    #cv2.imwrite(mask_path, mask_image)
    image_path = "Calibration_Image.png"
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

cap = cv2.VideoCapture(2)
cap.set(3, 1280) # set the resolution
cap.set(4, 720)

if not cap.isOpened():
    print("Error: Could not open camera.")
    
ret, frame = cap.read()
#    if not ret:
#        print("Failed to grab frame")
#        break
blob_search(frame, "blue")
cap.release()
cv2.destroyAllWindows()