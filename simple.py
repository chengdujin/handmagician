#import cv
import handwritingIO
from SimpleCV import *
import time

cam = JpegStreamCamera('http://172.17.200.241:8080/videofeed')
coordinates = []
prev_point = None
diff = -1
prev_diff = -1

while True:
    diff = -1
    org = cam.getImage().flipVertical().flipHorizontal()
    org.drawLine((50, 70), (50, 400), color=Color.BLUE, thickness=2)
    org.drawLine((50, 70), (400, 70), color=Color.BLUE, thickness=2)
    #img.drawLine(point, blob.centroid(), color=Color.GREEN, thickness=2)
    if org:
        img = org.hueDistance(Color.RED).threshold(70).invert()
        #img = org.hueDistance(Color.RED).threshold(60).invert()
        blobs = img.findBlobs()
        if blobs:
            blob = blobs[-1]
            if blob.area() > 17000 and blob.area() < 50000:
                points = blob.contour()
                point = max(points, key=lambda x:-x[1])
                img.drawCircle(point, 7, color=Color.YELLOW, thickness=-1)
                coordinates.append(blob.centroid())
                if prev_point:
                    diff = math.hypot(point[0] - prev_point[0], point[1] - prev_point[1])
                prev_point = point
        img.show() 

    #print diff, prev_diff
    if diff == prev_diff:
        if len(coordinates) > 5:
            print '... submitting coordinates to the server'
            hw_input = 'a'.join(['%sa%s' % (int(co[0]), int(co[1])) for co in coordinates])
            hw_output = handwritingIO.getHWResult(hw_input)
            r = list(hw_output['s'])
            print '\t'.join(r)
            coordinates = []
    prev_diff = diff
