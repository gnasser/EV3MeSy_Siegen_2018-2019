#!/usr/bin/env python

## Simple talker demo that listens to std_msgs/Strings published 
## to the 'chatter' topic

import rospy
from sensor_msgs.msg import Illuminance	# Sensor library
from std_msgs.msg import String
from std_msgs.msg import Float64
motor_v_A=0	# velocidad de motor
motor_v_B=0	# velocidad de motor


#black=0
#Se agrega el Publisher---------------------------------
pub=rospy.Publisher('/ev3dev/OutPortA/command', Float64,queue_size=10)	# the node is publishing to the /ev3dev/OutPortA/command topic, motorA velocity
pub2=rospy.Publisher('/ev3dev/OutPortB/command', Float64,queue_size=10)	# the node is publishing to the /ev3dev/OutPortB/command topic, motorB velocity
#-------------------------------------------------------

def callback(data):
	global il
	il=data.illuminance	#illuminance number 0 (dark) to 100 (bright)
	print il
	print inicio
	'''if inicio == 0:
		print 'Es necesario calibrar'
		calibration()
	else:
		print 'Calibrado''''
	if il > 50 :
		print('blanco')
		motor_v_A=0
		motor_v_B=0
	else:
		print('negro')
		motor_v_A=10
		motor_v_B=10
#Introduccion de los datos a mandar---------------------
	rospy.loginfo(motor_v_A)
	rospy.loginfo(motor_v_B)
	pub.publish(Float64(motor_v_A))
	pub2.publish(Float64(motor_v_B))
#-------------------------------------------------------

def calibration():
	global inicio
	global white
	global black

	print("Place the robot in white and press w")
	ref_cali=raw_input()
	while ref_cali != 'w':
		print "waiting for w"
		ref_cali=raw_input()
	white=il	
	print'White color:',white

	print("Place the robot in black and press b")
	ref_cali=raw_input()
	while ref_cali != 'b':
		print "waiting for b"
		ref_cali=raw_input()
	black=il
	print 'Black color:',black
	inicio = 1

def listener():
#--------Calibration----------
	global inicio	
	inicio = 0
	rospy.init_node('listener', anonymous=True)	# Crate the node
	rospy.Subscriber('color', Illuminance, callback)	#To read the color from sensor, the node is subscribed to /color topic
	
	'''if inicio == 0:	# if the code has just begun inicio=0
		calibration()
		inicio=inicio+1'''
#Publicar-----------------------------------------------
	pub.publish(Float64(motor_v_A))	# The velocity of motor A
	pub2.publish(Float64(motor_v_B))	# The velocity of motor B
#-------------------------------------------------------
    # spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
    #Talker - Motores

if __name__ == '__main__':
	listener()



