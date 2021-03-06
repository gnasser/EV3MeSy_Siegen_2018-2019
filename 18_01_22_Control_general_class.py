#!/usr/bin/env python

##proporcional 1: sigue la linea y hace cruces 90 grados negro a la izquierda y cruces en esquinas cerrado calibraciones hechas es el laboratorio
#Se esta reeatructurando el c'odigo para que acepte distintos sensores
##Lee sensores de proximidad y color, tiene topico para publicar a motor que mueve el brazo
# se corrige la trayectoria solo girando en torno al centro de masa del robot si se desvia un poco del centro de la linea
# Al encontrar un obstaculo a 12cm se detiene, baja brazo, avanza un poco, sube brazo y luego gira a la izquierda para seguir el algoritmo de linea
# Al llegar al almacen se detiene, baja brazo, retrocede, sube brazo, gira a la izquierda para seguir el algoritmo de seguir linea.

import rospy
from sensor_msgs.msg import Illuminance	# color Sensor library
from sensor_msgs.msg import Range	# ultrasonic Sensor library
from std_msgs.msg import String
from std_msgs.msg import Float64
import time

motor_v_L=0	# velocidad de motor
motor_v_R=0	# velocidad de motor
inicio=0

#Se agrega el Publisher---------------------------------

#-------------------------------------------------------

class sensor_data:	# En esta clase se almacenan los datos recibidos por los sensores
	def __init__(self):	#Creacion de la clase	
		self.il=0.0		#En il se almacena el valor de la iluminancia recibida por el sensor de color
		self.dist=0.5
		self.caja=0
	def iluminacion (self,data):
		self.il=data.illuminance # Recibido un valor de iluminacion, actualizacion del dato. illuminance number 0 (dark) to 100 (bright)
		return self.il
	def distancia(self,data):
		self.dist=data.range
		return self.dist
#--------------------------------------------------------
def motors_velocity(il,dist):
	motor_base=1.4
	if il < 30 and il > 13 :	# robot sigue derecho
		motor_v_L=motor_base
		motor_v_R=motor_base
	elif il >= 30:	# robot desvia a derecha
		print('blanco')
		motor_v_L=-1
		motor_v_R= 1		
	else:		#robot desvia a izquierda
		print('negro')
		motor_v_L=1#motor_base+(correccion)
		motor_v_R=-1#-motor_base+(correccion)
	if il<3:
		motor_v_L=0
		motor_v_R=0		
	return motor_v_L, motor_v_R
#-------------------------------------------------------
def listener_talker():
	inicio=0	#variable que indica si se leyeron los valores de negro y blanco antes de iniciar los motores
	SensorData=sensor_data()
	delay_palanca=3.4
#--------Creacion de los nodos a utilizar----------
	rospy.init_node('listener_talker_color', anonymous=True)	# Creacion del nodo que se suscribe al sensor de color
	pub_motor_L=rospy.Publisher('/ev3dev/OutPortA/command', Float64,queue_size=10)	# the node is publishing to the /ev3dev/OutPortA/command topic, motorL velocity
	pub_motor_R=rospy.Publisher('/ev3dev/OutPortB/command', Float64,queue_size=10)	# the node is publishing to the /ev3dev/OutPortB/command topic, motorR velocity
	pub_motor_C=rospy.Publisher('/ev3dev/OutPortC/command', Float64,queue_size=10)	# the node is publishing to the /ev3dev/OutPortC/command topic, motorC velocity
	rospy.Subscriber('color', Illuminance, SensorData.iluminacion)	#To read the color from sensor, the node is subscribed to /color topic
	rospy.Subscriber('ultrasonic', Range, SensorData.distancia)
	rate=rospy.Rate(10)
#Publicar-----------------------------------------------
	while not rospy.is_shutdown():
		distancia_m=SensorData.dist
		print "distancia" , distancia_m
		rospy.loginfo(distancia_m)
		if distancia_m <= 0.11:# and distancia_m <= 0.125:	#the robot detect a box
			if SensorData.caja==0:
				pub_motor_L.publish(Float64(0))		# The velocity of motor A
			 	pub_motor_R.publish(Float64(0))	# The velocity of motor B
				rospy.sleep(.5)
				# baja palanca
				pub_motor_C.publish(Float64(-1))	# The velocity of motor B
				rospy.sleep(delay_palanca)
				pub_motor_C.publish(Float64(0))	# The velocity of motor B
				rospy.sleep(1)
				# Avanza hacia adelante
				pub_motor_R.publish(Float64(1))	# The velocity of motor B
				pub_motor_L.publish(Float64(1))		# The velocity of motor A
				rospy.sleep(2)
				pub_motor_L.publish(Float64(0))		# The velocity of motor A
			 	pub_motor_R.publish(Float64(0))	# The velocity of motor B
				rospy.sleep(1)
				# sube la palanca
				pub_motor_C.publish(Float64(1))	# The velocity of motor C
				rospy.sleep(delay_palanca)
				pub_motor_C.publish(Float64(0))	# The velocity of motor C
				rospy.sleep(1)
				# gira hacia izquierda
				pub_motor_L.publish(Float64(-1.4))	# The velocity of motor A
			 	pub_motor_R.publish(Float64( 1.4))	# The velocity of motor B
				rospy.sleep(2)
				SensorData.caja=1
			else:
				pub_motor_L.publish(Float64(0))		# The velocity of motor A
			 	pub_motor_R.publish(Float64(0))		# The velocity of motor B
				rospy.sleep(.5)
				# baja palanca
				pub_motor_C.publish(Float64(-1))	# The velocity of motor B
				rospy.sleep(delay_palanca)
				pub_motor_C.publish(Float64(0))	# The velocity of motor B
				rospy.sleep(1)
				# retrocede
				pub_motor_L.publish(Float64(-1))	# The velocity of motor A
			 	pub_motor_R.publish(Float64(-1))	# The velocity of motor B
				rospy.sleep(1.7)
				pub_motor_L.publish(Float64(0))	# The velocity of motor A
			 	pub_motor_R.publish(Float64(0))	# The velocity of motor B
				rospy.sleep(0.5)
				# sube la palanca
				pub_motor_C.publish(Float64(1))	# The velocity of motor C
				rospy.sleep(delay_palanca)
				pub_motor_C.publish(Float64(0))	# The velocity of motor C
				rospy.sleep(1)
				# gira hacia izquierda
				pub_motor_L.publish(Float64(-1.4))	# The velocity of motor A
			 	pub_motor_R.publish(Float64( 1.4))	# The velocity of motor B
				rospy.sleep(2)
				SensorData.caja=0
		else:
			motor_v_L, motor_v_R = motors_velocity(SensorData.il,SensorData.dist)
			rospy.loginfo(motor_v_L)
	 		rospy.loginfo(motor_v_R)
			pub_motor_L.publish(Float64(motor_v_L))	# The velocity of motor A
		 	pub_motor_R.publish(Float64(motor_v_R))	# The velocity of motor B
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
