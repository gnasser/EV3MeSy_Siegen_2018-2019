#!/usr/bin/env python

##proporcional 1: sigue la linea y hace cruces 90 grados negro a la izquierda y cruces en esquinas cerrado calibraciones hechas es el laboratorio
#Se esta reeatructurando el c'odigo para que acepte distintos sensores
##Lee sensores de proximidad y color, tiene topico para publicar a motor que mueve el brazo
# se corrige la trayectoria solo girando en torno al centro de masa del robot si se desvia un poco del centro de la linea
# Al encontrar un obstaculo a 12cm se detiene, avanza un poco y luego retrocede la misma distancia

import rospy
from sensor_msgs.msg import Illuminance	# color Sensor library
from sensor_msgs.msg import Range	# ultrasonic Sensor library
from std_msgs.msg import String
from std_msgs.msg import Float64
import time

motor_v_iz=0	# velocidad de motor
motor_v_der=0	# velocidad de motor
inicio=0

#Se agrega el Publisher---------------------------------

#-------------------------------------------------------

class sensor_data:	# En esta clase se almacenan los datos recibidos por los sensores
	def __init__(self):	#Creacion de la clase	
		self.il=0.0		#En il se almacena el valor de la iluminancia recibida por el sensor de color
		self.dist=0.0
	def iluminacion (self,data):
		self.il=data.illuminance # Recibido un valor de iluminacion, actualizacion del dato. illuminance number 0 (dark) to 100 (bright)
		return self.il
	def distancia(self,data):
		self.dist=data.range
		return self.dist



def motors_velocity(il,dist):
	motor_base=1
	
	if il < 33 and il > 13 :	# robot sigue derecho
		motor_v_iz=motor_base
		motor_v_der=motor_base
	
	elif il > 34:	# robot desvia a derecha
		print('blanco')
		motor_v_iz=-1
		motor_v_der= 1		
	else:		#robot desvia a izquierda
		print('negro')
		motor_v_iz=1#motor_base+(correccion)
		motor_v_der=-1#-motor_base+(correccion)
	if il<3:
		motor_v_iz=0
		motor_v_der=0		
	return motor_v_iz, motor_v_der
#-------------------------------------------------------
def listener_talker():
	inicio=0	#variable que indica si se leyeron los valores de negro y blanco antes de iniciar los motores
	SensorData=sensor_data()
#--------Creacion de los nodos a utilizar----------
	rospy.init_node('listener_talker_color', anonymous=True)	# Creacion del nodo que se suscribe al sensor de color
	pub=rospy.Publisher('/ev3dev/OutPortA/command', Float64,queue_size=10)	# the node is publishing to the /ev3dev/OutPortA/command topic, motorA velocity
	pub2=rospy.Publisher('/ev3dev/OutPortB/command', Float64,queue_size=10)	# the node is publishing to the /ev3dev/OutPortB/command topic, motorB velocity
	pub3=rospy.Publisher('/ev3dev/OutPortC/command', Float64,queue_size=10)	# the node is publishing to the /ev3dev/OutPortC/command topic, motorC velocity
	rospy.Subscriber('color', Illuminance, SensorData.iluminacion)	#To read the color from sensor, the node is subscribed to /color topic
	rospy.Subscriber('ultrasonic', Range, SensorData.distancia)
	rate=rospy.Rate(10)
#Publicar-----------------------------------------------
	while not rospy.is_shutdown():
		'''if inicio==0:	#es necesario calibrar
			white, black, midpos = calibracion(SensorData.il)
			inicio=1	#Ya se calibro el sistema'''
		distancia_m=SensorData.dist
		print "distancia" , distancia_m
		rospy.loginfo(distancia_m)
		if distancia_m <= 0.10:# and distancia_m <= 0.125:	#the robot detect a box
			motor_v_iz = 0
			motor_v_der = 0
		 	rospy.loginfo(motor_v_iz)
	 		rospy.loginfo(motor_v_der)
			pub.publish(Float64(motor_v_iz))	# The velocity of motor A
		 	pub2.publish(Float64(motor_v_der))	# The velocity of motor B
			rospy.sleep(2)
			pub.publish(Float64(1))	# The velocity of motor A
		 	pub2.publish(Float64(1))	# The velocity of motor B
			rospy.sleep(1.8)
			pub.publish(Float64(0))	# The velocity of motor A
		 	pub2.publish(Float64(0))	# The velocity of motor B'''
			rospy.sleep(2)
			pub.publish(Float64(-1))	# The velocity of motor A
		 	pub2.publish(Float64(-1))	# The velocity of motor B
			rospy.sleep(2)
		else:
			motor_v_iz, motor_v_der = motors_velocity(SensorData.il,SensorData.dist)
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
