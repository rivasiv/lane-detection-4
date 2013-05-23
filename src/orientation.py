import cv2 as cv
import numpy as np

class Lane():
    def __init__(self):
        xyz = [0,0,0]
        self.xPos = 0
        self.yPos = 0
        self.width = 0
        self.lineRGB = xyz
        self.lineHSV = xyz
        self.lineWidth = [0, 0]
        self.roadRGB = xyz
        self.roadHSV = xyz
        self.avgRGB = [ 0.8888889,0.99607843,  0.98823529 ]
        self.avgHSV = [ 1.75261841e+02,1.07563006e-01,9.96078432e-01 ]
        self.lineProbabilityMap = 0
        self.initialPoints = []

    def config(self, position, width):
        self.xPos = max(0, position[0]-width/2)
        self.yPos = position[1] 
        self.width = width

    
    def colores(self, linergb, linehsv, roadrgb, roadhsv):
        self.lineRGB = linergb
        self.lineHSV = linehsv
        self.roadRGB = roadrgb
        self.roadHSV = roadhsv

    def probabilidad_(self, rgb, hsv):
        #Calculamos la distancia RGB
        rgbLaneError = np.abs(rgb - self.lineRGB)
        rgbLaneDistance = np.sqrt(np.square(rgbLaneError[:,0])+np.square(rgbLaneError[:,1])+np.square(rgbLaneError[:,2]))/3.0

        HLaneError = np.abs(hsv - self.lineHSV)[:, 0]/360.0
        
        #probabilidad y relatividad
        probability = 1.0-(1.0*rgbLaneDistance + 0.0*HLaneError)/1.0
        reliability = np.ones_like(probability)
        
        return (probability, reliability)
       
    def FindSegments(self, rgbGlobal, hsvGlobal, cannyGlobal, outputImg, previousLineCenterPosition):
        #cortamos la imagen a nuestra medida para hacer calculo de orientacion usando como parametros
        #canny y por colores
        rgb = rgbGlobal[self.yPos, self.xPos:(self.xPos+self.width)]
        hsv = hsvGlobal[self.yPos, self.xPos:(self.xPos+self.width)]
        canny = cannyGlobal[self.yPos, self.xPos:(self.xPos+self.width)]

        probability, reliability = self.probabilidad_(rgb, hsv)
        if canny.shape[0] == 0: return [0, [], []]
        segStart = 0
        while canny[segStart] == 0: #find start of a first segment
            segStart+=1 
            if segStart == canny.shape[0]:
                break
            
        #find Canny segments
        segments = []
        segmentProbability = 0

        for x in range(1, canny.shape[0]):
            if canny[x] > 0 and (x - segStart) > 2: 
                segmentProbability = np.average(probability[segStart:x])
                segments.append([segStart, x, segmentProbability])
                segStart = x
        
        #Buscamos segmentos de lineas
        lineSegments = []
        for seg in segments:
            segmentProbability = seg[2]
            if segmentProbability > 0.85:
                segmentProbability = 1
            else:
                segmentProbability = 0
            
            #ancho de linea 
            if self.lineWidth[1] > 10: 
                if abs((seg[1]-seg[0])-self.lineWidth[0]/self.lineWidth[1]) > 5+50/self.lineWidth[1]:
                    segmentProbability = 0
                    
            cv.line(outputImg, (self.xPos+seg[0], self.yPos), (self.xPos+seg[1], self.yPos), [segmentProbability, segmentProbability, 0], 1)
            if(segmentProbability == 1):
                lineSegments.append([self.xPos+seg[0], self.xPos+seg[1]])
        
        lineCenter = previousLineCenterPosition-self.xPos
        if len(lineSegments) == 0 and len(segments) >= 3: 
            #En esta parte se busca si el segmento cumple las condiciones y se actualiza
            for seg in segments:
                if(seg[0] <= lineCenter and seg[1] >= lineCenter and self.lineWidth[1] > 10): 
                    if abs((seg[1]-seg[0])-self.lineWidth[0]/self.lineWidth[1]) < 10:
                        lineSegments.append([self.xPos+seg[0], self.xPos+seg[1]])
        
        return (len(lineSegments), lineSegments, segments)

    def update(self, rgbGlobal, hsvGlobal, region):
        x1 = region[0]
        x2 = region[1]
        self.xPos = max(0, x1 - (self.width - (x2-x1))/2)
        rgb = rgbGlobal[self.yPos, x1:x2]
        hsv = hsvGlobal[self.yPos, x1:x2]
        self.lineRGB = [np.average(rgb[:, 0]), np.average(rgb[:, 1]), np.average(rgb[:, 2])]
        self.lineHSV = [np.average(hsv[:, 0]), np.average(hsv[:, 1]), np.average(hsv[:, 2])]
        self.lineWidth[0]+= x2-x1 
        self.lineWidth[1]+= 1 
        
    def line_Z(self, previousLineCenterPosition):
        if abs(previousLineCenterPosition - self.xPos+self.width/2) > 20:
            self.xPos = int(max(0, previousLineCenterPosition - self.width/2))
        
