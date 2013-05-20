from SimpleCV import Image, JpegStreamCamera 
import time

cam = JpegStreamCamera('http://192.168.1.100:8080/videofeed')
img = cam.getImage()
ts = []
time.sleep(0.4)

while True:
    img1 = cam.getImage()
    bb = (50,50,20,20) # get Bounding Box from some method
    ts = img1.track(method="camshift", ts=ts, img=img, bb=bb)
    ts.drawBB()
    img1.show()
