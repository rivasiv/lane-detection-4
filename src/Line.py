import cv2 as cv
import numpy as np
from marcador import marcador
import serial, time 



class Line():
    def __init__(self, crop, marcsNumber, marcsWidth, lineStart, lineEnd, mod_col):
        self.linemarcs = []
        self.lineModel = None
        self.crop = None
        self.Initialize(crop, marcsNumber, marcsWidth, lineStart, lineEnd, mod_col)

    def Initialize(self, crop, marcsNumber, marcsWidth, lineStart, lineEnd, mod_col):
        self.crop = crop
        for imarc in range(0, marcsNumber):
            marc = Lanemarc()
            pos = lineStart + imarc*(lineEnd-lineStart)/(marcsNumber+1)
            marc.SetGeometry(pos, marcsWidth)
            marc.InitializeModel(mod_col.avgRGB, mod_col.avgHSV, (0.8318770212301404, 0.784796499543384, 0.6864621111668014), (41.02017792349725, 0.17449159984689502, 0.832041028240797))
            self.linemarcs.append(marc)
        try:   
            self.lineModel = np.poly1d(np.polyfit([lineStart[1], lineEnd[1]], [lineStart[0], lineEnd[0]], 1))
        except:
            pass 
    
    def LaneDetection(self, img, hsv, canny, outputImg, outputFull):
        laneCoordinatesX = []
        laneCoordinatesY = []
        for marc in self.linemarcs:
            linesNumber, lineSegments, allSegments = marc.FindSegments(img, hsv, canny, outputImg, self.lineModel(marc.yPos))
            if linesNumber == 1:
                marc.UpdatePositionAndModelFromRegion(img, hsv, lineSegments[0])
                laneCoordinatesY.append((lineSegments[0][0]+lineSegments[0][1])/2)
                laneCoordinatesX.append(marc.yPos)
            marc.UpdatePositionIfItIsFarAway(self.lineModel(marc.yPos))
        
        if len(laneCoordinatesX)>0:
            rank = 'ok'
            try:
                z = np.polyfit(laneCoordinatesX, laneCoordinatesY, 1)
            except np.RankWarning:
                rank = 'bad'
            except:
                pass
            if rank == 'ok':
                tmpLineModel = np.poly1d(z) 
                self.lineModel = tmpLineModel
            
            self.lineModel = np.poly1d(np.polyfit(laneCoordinatesX, laneCoordinatesY, 1))
            for marc in self.linemarcs:
                cv.circle(outputImg, (int(self.lineModel(marc.yPos)), marc.yPos), 2, [200, 0, 100], 3)
        self.CheckLinePositionAndDrawOutput(outputFull, img)

    def CheckLinePositionAndDrawOutput(self, outputFull, img):
        arduino = serial.Serial('/dev/tty.usbmodem1411', 9600)
        time.sleep(1) # waiting the initialization...

        lineX = np.array([0,255,0])/1.0

        color_lineX = np.array([0,128,255])/1.0
        
        testLeftLineXAlert = 130
        testRightLineXAlert = 550

        testLeftLineY = 100
        
        #Buscando intereseccion de los bordes
        testLeftLineIntersection = int(self.lineModel(testLeftLineY))      

        #marca el punto final
        orientation = 'Ok'
        orientationColor = [0, 255, 0]

        if testLeftLineIntersection < img.shape[1]/2: 
            if testLeftLineXAlert < testLeftLineIntersection: 
                orientation = 'AlertLeft'
                orientationColor = color_lineX

        if testLeftLineIntersection > img.shape[1]/2: 
            if testLeftLineIntersection < testRightLineXAlert: 
                orientation = 'AlertRight'
                orientationColor = color_lineX
    
        #linea
        cv.line(outputFull, (self.crop[0]+int(self.lineModel(0)), self.crop[1]+0), (self.crop[0]+int(self.lineModel(img.shape[0])), self.crop[1]+img.shape[0]), [255, 0, 0], 2)        
        cv.line(outputFull, (self.crop[0]+0,self.crop[1]+testLeftLineY) , (self.crop[0]+img.shape[1],self.crop[1]+testLeftLineY), [0.2,0.2,0.2])
        #Draw Left
        cv.line(outputFull, (self.crop[0]+0,self.crop[1]+testLeftLineY) , (self.crop[0]+testLeftLineXAlert,self.crop[1]+testLeftLineY), lineX, 2)
        cv.line(outputFull, (self.crop[0]+testLeftLineXAlert,self.crop[1]+testLeftLineY) , (self.crop[0]+testLeftLineXDanger,self.crop[1]+testLeftLineY), color_lineX, 2)
        cv.line(outputFull, (self.crop[0]+testLeftLineXDanger,self.crop[1]+testLeftLineY) , (self.crop[0]+img.shape[1]/2,self.crop[1]+testLeftLineY), testLineXDangerColor, 2)
        #Draw Right
        cv.line(outputFull, (self.crop[0]+img.shape[1],self.crop[1]+testLeftLineY) , (self.crop[0]+testRightLineXAlert,self.crop[1]+testLeftLineY), lineX, 2)
        cv.line(outputFull, (self.crop[0]+testRightLineXAlert,self.crop[1]+testLeftLineY), (self.crop[0]+testRightLineXDanger,self.crop[1]+testLeftLineY), color_lineX, 2)
        cv.line(outputFull, (self.crop[0]+testRightLineXDanger,self.crop[1]+testLeftLineY), (self.crop[0]+img.shape[1]/2,self.crop[1]+testLeftLineY), testLineXDangerColor, 2)
        #intersection
        cv.circle(outputFull, (self.crop[0]+testLeftLineIntersection, self.crop[1]+testLeftLineY), 2, orientationColor, 4)
        #alerts


        if orientation == 'AlertLeft':
            cv.line(outputFull, (img.shape[1]/2,50), (img.shape[1]/2-25,75), orientationColor, 15)
            cv.line(outputFull, (img.shape[1]/2,100), (img.shape[1]/2-25,75), orientationColor, 15)
            arduino.write('R')
            time.sleep(1) 
            print "Orientacion: Hacia la Izquierda"

        if orientation == 'AlertRight' :
            cv.line(outputFull, (img.shape[1]/2,50), (img.shape[1]/2+25,75), orientationColor, 15)
            cv.line(outputFull, (img.shape[1]/2,100), (img.shape[1]/2+25,75), orientationColor, 15)
            arduino.write('L')
            print "Orientacion: Hacia la Derecha"

        #if orientation != 'AlertRight':
            #cv.line(outputFull, (img.shape[1]/2,50), (img.shape[1]/2+25,75), orientationColor, 15)
            #cv.line(outputFull, (img.shape[1]/2,100), (img.shape[1]/2+25,75), orientationColor, 15)    
            #time.sleep(1) 
            #print "En direccion recta"

        arduino.close() 
