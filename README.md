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

De forma introductoria se recomienda leer estas [diapositivas](https://github.com/samirasancheze/EV3MeSy_Siegen_2018-2019/blob/master/Robot%20Operating%20System%20(ROS).pdf) y seguir paso a paso las instrucciones para lograr conexión con el robot y tener instalados los paquetes necesarios para su control.
### Implementación 

El código implementado es el titulado [18_01_22_Control_general_class.py](https://github.com/samirasancheze/EV3MeSy_Siegen_2018-2019/blob/master/18_01_22_Control_general_class.py)

 - Se contruyó el diseño como el mostrado en la foto, en el que es importante destacar que el sensor de color y el ultrasónico están centrados en la estructura.
 
#### Sensor de color
 - El Sensor de color fue utilizado en modo reflect [en este archivo se modifica este modo](https://github.com/samirasancheze/EV3MeSy_Siegen_2018-2019/blob/master/h4r_ev3_ctrl/h4r_ev3_launch/config/color.yaml), es decir, del sensor se registran valores de iluminación entre 0 (negro absoluto) y 100 (blanco absoluto).
 - Para iniciar el nodo /color, en el que se inicializa el sensor de color se hace launch al [archivo](https://github.com/samirasancheze/EV3MeSy_Siegen_2018-2019/blob/master/h4r_ev3_ctrl/h4r_ev3_launch/launch/color.launch) en el que se debe especificar la ruta donde está almacenado el archivo color.yaml.
 - El robot sigue el borde derecho de la línea negra pues cuenta con un solo sensor de color.
 - Se tomaron medidas con el sensor de color en la fontera entre el negro y el blanco (midpos), en completamente blanco y completamente negro.
 - El robot se desplaza hacia adelante con velocidad constante cuando el sensor de color registra valores cercanos a midpos (midpos +-10). En caso contrario, de estar muy desviado hacia blanco o hacia negro, el robot gira entorno al centro del eje de las ruedas para volver a estar cercano al borde de la línea, hacia la derecha de estar en negro y hacia la izquierda de estar en blanco.
