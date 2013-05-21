from SimpleCV import *
import time
import cv

cam = JpegStreamCamera('http://192.168.1.100:8080/videofeed')
#cam = JpegStreamCamera('http://172.17.200.202:8080/videofeed')
'''
while True:
    img = cam.getImage().threshold(128)
    blobs = img.findBlobs()
    blob = blobs[-1]
    lines, farpoints = blob.getConvexityDefects()
    #lines.draw(color=Color.RED, width=2)
    farpoints.draw(color=Color.RED, width=3)
    #img.dl().polygon(blob.mConvexHull, color=Color.RED, width=3)
    img.show()
'''
'''
img = Image('lenna')
blobs = img.findBlobs()
blob = blobs[-1]
lines, farpoints = blob.getConvexityDefects()
lines.draw()
farpoints.draw(color=Color.RED, width=-1)
img.show()
'''


while True:
    #img = Image('/home/jinyuan/Downloads/handmagician/my_hand_mod.jpg')
    img = cam.getImage()
    #img = Image('lenna')
    img = img.threshold(100).invert()
    blobs = img.findBlobs()
    if blobs:
        blob = blobs[-1]
        if blob.area() > 10000 and blob.area() < 60000:
            try:
                chull = cv.ConvexHull2(blob.mContour, cv.CreateMemStorage(), return_points=False)
                defects = cv.ConvexityDefects(blob.mContour, chull, cv.CreateMemStorage())
                points = [(defect[0], defect[1], defect[2]) for defect in defects]
                del chull
                del defects

                #print len(points)
                for i in range(len(points)-1):
                    s1, e1, f1 = points[i]
                    s2, e2, f2 = points[i+1]
                    img.drawLine(f1, f2, color=Color.RED, thickness=3)
            except Exception as e:
                print e
        else:
            img.dl().polygon(blob.mConvexHull, color=Color.RED, width=3)
    img.show() 
    time.sleep(0.1)
