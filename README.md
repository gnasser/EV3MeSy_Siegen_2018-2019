# Automated Warehouse Robots
Build and program a LEGO robot using the Mindstorm Ev3 core set 45544 components.

<img src="https://le-www-live-s.legocdn.com/images/423923/live/sc/Products/5003400/5003400_1050x1050_1_xx-xx/63feb014132ef703a7e6d2c600b1d52d/2d9e36d3-afaf-4203-aa23-a58d00d7ca07/original/2d9e36d3-afaf-4203-aa23-a58d00d7ca07.jpg?fit=inside|855:640"  alt= "Diagrama de Bloques" height="400" width = "400"> 

The robot have to be capable to start at START point, drive to the loading station where it have to pick a box up, continue its path to the storage station where it have to leave the box to finally come back to the start point to reapeat the duty. The path is signalized by mean a black line on the floor and the robot follows the right border.

### Programming Specifications

 - Software development frame is ROS Indigo
 - Programming language is C++ or python
 - Hack4ROS EV3 Linux image as EV3 operating system ([more info](http://hacks4ros.github.io/h4r_ev3_ctrl/))
 
### Sensors

 - *Color sensor* reflect mode (0 black, 100 white) sensor_msgs.msg.Illuminance
 - *Ultrasonic sensor* distance mode (distance in meters) sensor_msgs.msg.Range
 
The implemented software frame was ROS Indigo in VirtualBox ([download image](https://nootrix.com/diy-tutos/ros-indigo-virtual-machine/)), However, it is also possible to work on Ubuntu 14.04.

As introductory form it is recommended to read this [slides](https://github.com/samirasancheze/EV3MeSy_Siegen_2018-2019/blob/master/Robot%20Operating%20System%20(ROS).pdf) and follow step by step the instructions so that the PC-robot conection be achieved and run the necessary nodes.

### Implementation 

The implemented code was [18_01_22_Control_general_class.py](https://github.com/samirasancheze/EV3MeSy_Siegen_2018-2019/blob/master/18_01_22_Control_general_class.py). To run it follow the [Step by Step](https://github.com/samirasancheze/EV3MeSy_Siegen_2018-2019/wiki/Step-by-Step) 

 - The builded design is the one showed in the picture, is important to mencion that the color and ultrasonic sensors are in the symetric axis of the robot, in case that the color sensor were placed in another part of the structure the algorithm could have to be modified.
#### Sensors

##### Color sensor
 - The color sensor sensor was used in reflect mode this mode can be modified changing teh mode parameter in this [file](https://github.com/samirasancheze/EV3MeSy_Siegen_2018-2019/blob/master/h4r_ev3_ctrl/h4r_ev3_launch/config/color.yaml), the sensor registers illuminances values between 0 (black) and 100 (white).
 - To inicialize the /color node, is needed to call roslaunch with the [file](https://github.com/samirasancheze/EV3MeSy_Siegen_2018-2019/blob/master/h4r_ev3_ctrl/h4r_ev3_launch/launch/color.launch) in which it have to be specified the file path where color.yaml is llocated.
 - The robot follow the right black line border due to we have only one color sensor.
 - Se tomaron medidas con el sensor de color en la fontera entre el negro y el blanco (midpos), en completamente blanco y completamente negro.
 - The robot moves forward at constant velocity when the sensor registers values near by midpos (midpos +-10). Otherwise, whether the robot is deviated to black it will turn right and if it is deviated to white will turn left in order to be again near by mispos. 
 
##### Ultrasonic sensor
 - The ultrasonic sensor was used in distance mode this mode can be modified changing this [file](https://github.com/samirasancheze/EV3MeSy_Siegen_2018-2019/blob/master/h4r_ev3_ctrl/h4r_ev3_launch/config/ultrasonic.yaml), the sensor registers (in meters) the distance between the robot and an obstacle.
 - To inicialize the /ultrasonic node, is needed to call roslaunch with the [file](https://github.com/samirasancheze/EV3MeSy_Siegen_2018-2019/blob/master/h4r_ev3_ctrl/h4r_ev3_launch/launch/ultrasonic.launch) in which it have to be specified the file path where ultrasonic.yaml is llocated.
 
 To inicialize the /color and /ultrasonic node at the same time, is needed to call roslaunch with the [file](https://github.com/samirasancheze/EV3MeSy_Siegen_2018-2019/blob/master/h4r_ev3_ctrl/h4r_ev3_launch/launch/sensors.launch) in which it have to be specified the file path where sensors.yaml is llocated. sensors.launch is a file where the sensors nodes are initialized and if it's needed to use another sensor could be added there. (see the [launch](https://github.com/samirasancheze/EV3MeSy_Siegen_2018-2019/tree/master/h4r_ev3_ctrl/h4r_ev3_launch/launch) and [config](https://github.com/samirasancheze/EV3MeSy_Siegen_2018-2019/tree/master/h4r_ev3_ctrl/h4r_ev3_launch/config) folder).
 
 [![Robot running](https://img.youtube.com/vi/dpWQEXYTF88/0.jpg)](https://www.youtube.com/watch?v=dpWQEXYTF88)
 
 
 

