#import cv
import handwritingIO
from math import atan2, degrees
from SimpleCV import *
import time

#cam = JpegStreamCamera('http://192.168.0.165:8080/videofeed')
cam = JpegStreamCamera('http://192.168.1.102:8080/videofeed')
#cam = JpegStreamCamera('http://172.17.200.200:8080/videofeed')
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

def angle_between(curr, succ, prev):
    x = atan2(succ[0] - curr[0], succ[1] - curr[1])
    y = atan2(prev[0] - curr[0], prev[1] - curr[1])
    return abs(round(degrees(x - y)))

def angle_to_centroid(tip, centroid, angle):
    x = tip[0] - centroid[0]
    y = centroid[1] - tip[1]
    theta = atan2(y, x)
    angle_tip = round(degrees(theta))
    return angle_tip + (90 - angle)

coordinates = []

while True:
    OCCUPIED = False
    org = cam.getImage()
    if org:
        #img = org.threshold(100).invert() # at home/office
        #img = org.hueDistance(Color.RED).threshold(30).flipVertical().invert() # at will's coffee
        img = org.hueDistance(Color.RED).threshold(60).flipHorizontal().invert() # at will's coffee
        blobs = img.findBlobs()
        if blobs:
            blob = blobs[-1]
            blob_area = blob.area()
            #if blob_area > 10000 and blob_area < 50000:
            if blob_area > 17000:
                try:
                    #lines, farpoints = blob.getConvexityDefects()
                    #farpoints.draw()
                    blob.drawOutline(color=Color.RED)
                    points = blob.contour()
                    point = max(points, key=lambda x:-x[1])
                    img.drawCircle(point, 6, color=Color.YELLOW, thickness=-1)
                    #img.drawLine(point, blob.centroid(), color=Color.GREEN, thickness=2)
                    """
                    chull = cv.ConvexHull2(blob.mContour, cv.CreateMemStorage(), orientation=cv.CV_COUNTER_CLOCKWISE, return_points=False)
                    defects = cv.ConvexityDefects(blob.mContour, chull, cv.CreateMemStorage())
                    points = [(defect[0], defect[1], defect[2], defect[3]) for defect in farpoints]
                    #del chull
                    #del defects

                    #points = blob.mContour
                    #for i in range(len(points)-1):
                    for i in range(len(points)):
                        start, end, far, depth = points[i]
                        if depth < 40:
                            continue
                    
                        #prev = len(points) - 1 if i == 0 else i - 1
                        #succ = 0 if i == len(points) - 1 else i + 1
                        #prev_start, prev_end, prev_far, prev_depth = points[prev]
                        #succ_start, succ_end, succ_far, succ_depth = points[succ]
                        #angle = angle_between(start, prev_far, succ_far)
                        #if angle > 60:
                        #    continue
                    
                        angle = angle_to_centroid(start, blob.centroid(), 0)
                        if angle > 30 and angle < 100:
                            img.drawText('Index Finger', start, color=Color.GREEN, fontsize=16)
                        else:
                            img.drawText(str(angle), start, color=Color.GREEN, fontsize=16)
                        #    img.drawCircle(start, 7, color=Color.RED, thickness=-1)
                        img.drawCircle(start, 7, color=Color.YELLOW, thickness=-1)
                        img.drawCircle(far, 5, color=Color.YELLOW, thickness=-1)
                        #img.drawLine(f1, blob.centroid(), color=Color.RED, thickness=4)
                        #s2, e2, f2 = points[i+1]
                        #org.drawLine(f1, f2, color=Color.YELLOW, thickness=4)
                        #img.drawLine(start, blob.centroid(), color=Color.GREEN, thickness=2)
                    """

                    #img.drawCircle(blob.centroid(), 6, color=Color.BLUE, thickness=-1)
                    #print blob.centroid()
                    coordinates.append(blob.centroid())
                    #print 'a'.join(['%sa%s' % (int(co[0]), int(co[1])) for co in coordinates])
                except Exception as e:
                    print e
            #elif blob_area > 5000 and blob_area < 10000:
                #img.dl().polygon(blob.mConvexHull, color=Color.RED, width=3)
                #img.drawCircle(blob.centroid(), 6, color=Color.BLUE, thickness=-1)
                #print blob.centroid()
            #new_blobs = FeatureSet([blob for blob in blobs if blob.area > 5000])
            #if new_blobs.overlaps(Circle(5, 50, 550, 30)):
            #    img.dl().circle((50, 550), 30, Color.YELLOW, filled=True, alpha=100)
                OCCUPIED = True

        if not OCCUPIED:
            #img.dl().circle((50, 550), 30, Color.WHITE, filled=True, alpha=100)
            if len(coordinates) > 5:
                hw_input = 'a'.join(['%sa%s' % (int(co[0]), int(co[1])) for co in coordinates])
                hw_output = handwritingIO.getHWResult(hw_input)
                r = list(hw_output['s'])
                print '\t'.join(r)
            coordinates = []
        img.show() 
        #time.sleep(0.4)
