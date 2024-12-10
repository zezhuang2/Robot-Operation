#!/usr/bin/env python
import numpy as np
from scipy.linalg import expm, logm
#from blob_search import *
#from lab5_header import *

"""
Use 'expm' for matrix exponential.
Angles are in radian, distance are in meters.
"""
def Get_MS():
	# =================== Your code starts here ====================#
	# Fill in the correct values for w1~6 and v1~6, as well as the M matrix
	M = np.eye(4)
	S = np.zeros((6,6))
	w1 = np.array([0, 0, 1])
	w2 = np.array([0, 1, 0])
	w3 = np.array([0, 1, 0])
	w4 = np.array([0, 1, 0])
	w5 = np.array([1, 0, 0])
	w6 = np.array([0, 1, 0])
	q1 = np.array([-155, 0, 0]) #[-150,-150,10]
	q2 = np.array([-155, 120, 152]) #[-150,270,152]
	q3 = np.array([244-155, 120, 152]) #[94,270,152]
	q4 = np.array([244+213-155,27, 152]) #[307,177,152]
	q5 = np.array([244+213-155, 110, 152]) #[307,260,152]
	q6 = np.array([244+213+83-155, 110, 152]) #[390,260,152]
	v1 = np.cross(-w1,q1)
	v2 = np.cross(-w2,q2)
	v3 = np.cross(-w3,q3)
	v4 = np.cross(-w4,q4)
	v5 = np.cross(-w5,q5)
	v6 = np.cross(-w6,q6)
	S1 = np.array([[0, -w1[2], w1[1], v1[0]], [w1[2], 0, -w1[0], v1[1]], [-w1[1], w1[0], 0, v1[2]], [0, 0, 0, 0]])
	S2 = np.array([[0, -w2[2], w2[1], v2[0]], [w2[2], 0, -w2[0], v2[1]], [-w2[1], w2[0], 0, v2[2]], [0, 0, 0, 0]])
	S3 = np.array([[0, -w3[2], w3[1], v3[0]], [w3[2], 0, -w3[0], v3[1]], [-w3[1], w3[0], 0, v3[2]], [0, 0, 0, 0]])
	S4 = np.array([[0, -w4[2], w4[1], v4[0]], [w4[2], 0, -w4[0], v4[1]], [-w4[1], w4[0], 0, v4[2]], [0, 0, 0, 0]])
	S5 = np.array([[0, -w5[2], w5[1], v5[0]], [w5[2], 0, -w5[0], v5[1]], [-w5[1], w5[0], 0, v5[2]], [0, 0, 0, 0]])
	S6 = np.array([[0, -w6[2], w6[1], v6[0]], [w6[2], 0, -w6[0], v6[1]], [-w6[1], w6[0], 0, v6[2]], [0, 0, 0, 0]])
	S = np.array([S1, S2, S3, S4, S5, S6])
	#M = np.array([[0, -1, 0, 390],[0, 0, -1, 401], [1, 0, 0, 215.5], [0, 0, 0, 1]])
	M = np.array([[0, -1, 0, 380],[0, 0, -1, 310], [1, 0, 0, 152], [0, 0, 0, 1]])



	# ==============================================================#
	return M, S


"""
Function that calculates encoder numbers for each motor
"""
def lab_fk(theta1, theta2, theta3, theta4, theta5, theta6):

	# Initialize the return_value
	return_value = [None, None, None, None, None, None]

	#print("Foward kinematics calculated:\n")

	# =================== Your code starts here ====================#
	theta = np.array([theta1,theta2,theta3,theta4,theta5,theta6])
	M, S = Get_MS()
	T = np.array(expm(S[0]*theta1)@expm(S[1]*theta2)@expm(S[2]*theta3)@expm(S[3]*theta4)@expm(S[4]*theta5)@expm(S[5]*theta6)@M)
	#print(T)
	#theta = T*theta

	# ==============================================================#

	return_value[0] = theta[0] + 0.5*np.pi #- 3.66/180*np.pi
	return_value[1] = theta[1]
	return_value[2] = theta[2]
	return_value[3] = theta[3] - (0.5*np.pi)
	return_value[4] = theta[4]
	return_value[5] = theta[5]
	#print("return_value",return_value)
	#print(return_value[0]/3.14159*180,return_value[1]/3.14159*180,return_value[2]/3.14159*180,return_value[3]/3.14159*180,return_value[4]/3.14159*180,return_value[5]/3.14159*180)
	return return_value


"""
Function that calculates an elbow up Inverse Kinematic solution for the UR3
"""
def lab_invk(xWgrip, yWgrip, zWgrip, yaw_WgripDegree):
	# =================== Your code starts here ====================#

	theta1 = 0.0
	theta2 = 0.0
	theta3 = 0.0
	theta4 = 0.0
	theta5 = 0.0
	theta6 = 0.0

	xWgrip = xWgrip*1000
	yWgrip = yWgrip*1000
	zWgrip = zWgrip*1000
	xgrip = xWgrip + 230
	ygrip = yWgrip - 21#- 150S
	zgrip = zWgrip #- 10
	#print("COORDS", xgrip,ygrip,zgrip)
	yaw_radians = yaw_WgripDegree*np.pi/180.0
	xcen = xgrip #- 53.5*np.cos(yaw_radians) # 53.5 is distance from gripper to center
	ycen = ygrip #- 53.5*np.sin(yaw_radians)
	zcen = zWgrip
	a = 110/((xcen**2 + ycen**2)**0.5) # 110 is distance from center to 3end
	smallAng = np.arcsin(a)
	bigAng = np.arctan(ycen/xcen)
	#print("bigangle",bigAng)
	theta1 = bigAng - smallAng
	theta6 = np.pi/2 - yaw_radians + theta1
	x3end = np.cos(theta1)*((xcen**2 + ycen**2)**0.5*np.cos(smallAng)-83) # 83 = L8
	y3end = np.sin(theta1)*((xcen**2 + ycen**2)**0.5*np.cos(smallAng)-83) # 83 = L8
	z3end = zcen + 83 # 142 = L10 + L8 = 59 + 83
	#print("z3end",z3end)
	L = (x3end**2 + y3end**2 + (z3end-152)**2)**0.5 # 152 = L1
	b = (244**2+L**2-213**2)/(2*244*L) # 244 = L3, L = endpoint to origin, 213 = L5
	#print("B",b)
	beta2 = np.arccos(b)
	c = (z3end-152)/L # 83 = L8
	alpha2 = np.arcsin(c)
	theta2 = -(beta2 + alpha2)
	d4 = (213**2-L**2+244**2)/(2*213*244)
	#print("D4", d4)
	alpha4 = np.arccos(d4)
	#print("alpha4",alpha4)
	theta3 = np.pi - alpha4
	#beta4 = 2*np.pi - alpha4 - theta2 - np.pi/2
	theta4 = -(np.pi + theta2 - alpha4)
	theta5 = -90*np.pi/180
	thetas = [theta1, theta2, theta3, theta4, theta5, theta6]
	#print(thetas)
	#print("THETAS", theta1, theta2, theta3, theta4, theta5, theta6)
	# ==============================================================#
	#print(lab_fk(theta1, theta2, theta3, theta4, theta5, theta6))
	return lab_fk(theta1, theta2, theta3, theta4, theta5, theta6)
	#return thetas

