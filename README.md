# Robot para almacenaje automatizado

La finalidad de este proyecto es construir y programar un robot de almacen utilizando los componentes del Mindstorm Ev3 core set 45544

<img src="https://le-www-live-s.legocdn.com/images/423923/live/sc/Products/5003400/5003400_1050x1050_1_xx-xx/63feb014132ef703a7e6d2c600b1d52d/2d9e36d3-afaf-4203-aa23-a58d00d7ca07/original/2d9e36d3-afaf-4203-aa23-a58d00d7ca07.jpg?fit=inside|855:640"  alt= "Diagrama de Bloques" height="400" width = "400"> 

El robot debe ser capaz de iniciar el un punto de partida (START), dirigirse a la estación de carga (LOADING) donde debe recoger una caja, contuniar su camino hasta el almacen (STORAGE) donde debe dejar la caja para finalmente volver al punto de partida y repetir la tarea. El camino está indicado con una línea negra en el suelo y el robot ha sido programado para seguir el borde derecho de esta línea.

### Especificaciones de programación

 - ROS como frame de desarrollo de software
 - Los códigos desarrollados se hicieron en python
 - En el robot se corre la imagen Hack4ROS EV3 Linux como sistema operativo ([mas info](http://hacks4ros.github.io/h4r_ev3_ctrl/))
 
### Sensores utilizados

 - Sensor de color en modo reflect (0 negro, 100 blanco) sensor_msgs.msg.Illuminance
 - Sensor ultrasonico en modo distance (distancia en metros) sensor_msgs.msg.Range
 
Se trabajó con ROS Indigo en una máquina virtual ([descargar imagen](https://nootrix.com/diy-tutos/ros-indigo-virtual-machine/)), sin embargo también se puede trabajar directamente con una PC donde se tenga Ubuntu 14.04

As introductory form it is recommended to read the [slises](https://github.com/samirasancheze/EV3MeSy_Siegen_2018-2019/blob/master/Robot%20Operating%20System%20(ROS).pdf) and follow step by step the instructions so that the PC-robot conection be achieved and run the necessary nodes.

### Implementación 

the implemented code was [18_01_22_Control_general_class.py](https://github.com/samirasancheze/EV3MeSy_Siegen_2018-2019/blob/master/18_01_22_Control_general_class.py)

 - The builded design is the one showed in the picture, is important to mencion that the color and ultrasonic sensors are in the symetric axis of the robot, in case that the color sensor were placed in another part of the structure the algorithm could have to be modified.
 
#### Sensor de color
 - The color sensor sensor was used in reflect mode [this mode can be modified changing this file](https://github.com/samirasancheze/EV3MeSy_Siegen_2018-2019/blob/master/h4r_ev3_ctrl/h4r_ev3_launch/config/color.yaml), the sensor registers illuminances values between 0 (black) and 100 (white).
 - To inicialize the /color node, is needed to call roslaunch with the [file](https://github.com/samirasancheze/EV3MeSy_Siegen_2018-2019/blob/master/h4r_ev3_ctrl/h4r_ev3_launch/launch/color.launch) in which it have to be specified the file path where color.yaml is llocated.
 - The robot follow the right black line border due to we have only one color sensor.
 - Se tomaron medidas con el sensor de color en la fontera entre el negro y el blanco (midpos), en completamente blanco y completamente negro.
 - The robot moves forward at constant velocity when the sensor registers values near by midpos (midpos +-10). Otherwise, whether the robot is deviated to black it will turn right and if it is deviated to white will turn left in order to be again near by mispos. 
 
#### Ultrasonic sensor
 - The ultrasonic sensor was used in distance mode [this mode can be modified changing this file](https://github.com/samirasancheze/EV3MeSy_Siegen_2018-2019/blob/master/h4r_ev3_ctrl/h4r_ev3_launch/config/ultrasonic.yaml), the sensor registers (in meters) the distance between the robot and an obstacle. 
 - Se 
 
