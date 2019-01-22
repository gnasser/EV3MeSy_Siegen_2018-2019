#!/usr/bin/env python

##proporcional 1: sigue la linea y hace cruces 90 grados con negro a la derecha

## Simple talker demo that listens to std_msgs/Strings published 
## to the 'chatter' topic

import rospy
from sensor_msgs.msg import Illuminance	# Sensor library
from std_msgs.msg import String
from std_msgs.msg import Float64
motor_v_A=0	# velocidad de motor
motor_v_B=0	# velocidad de motor
inicio=0
integral=0
#Se agrega el Publisher---------------------------------
pub=rospy.Publisher('/ev3dev/OutPortA/command', Float64,queue_size=10)	# the node is publishing to the /ev3dev/OutPortA/command topic, motorA velocity
pub2=rospy.Publisher('/ev3dev/OutPortB/command', Float64,queue_size=10)	# the node is publishing to the /ev3dev/OutPortB/command topic, motorB velocity
#-------------------------------------------------------

def callback(data):
	global il
	global midpos
	Kp=1
	Ki=0.5
	il=data.illuminance	#illuminance number 0 (dark) to 100 (bright)
	'''if inicio == 0:
		print 'Es necesario calibrar'
		calibration(data)
	else:
		print 'Calibrado'
'''
	midpos=21 # (white-black)/2
	error=midpos-il
	correccion=error/midpos
	print "correcion" , correccion
	
	if il>80:
		motor_v_A=-2
		motor_v_B=2
	else:
		if il < midpos+25 and il > midpos-8 :	# robot sigue derecho
			motor_v_A=2
			motor_v_B=2
		
		elif il > midpos+25:	# robot desvia a derecha
			print('blanco')
			motor_v_A=-2-(correccion)
			motor_v_B=2-(correccion)		
		else:		#robot desvia a izquierda
			print('negro')
			motor_v_A=2+(correccion/2)
			motor_v_B=-2+(correccion/2)
		if il<3:	#apagar motores voltea el carro y deten el programa
			motor_v_A=0
			motor_v_B=0			
	

#Introduccion de los datos a mandar---------------------
	rospy.loginfo(motor_v_A)
	rospy.loginfo(motor_v_B)
	pub.publish(Float64(motor_v_A))
	pub2.publish(Float64(motor_v_B))
#-------------------------------------------------------

def calibration(data):
	global white
	global black
	global inicio
	print("Place the robot in white and press w")
	il=data.illuminance
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
	inicio =1

def listener():
#--------Calibration----------
	rospy.init_node('listener', anonymous=True)	# Crate the node
	rospy.Subscriber('color', Illuminance, callback)	#To read the color from sensor, the node is subscribed to /color topic
#Publicar-----------------------------------------------
	pub.publish(Float64(motor_v_A))	# The velocity of motor A
	pub2.publish(Float64(motor_v_B))	# The velocity of motor B
#-------------------------------------------------------
    # spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
    #Talker - Motores

if __name__ == '__main__':
	listener()



