Lane Detection
===============

El proposito del proyecto es sistema de detección de salidas de carril basado en visión por computador.
Se obtienen imágenes mediante una camara de vídeo situada en el vehiculo y posteriormente se testea el
algoritmo de detección fuera de la ejecución en tiempo real. En ausencia de las dos líneas en las zonas
laterales del campo de visión de la cámara, se da un aviso de salida de carril.

Instalación
===========

No es necesario instalar el programa, basta con descargarlo
para poder ejecutarlo. Para ver los requerimientos necesarios
para ejecutarlo correctamente, ver el archivo "INSTALL".


Uso
===

El programa inmediatmente empieza a procesar un video y aparece una ventana de reproduccion 
de lo que se esta obteniendo Al final de la ejecucion se guarda un archivo log 
contiene lo necesario para hacer un analisis de desempeño

Tiempo real o test de un video:

    True (Captura de una Webcam)
    False (Test desde un video)
    
Para correr el programa, en la terminal,una vez ubicado en el directorio raiz del proyecto
y escribir el comando:

    python Main.py [Nombre_video] [True o False]
    
Mas Informacion
===
[Blog personal](http://blog.rafaellopezgtz.com)

Proyecto final de la materia de Visión Computacional de la carrera Ingeniería en Tecnologías de Software, FIME, UANL.
Impartida por la Dra. Elisa Schaeffer en el periodo enero-agosto 2013


Fecha Actualizacion: 23 Mayo 2013
