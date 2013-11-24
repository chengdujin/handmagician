from SimpleCV import JpegStreamCamera
from SimpleCV import Color, Display, RunningSegmentation, Circle
import os, time

cam = JpegStreamCamera("https://192.168.1.102:8080/videofeed")
frame = cam.getImage()
display = Display((frame.width, frame.height))

diff_seg = RunningSegmentation()
default_area = 1000

while display.isNotDone(): 
    original = cam.getImage().flipHorizontal()
    diff_seg.addImage(original)
    diff_image = diff_seg.getSegmentedImage(False).invert()
    active = original - diff_image
    
    if active:
        hue = active.hueDistance(Color.RED).binarize(50)
        blobs = hue.findBlobs()
        if blobs:
            original.dl().polygon(blobs[-1].mConvexHull, color=Color.RED, width=3)
    original.save(display)
    time.sleep(0.1)
    
    
