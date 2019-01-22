#!/usr/bin/env python

##proporcional 1: sigue la linea y hace cruces 90 grados negro a la izquierda y cruces en esquinas cerrado calibraciones hechas en el laboratorio
#Se esta reestructurando el c'odigo para que acepte distintos sensores
## Simple talker demo that listens to std_msgs/Strings published 
## to the 'chatter' topic

import rospy
from sensor_msgs.msg import Illuminance	# Sensor library
from std_msgs.msg import String
from std_msgs.msg import Float64
motor_v_iz=0	# velocidad de motor
motor_v_der=0	# velocidad de motor
inicio=0

#Se agrega el Publisher---------------------------------

#-------------------------------------------------------

class sensor_data:	# En esta clase se almacenan los datos recibidos por los sensores
	def __init__(self):	#Creacion de la clase	
		self.il=0.0		#En il se almacena el valor de la iluminancia recibida por el sensor de color
	def iluminacion (self,data):
		self.il=data.illuminance # Recibido un valor de iluminacion, actualizacion del dato. illuminance number 0 (dark) to 100 (bright)
		return self.il

def motors_velocity(il):

#esta funcion define la velocidad de los motores en funcion de lo que se lee del sensor de color
# il es la lectura del sensor de color
	midpos=60 # (white-black)/2
	d_blanco=15
	d_negro=5
	motor_base=1
	motor_curva=2
	error=midpos-il
	correccion=error/midpos
	#correccion = (Kp*error + Ki*integral)/midpos
	print "correcion" , correccion
	
	'''if il>=88:	#si esta en esquina
		motor_v_iz=-motor_curva
		motor_v_der=motor_curva'''

	'''elif 3<il<=13:
		motor_v_iz=motor_curva
		motor_v_der=-motor_curva'''		
	
	if il < 65 and il > 20 :	# robot sigue derecho
		motor_v_iz=motor_base
		motor_v_der=motor_base
	
	elif il > midpos+d_blanco:	# robot desvia a derecha
		print('blanco')
		motor_v_iz=-.5
		motor_v_der= 1		
	else:		#robot desvia a izquierda
		print('negro')
		motor_v_iz=1#motor_base+(correccion)
		motor_v_der=-.5#-motor_base+(correccion)
	if il<3:
		motor_v_iz=0
		motor_v_der=0
			
	return motor_v_iz, motor_v_der
#-------------------------------------------------------
def listener_talker():
	SensorData=sensor_data()
#--------Creacion de los nodos a utilizar----------
	rospy.init_node('listener_talker_color', anonymous=True)	# Creacion del nodo que se suscribe al sensor de color
	pub=rospy.Publisher('/ev3dev/OutPortA/command', Float64,queue_size=10)	# the node is publishing to the /ev3dev/OutPortA/command topic, motorA velocity
	pub2=rospy.Publisher('/ev3dev/OutPortB/command', Float64,queue_size=10)	# the node is publishing to the /ev3dev/OutPortB/command topic, motorB velocity
	rospy.Subscriber('color', Illuminance, SensorData.iluminacion)	#To read the color from sensor, the node is subscribed to /color topic
	rate=rospy.Rate(100)
#Publicar-----------------------------------------------
	while not rospy.is_shutdown():
	 	motor_v_iz, motor_v_der = motors_velocity(SensorData.il)
	 	rospy.loginfo(motor_v_iz)
	 	rospy.loginfo(motor_v_der)
	 	pub.publish(Float64(motor_v_iz))	# The velocity of motor A
	 	pub2.publish(Float64(motor_v_der))	# The velocity of motor B
		rate.sleep()
#-------------------------------------------------------
    # spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
    #Talker - Motores

if __name__ == '__main__':
	try:
		listener_talker()
	except rospy.ROSInterruptException:
	        pass



