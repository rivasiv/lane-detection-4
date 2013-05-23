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

Ejecución
=========

Para correr el programa, en la terminal,
una vez ubicado en el directorio raiz del proyecto
y escribir el comando:

    python Main.py [Nombre_video] 


Uso
===

El programa inmediatmente empieza a procesar un video y aparece una ventana de reproduccion 
de lo que se esta obteniendo Al final de la ejecucion se guarda un archivo log 
contiene lo necesario para hacer un analisis de desempeño

Configuracion Tiempo real o test de un video:

    REALTIME : True (Captura de una Webcam)
    REALTIME : False (Test desde un video)

[blog](http://blog.rafaellopezgtz.com)
