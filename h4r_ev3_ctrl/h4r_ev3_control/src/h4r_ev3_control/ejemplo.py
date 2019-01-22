#!/usr/bin/env python

## Simple talker demo that listens to std_msgs/Strings published 
## to the 'chatter' topic

import rospy
from sensor_msgs.msg import Illuminance	# Sensor library
from std_msgs.msg import String
from std_msgs.msg import Float64
motor_v=0	#velocidad de motor
#Se agrega el Publisher---------------------------------
pub=rospy.Publisher('/ev3dev/OutPortA/command', Float64,queue_size=10)
pub2=rospy.Publisher('/ev3dev/OutPortB/command', Float64,queue_size=10)
#-------------------------------------------------------

def callback(data):
#-------------------------------------------------------
    global motor_v
#-------------------------------------------------------
    #rospy.loginfo('I heard %s', data.illuminance)
    il=data.illuminance	#illuminance number 0 (dark) to 100 (bright)
    w=raw_input()
    if (w == "w"):
       blanco = il
       print blanco

    elif (w == "b"):
       negro=il
       print negro

    if il > 50 :
      print('blanco')
      motor_v=0
    else:
      print('negro')
      motor_v=10
#Introduccion de los datos a mandar---------------------
    rospy.loginfo(motor_v)
    pub.publish(Float64(motor_v))
    pub2.publish(Float64(motor_v))
#-------------------------------------------------------
  
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)
    #rospy.init_node('talker', anonymous=True) #
    rospy.Subscriber('color', Illuminance, callback)
#Publicar-----------------------------------------------
    pub.publish(Float64(motor_v))
    pub2.publish(Float64(motor_v))
#-------------------------------------------------------
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
    #Talker - Motores

if __name__ == '__main__':
    listener()

