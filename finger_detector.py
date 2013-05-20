from SimpleCV import *
import os, time

cam = JpegStreamCamera("http://192.168.1.100:8080/videofeed")
frame = cam.getImage()
running = RunningSegmentation(thresh=50)
found = False
bb = None
ts = []
found_image = None

while True: 
    original = cam.getImage().flipHorizontal()
    hue = original.hueDistance(Color.RED, minsaturation=150).invert()
    hue_blobs = hue.findBlobs(minsize=1000)
    '''if hue_blobs:
        hue.dl().polygon(hue_blobs[-1].mConvexHull, color=Color.YELLOW, width=3)
        if hue_blobs[-1].area() > 2000:
            try:
                lines, points = hue_blobs[-1].getConvexityDefects()
                points.draw(color=Color.RED, width=2)
            except Exception as e:
                print e

    '''
    if not found:
        running.addImage(hue)
        motion = running.getSegmentedImage(False)
        if motion:
            motion_blobs = motion.findBlobs(minsize=1000)
            if motion_blobs:
                #for mb in motion_blobs:
                #hue.dl().polygon(motion_blobs[-1].mConvexHull, color=Color.GREEN, width=3)
                if hue_blobs:
                    matched_hb = None
                    max_score = 10
                    for hb in hue_blobs:
                        cur_score = motion_blobs[-1].match(hb)
                        if cur_score < max_score:
                            max_score = cur_score
                            matched_hb = hb
                    if matched_hb:
                        #matched_hb.drawMinRect(color=Color.RED, width=3)
                        found = True
                        bb = [matched_hb.mMinRectangle[0][0], matched_hb.mMinRectangle[0][1], matched_hb.minRectWidth(), matched_hb.minRectHeight()]
                        print bb
                        found_image = hue
    else:
        ts = hue.track('camshift', ts, found_image, bb)
        ts.drawBB()
    hue.show()
