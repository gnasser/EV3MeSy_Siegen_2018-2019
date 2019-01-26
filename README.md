# Robot para almacenaje automatizado

La finalidad de este proyecto es construir y programar un robot de almacen utilizando los componentes del Mindstorm Ev3 core set 45544

<img src="https://le-www-live-s.legocdn.com/images/423923/live/sc/Products/5003400/5003400_1050x1050_1_xx-xx/63feb014132ef703a7e6d2c600b1d52d/2d9e36d3-afaf-4203-aa23-a58d00d7ca07/original/2d9e36d3-afaf-4203-aa23-a58d00d7ca07.jpg?fit=inside|855:640"  alt= "Diagrama de Bloques" height="400" width = "400"> 

El robot debe ser capaz de iniciar el un punto de partida (START), dirigirse a la estación de carga (LOADING) donde debe recoger una caja, contuniar su camino hasta el almacen (STORAGE) donde debe dejar la caja para finalmente volver al punto de partida y repetir la tarea. El camino está indicado con una línea negra en el suelo y el robot ha sido programado para seguir esta línea.

### Especificaciones de programación

 - ROS como frame de desarrollo de software
 - Los códigos desarrollados se hicieron en python
 - En el robot se corre la imagen Hack4ROS EV3 Linux como sistema operativo ([mas info](http://hacks4ros.github.io/h4r_ev3_ctrl/))
 
Se trabajó con ROS Indigo en una máquina virtual ([descargar imagen](https://nootrix.com/diy-tutos/ros-indigo-virtual-machine/)), sin embargo también se puede trabajar directamente con una PC donde se tenga Ubuntu 14.04

De forma introductoria se recomienda leer estas [diapositivas](https://github.com/samirasancheze/EV3MeSy_Siegen_2018-2019/blob/master/Robot%20Operating%20System%20(ROS).pdf) y seguir paso a paso las instrucciones para lograr conexión con el robot y tener instalados los paquetes necesarios para su control.

El código implementado es el titulado,
 - Se contruyó el diseño como el mostrado en la foto.
 - El Sensor de color fue utilizado en modo reflexión, del sensor se recibe un mensaje de tipo std_sensor.Illuminance y los valores registrados de iluminancia están entre 0 (negro absoluto) y 100 (blanco absoluto).
 - El robot sigue el borde derecho de la línea negra pues cuenta con un solo sensor de color.
 - Se tomaron medidas con el sensor de color en la fontera entre el negro y el blanco (midpos), en completamente blanco y completamente negro.
 - El robot se desplaza hacia adelante con velocidad constante cuando el sensor de color registra valores cercanos a midpos (midpos +-10). En caso contrario, de estar muy desviado hacia blanco o hacia negro, el robot gira entorno al centro del eje de las ruedas para volver a estar cercano al borde de la línea, hacia la derecha de estar en negro y hacia la izquierda de estar en blanco.
 - Las desviaciones des robot respecto a la trayectoria deseada se efectua
