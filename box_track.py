from SimpleCV import Image, JpegStreamCamera 
import time

#cam = JpegStreamCamera('http://192.168.1.102:8080/videofeed')
cam = JpegStreamCamera('http://172.17.200.241:8080/videofeed')
img = cam.getImage().flipHorizontal().flipVertical()
#img = Image('/home/jinyuan/Downloads/handmagician/finger.jpg')
ts = []
bb = (300,400,20,20) # get Bounding Box from some method

while True:
    img1 = cam.getImage().flipHorizontal().flipVertical()
    ts = img1.track(method="camshift", ts=ts, img=img, bb=bb)
    #ts = img1.track(method="camshift", ts=ts, img=img, bb=bb)
    ts = img1.track(method="mftrack", ts=ts, img=img, bb=bb)
    ts.drawBB()
    img1.show()
