from SimpleCV import *

#cam = JpegStreamCamera('http://192.168.1.100:8080/videofeed')
cam = JpegStreamCamera('http://172.17.200.202:8080/videofeed')
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
    img = Image('/home/jinyuan/Downloads/handmagician/my_hand_mod.jpg')
    #img = cam.getImage()
    #img = Image('lenna')
    img = img.threshold(200)
    blobs = img.findBlobs()
    blob = blobs[-1]
    if blob.area() < 80000:
        print 'oh ...', blob.area()
        lines, farpoints = blob.getConvexityDefects()
        lines.draw()
        farpoints.draw(color=Color.RED, width=3)
    img.dl().polygon(blob.mConvexHull, color=Color.RED, width=3)
    print 'no ... ', blob.area()
    img.show() 
