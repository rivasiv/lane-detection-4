Lane Detection
===============

El proposito del proyecto es sistema de detección de salidas de carril basado en visión por computador.
Se obtienen imágenes mediante una camara de vídeo situada en el vehiculo y posteriormente se testea el
algoritmo de detección fuera de la ejecución en tiempo real. En ausencia de las dos líneas en las zonas
laterales del campo de visión de la cámara, se da un aviso de salida de carril.


Uso
===

Tiempo real o test de un video:

    True (Captura de una Webcam)
    VIDEO (Nombre del video y su extencion)
    Ejemplo de test video : python Main.py video.mp4
    Ejemplo test realtime : python Main.py True

    
Para correr el programa, en la terminal,una vez ubicado en el directorio raiz del proyecto
y escribir el comando:

    python Main.py [OPCION] 
  
En el archivo log.txt ubicado en src/ se encuentran el tiempo que se tarda en 
procesar por frame asi como el tiempo promedio

Ejemplo:
===
Ejecución de un ejemplo 

    python ./src/Main.py ./test/009-1.mp4 
    
    
Acerca de :
===
Mas información sobre el proyecto:
[Blog personal](http://blog.rafaellopezgtz.com)

Proyecto de Visión Computacional de la carrera Ingeniería en Tecnología de Software en la Facultad de Ingeniería Mecanica 
y Eléctrica,Impartida por la Dra. Elisa Schaeffer.


Fecha Actualizacion: 25 Mayo 2013
