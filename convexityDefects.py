from SimpleCV import *
import time
import cv
from math import atan2, degrees

cam = JpegStreamCamera('http://192.168.0.165:8080/videofeed')
#cam = JpegStreamCamera('http://192.168.1.100:8080/videofeed')
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
'''
img = Image('lenna')
blobs = img.findBlobs()
blob = blobs[-1]
lines, farpoints = blob.getConvexityDefects()
lines.draw()
farpoints.draw(color=Color.RED, width=-1)
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

while True:
    #img = Image('/home/jinyuan/Downloads/handmagician/my_hand_mod.jpg')
    org = cam.getImage()
    #img = Image('lenna')
    #img = org.threshold(100).invert() # at home/office
    img = org.hueDistance(Color.RED).threshold(30).invert() # at will's coffee
    blobs = img.findBlobs()
    if blobs:
        blob = blobs[-1]
        blob_area = blob.area()
        if blob_area > 10000 and blob_area < 50000:
            try:
                chull = cv.ConvexHull2(blob.mContour, cv.CreateMemStorage(), orientation=cv.CV_COUNTER_CLOCKWISE, return_points=False)
                defects = cv.ConvexityDefects(blob.mContour, chull, cv.CreateMemStorage())
                points = [(defect[0], defect[1], defect[2], defect[3]) for defect in defects]
                del chull
                del defects

                #points = blob.mContour
                #for i in range(len(points)-1):
                for i in range(len(points)):
                    start, end, far, depth = points[i]
                    if depth < 40:
                        continue
                    '''prev = len(points) - 1 if i == 0 else i - 1
                    succ = 0 if i == len(points) - 1 else i + 1
                    prev_start, prev_end, prev_far, prev_depth = points[prev]
                    succ_start, succ_end, succ_far, succ_depth = points[succ]
                    angle = angle_between(start, prev_far, succ_far)
                    if angle > 60:
                        continue'''
                    angle = angle_to_centroid(start, blob.centroid(), 0)
                    if angle > 120 and angle < 200:
                        img.drawText('Index Finger', start, color=Color.GREEN, fontsize=16)
                    img.drawCircle(start, 7, color=Color.YELLOW, thickness=-1)
                #    img.drawCircle(far, 3, color=Color.YELLOW, thickness=-1)
                #    img.drawLine(f1, blob.centroid(), color=Color.YELLOW, thickness=4)
                #    s2, e2, f2 = points[i+1]
                #    org.drawLine(f1, f2, color=Color.YELLOW, thickness=4)
                    img.drawLine(start, blob.centroid(), color=Color.GREEN, thickness=2)
                img.drawCircle(blob.centroid(), 6, color=Color.BLUE, thickness=-1)
            except Exception as e:
                print e
        elif blob_area > 5000 and blob_area < 10000:
            img.dl().polygon(blob.mConvexHull, color=Color.RED, width=3)
    img.show() 
    time.sleep(0.4)
