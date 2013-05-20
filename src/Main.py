import cv2 as cv
import points as dr
import numpy as np
import time
from orientation import orientation
from lanedetection import LaneDetection


log = open("log.txt","w")
log.close()
#Parametros del filtro de canny
CAN_L = 70
CAN_R = 170
#Archivo de entrada para pruebas
File_Test = "video5.mp4"
#Captura de camara en tiempo real
REALTIME = False
DEVICE = 0
UMBRAL_H = 200
UMBRAL_L = 255
#Iniciando lectura de frames
if REALTIME == True:
    capture = cv.VideoCapture(DEVICE) #6 7 8
    print "Modo video captura "
else:
    capture = cv.VideoCapture(File_Test)
    print "Modo de prueba"

if capture.isOpened() == False:
    print "Error al Abrir el Archivo de entrada"
    exit()


#Parametros de la imagen 
cropArea = [0, 124, 637, 298]
sensorsNumber = 50
sensorsWidth = 70

#inicio y final de las lineas
line1LStart = np.array([35, 128])
line1LEnd = np.array([220, 32])
line1RStart = np.array([632, 146])
line1REnd = np.array([476, 11])

#Obtener el primer frame para el modelo de color
flag, imgFull = capture.read()
img = imgFull[cropArea[1]:cropArea[3], cropArea[0]:cropArea[2]]

#Initialize left lane
leftLineColorModel = LaneMarkersModel()
leftLine = LineDetector(cropArea, sensorsNumber, sensorsWidth, line1LStart, line1LEnd, leftLineColorModel)

#Initialize right lane
rightLineColorModel = LaneMarkersModel()
#rightLineColorModel.InitializeFromImage(np.float32(img)/255.0, "Select right line")
rightLine = LineDetector(cropArea, sensorsNumber, sensorsWidth, line1RStart, line1REnd, rightLineColorModel)

Frame_ = 0
fr = 0
lista=[]
while(cv.waitKey(1) != 27):
    start_time = time.time()
    Frame_+=1

    #print Frame_
    #Leer y cortar en esta parte del procesos se corta el horizonte y algunas partes
    #que puedan proporcionar ruido para la imagen
    flag, imgFull = capture.read()
    if flag == False: break 

    #Pre-procesamiento
    #se recorta el area de la imagen
    #cv.Smooth(grayscale,grayscale,cv.CV_MEDIAN)
    #cv.Threshold(grayscale,grayscale,80,200,cv.CV_THRESH_BINARY)
    #cv.Threshold(grayscale,grayscale,80, 255, cv.CV_THRESH_BINARY | cv.CV_THRESH_OTSU);
    grayImage = cv.cvtColor(np.uint8(img*255), cv.COLOR_RGB2GRAY)
    img = cv.threshold(grayImage,UMBRAL_H,UMBRAL_L,cv.THRESH_BINARY)
    img = np.float32(imgFull[cropArea[1]:cropArea[3], cropArea[0]:cropArea[2]])/255.0
    #para convertir la imagen a HSV
    hsv = np.float32(cv.cvtColor(img, cv.COLOR_RGB2HSV))
    #Pasando la imagen a filtros de canny
    #cv.Canny(grayscale, dst, 40, 200, 3)
    #cv.Canny(grayscale, dst,low_threshold,low_threshold*3)
    #grayImage = cv2.cvtColor(sourceImage, cv2.COLOR_RGB2GRAY)
    #fil = cv.threshold(cv.cvtColor(np.uint8(img*255)), cv.COLOR_RGB2GRAY,UMBRAL_H,UMBRAL_L,cv.THRESH_BINARY)
    #canny = cv.Canny(cv.cvtColor(np.uint8(img*255), cv.COLOR_RGB2GRAY),CAN_L,CAN_R)
    canny = cv.Canny(cv.cvtColor(np.uint8(img*255), cv.COLOR_RGB2GRAY),90,90*3)
 
    #Salida de las imagenes 
    outputImg = img.copy()
    post = imgFull.copy()
    
    #Mostrando la salida de las imagenes 
    cv.imshow("Output", canny)
    cv.imshow("Lane deteccion", post)
    log = open("log.txt","a")
    t = time.time() - start_time
    lista.append(t)
    tp = sum(lista) / len(lista)
    log.write(str(Frame_)+" "+str(t)+" "+str(tp)+"\n")
    log.close()
    #Video con procesamiento
    videoWriter.write(post)
print "Frames Analizados: ",Frame_
print "Tiempo de ejecucion"
cv.destroyAllWindows()
