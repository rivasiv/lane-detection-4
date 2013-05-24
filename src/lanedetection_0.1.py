import sys
import time
import cv
import math

VIDEO = sys.argv[1]
#Valores de umbral de Threshold
UMBRAL_H = 200
UMBRAL_L = 255
#Valores de Hough

#cascade = cv.Load('frontalface10/haarcascade_frontalface_alt.xml')

def detect(image):
    image_size = cv.GetSize(image)
    # create grayscale version
    grayscale = cv.CreateImage(image_size, 8, 1)
    dst = cv.CreateImage(image_size, 8, 1)
    cv.Smooth(grayscale, dst, cv.CV_GAUSSIAN, 5, 5)
    #blur = cv.GaussianBlur(dst, (5, 5), 0)
    cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)
    #cv.Smooth(grayscale,grayscale,cv.CV_MEDIAN)
    #cv.Threshold(grayscale,grayscale,80,200,cv.CV_THRESH_BINARY)
    #cv.Threshold(grayscale,grayscale,80, 255, cv.CV_THRESH_BINARY | cv.CV_THRESH_OTSU);
    cv.Threshold(grayscale,grayscale,UMBRAL_H,UMBRAL_L,cv.CV_THRESH_BINARY | cv.CV_THRESH_OTSU )
    #image[10,10] = (0, 255, 0)
    
    # create storage
    storage = cv.CreateMemStorage(0)
#    cv.ClearMemStorage(storage)
    # equalize histogram
    #cv.EqualizeHist(grayscale, grayscale)
#    cv.Canny(grayscale, dst, 60, 200, 3)#!!!!!
    #cv.Canny(grayscale, dst, 40, 200, 3)
    #cv.Threshold(grayscale,grayscale,100,255,cv.CV_THRESH_BINARY) 90
    low_threshold = 30
    ratio = 3
    cv.Canny(grayscale, dst,low_threshold,low_threshold*3)
    cv.Smooth(grayscale,grayscale,cv.CV_MEDIAN)
    #cv.Sobel(grayscale, dst,1,1)
    color_dst = cv.CreateImage( cv.GetSize(image), 8, 3 )
    cv.CvtColor( dst, color_dst, cv.CV_GRAY2BGR );#360,1,50,5 50.50.50  -- 100,0,0 1,100,5


    i = 0
    for i in range(0,2):
        rho = cv.GetTrackbarPos('rho', 'Hough')
        thresh = cv.GetTrackbarPos('thresh', 'Hough')
        lines = cv.HoughLines2( dst, storage, cv.CV_HOUGH_PROBABILISTIC, 1, cv.CV_PI/180, 1, 100,5)
        #lines = cv.HoughLines2( dst, storage, cv.CV_HOUGH_PROBABILISTIC, 1, cv.CV_PI/180, 60, 0,0)
    
        for (rho, theta) in lines[:100]:
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho 
                y0 = b * rho
                pt1 = (cv.Round(x0 + 1000*(-b)), cv.Round(y0 + 1000*(a)))
                pt2 = (cv.Round(x0 - 1000*(-b)), cv.Round(y0 - 1000*(a)))
                cv.Line(color_dst, pt1, pt2, cv.RGB(255, 0, 0), 3, 8)

    for line in lines:
        cv.Line(image, line[0], line[1], cv.CV_RGB(50,255,0), 4, cv.CV_AA);
        #print "linea 0",line[0]
        #print "linea 1",line[1]
        D = None
        izq = None
        a,b = line[0]
        if a > 300:
            print "Derecha"
            D = "si"
        else:
            izq = "si"
            print "Inquierda"
            
        if D != izq:
            print "derecho"
        else :
            pass
#    cv.Sub(grayscale, dst, dst)
        #line( result_color, Point(120,0), Point(120,960), Scalar(255,0,0), 1, CV_AA);
#    cv.Line(  Point(240,0), Point(240,960), Scalar(255,0,0), 1, CV_AA);
#    cv.Line(  Point(360,0), Point(360,960), Scalar(255,0,0), 1, CV_AA);
#    cv.Line(  Point(480,0), Point(480,960), Scalar(255,0,0), 1, CV_AA);
#    cv.Line(  Point(600,0), Point(600,960), Scalar(255,0,0), 1, CV_AA);
#    cv.Line(  Point(720,0), Point(720,960), Scalar(255,0,0), 1, CV_AA);
#    cv.Line(  Point(840,0), Point(840,960), Scalar(255,0,0), 1, CV_AA);
#    cv.Line(  Point(960,0), Point(960,960), Scalar(255,0,0), 1, CV_AA);
#    cv.Line(  Point(1080,0), Point(1080,960), Scalar(255,0,0), 1, CV_AA);
#    cv.Line(  Point(1200,0), Point(1200,960), Scalar(255,0,0), 1, CV_AA);
    return color_dst,image




if __name__ == "__main__":
 
    DEVICE = 0 #/dev/video0
    # create windows
    cv.NamedWindow('Camera')
 
    # create capture device
    device = 0 # assume we want first device
    #capture = cv.CreateCameraCapture(DEVICE)
    capture = cv.CaptureFromFile(VIDEO)

    k = ''
    while k !='q' :
        frame = cv.QueryFrame(capture)#cv.RetrieveFrame(capture)
       # frame1 = cv.QueryFrame(capture)#cv.RetrieveFrame(capture)
        if frame is None:
            break

        # mirror
        cv.Flip(frame, None, 1)
                
        # face detection
        frame,original = detect(frame)
        
        # display webcam image
        cv.ShowImage('Camera', frame)
        cv.ShowImage("Main Video",original)

        # handle events
        k = cv.WaitKey(10)
