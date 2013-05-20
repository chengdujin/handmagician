from SimpleCV import JpegStreamCamera
from SimpleCV import Color, Display, RunningSegmentation, Circle
import os, time

cam = JpegStreamCamera("http://172.17.200.104:8080/videofeed")
frame = cam.getImage()
display = Display((frame.width, frame.height))

running = RunningSegmentation(thresh=50)
default_area = 1000

while display.isNotDone(): 
    original = cam.getImage().flipHorizontal()
    hue = original.hueDistance(Color.RED, minsaturation=64).binarize(50).morphOpen()
    hue_blobs = hue.findBlobs(minsize=70)
    if hue_blobs:
        for hb in hue_blobs:
             original.dl().polygon(hb.mConvexHull, color=Color.YELLOW, width=3)

    running.addImage(hue)
    motion = running.getSegmentedImage(False)
    if motion:
        motion_blobs = motion.findBlobs(minsize=70)
        if motion_blobs:
            #for mb in motion_blobs:
            original.dl().polygon(motion_blobs[-1].mConvexHull, color=Color.GREEN, width=3)
            if hue_blobs:
                matched_hb = None
                max_score = 10
                for hb in hue_blobs:
                    cur_score = motion_blobs[-1].match(hb)
                    if cur_score < max_score:
                        max_score = cur_score
                        matched_hb = hb
                if matched_hb:
                    original.dl().polygon(matched_hb.mConvexHull, color=Color.RED, width=3)
    original.save(display)
    time.sleep(0.1)
