import cv2 as cv
import numpy as np
from orientation import Lane
import serial, time 

AI = [0, 124, 637, 298]
RH = (0.8318770212301404, 0.784796499543384, 0.6864621111668014)
RS = (41.02017792349725, 0.17449159984689502, 0.832041028240797)

class LineDetector():
    def __init__(self, interes, x1, x2, color):
        self.lineorientation_Zs = []
        self.lineModel = None
        self.interes = None
        self.Initialize(interes, x1, x2, color)

    def Initialize(self, interes, x1, x2, color):
        self.interes = interes
        for iorientation_Z in range(0,50):
            orientation_Z = Lane()
            pos = x1 + iorientation_Z*(x2-x1)/(51)
            orientation_Z.config(pos,70)
            orientation_Z.colores(color.avgRGB, color.avgHSV,RH,RS)
            self.lineorientation_Zs.append(orientation_Z)
        try:   
            self.lineModel = np.poly1d(np.polyfit([x1[1], x2[1]], [x1[0], x2[0]], 1))
        except:
            pass 
    
    def LaneDetection(self, img, hsv, canny, outputImg, original):
        laneCoordinatesX = []
        laneCoordinatesY = []
        
        for orientation_Z in self.lineorientation_Zs:
            linesNumber, lineSegments, allSegments = orientation_Z.FindSegments(img, hsv, canny, outputImg, self.lineModel(orientation_Z.yPos))
            if linesNumber == 1:
                orientation_Z.update(img, hsv, lineSegments[0])
                laneCoordinatesY.append((lineSegments[0][0]+lineSegments[0][1])/2)
                laneCoordinatesX.append(orientation_Z.yPos)
            orientation_Z.line_Z(self.lineModel(orientation_Z.yPos))
        
        if len(laneCoordinatesX)>0:
            rank = True
            try:
                z = np.polyfit(laneCoordinatesX, laneCoordinatesY, 1)
            except np.RankWarning:
                rank = False
            if rank == True:
                tmpLineModel = np.poly1d(z) 
                self.lineModel = tmpLineModel
            
            self.lineModel = np.poly1d(np.polyfit(laneCoordinatesX, laneCoordinatesY, 1))
            for orientation_Z in self.lineorientation_Zs:
                cv.circle(outputImg, (int(self.lineModel(orientation_Z.yPos)), orientation_Z.yPos), 2, [200, 0, 100], 3)
        self.drawn(original, img)

    def drawn(self, original, img):
        #arduino = serial.Serial('/dev/tty.usbmodem1411', 9600)
        #time.sleep(1) # waiting the initialization...
        val_orientation = int(self.lineModel(100))
        #final de un punto
        orientationColor = [0, 255, 0]
        #se dibuja en la pantalla la orientacion hacia la izquierda
        if val_orientation < img.shape[1]/2: 
            if 130 < val_orientation: 
                cv.line(original, (img.shape[1]/2,50), (img.shape[1]/2-25,75),(0,128,255), 15)
                cv.line(original, (img.shape[1]/2,100), (img.shape[1]/2-25,75),(0,128,255), 15)
                #arduino.write('R')
                #time.sleep(1) 
                print "Orientacion: Hacia la Izquierda"
        #se dibuja en la pantalla la orientacion hacia la derecha
        if val_orientation > img.shape[1]/2: 
            if val_orientation < 550: 
                cv.line(original, (img.shape[1]/2,50), (img.shape[1]/2+25,75),(0,128,255), 15)
                cv.line(original, (img.shape[1]/2,100), (img.shape[1]/2+25,75),(0,128,255), 15)
                #arduino.write('L')
                print "Orientacion: Hacia la Derecha"
        cv.line(original, (self.interes[0]+int(self.lineModel(0)), self.interes[1]+0), (self.interes[0]+int(self.lineModel(img.shape[0])), self.interes[1]+img.shape[0]), [0, 255, 0], 4)        

