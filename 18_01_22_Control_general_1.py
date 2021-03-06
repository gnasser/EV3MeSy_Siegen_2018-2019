#!/usr/bin/env python

##proporcional 1: sigue la linea por el lado derecho del negro, ralenizando un solo motor, hasta incluso hacerlo retroceder a la velocidad de crucero si se sale completamente, y se deja el otro motor quieto. En la zona central no se corrije (va derecho) y en la zona intermedia se corrije proporcionalmente a la diferencia con la señal del midpos según la curva caracteristica del sensor.

## Simple talker demo that listens to std_msgs/Strings published 
## to the 'chatter' topic

import rospy
from sensor_msgs.msg import Illuminance	# Sensor library
from std_msgs.msg import String
from std_msgs.msg import Float64
motor_v_iz=0	# velocidad de motor
motor_v_der=0	# velocidad de motor
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
	global integral
	il=data.illuminance	#illuminance number 0 (dark) to 100 (bright)
	'''if inicio == 0:
		print 'Es necesario calibrar'
		calibration(data)
	else:
		print 'Calibrado'
'''

	midpos=54 # (white-black)/2
	d_blanco=10
	d_negro=10
	motor_base=1.5
	motor_curva=2
	error=midpos-il
	correccion=0.0122*il-0.1052-.05536 # curva caract del sensor da la magnitud de la corrección y pasa por cero en midpos
	#correccion = (Kp*error + Ki*integral)/midpos
	print "correcion" , correccion
	
	if il>=88:	#si esta en esquina
		motor_v_iz =-motor_curva
		motor_v_der= motor_curva
	elif 3<il<=12:
		motor_v_iz = motor_curva
		motor_v_der=-motor_curva		
	else:
		if il < midpos+d_blanco and il > midpos-d_negro :	# robot sigue derecho
			motor_v_iz =motor_base
			motor_v_der=motor_base
		
		elif il > midpos+d_blanco:	# robot desvia a derecha
			print('blanco')
			motor_v_iz = motor_base*(1-4*correccion)
			motor_v_der= motor_base		
		else:		#robot desvia a izquierda
			print('negro')
			motor_v_iz = motor_base
			motor_v_der= motor_base*(1-4*abs(correccion))
		if il<3:
			motor_v_iz= 0
			motor_v_der=0			
	

#Introduccion de los datos a mandar---------------------
	rospy.loginfo(motor_v_iz)
	rospy.loginfo(motor_v_der)
	pub.publish(Float64(motor_v_iz))
	pub2.publish(Float64(motor_v_der))
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
	pub.publish(Float64(motor_v_iz))	# The velocity of motor A
	pub2.publish(Float64(motor_v_der))	# The velocity of motor B
#-------------------------------------------------------
    # spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
    #Talker - Motores

if __name__ == '__main__':
	print "inicio main", inicio
	print "estoy en main"
	listener()



