import cv2 as cv
import numpy as np

#normalizar 
def normalize(a):
    return (a-np.min(a))/(np.max(a)-np.min(a))

class LineDetection():
    def __init__(self):
        #Valores RGB, HSV 
        self.avgRGB = [ 0.8888889,   0.99607843,  0.98823529 ]
        self.avgHSV = [ 1.75261841e+02,   1.07563006e-01,   9.96078432e-01 ]
        self.lineProbabilityMap = 0
        self.initialPoints = []

    def UpdateModelFromMask(self, mask, img, hsv):
        self.avgRGB = cv.mean(img, mask)[0:3]
        self.avgHSV = cv.mean(hsv, mask)[0:3]
        distMap = cv.distanceTransform(1-mask, cv.cv.CV_DIST_L2, 5)[0]
        self.lineProbabilityMap = (1.0/(1.0+0.1*distMap))    

    def InitializeFromImage(self, img, windowName):
        cv.imshow(windowName, img)
        cv.setMouseCallback(windowName, self.AddPoint, [img, windowName])
        cv.waitKey(0)
        
        #calcula el average de la linea
        hsv = np.float32(cv.cvtColor(img, cv.COLOR_RGB2HSV))
        
        if len(self.initialPoints)>0:
            lo = 20
            hi = 20
            flooded = np.uint8(img*255)
            largeMask = np.zeros((img.shape[0]+2, img.shape[1]+2), np.uint8)
            largeMask[:] = 0
            flags = cv.FLOODFILL_FIXED_RANGE
            cv.floodFill(flooded, largeMask, (self.initialPoints[0][1], self.initialPoints[0][0]), (0, 255, 0), (lo,), (hi,), flags)
            mask = largeMask[1:largeMask.shape[0]-1, 1:largeMask.shape[1]-1]
            cv.imshow(windowName, mask*255)
            self.UpdateModelFromMask(mask, img, hsv)
        cv.destroyWindow(windowName)
        
def main()
    pass


