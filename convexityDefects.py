from SimpleCV import Image, Blob, Color, Display

img = Image('hand_pic.JPG')
dp = Display((img.width, img.height))
img = img.hueDistance(Color.RED).binarize(50)

while dp.isNotDone():
    blobs = img.findBlobs()
    blob = blobs[-1]
    lines, farpoints = blob.getConvexityDefects()
    #for line in lines:
        #line.draw(color=Color.RED, width=2)
    #for p in farpoints:
        #p.draw(color=Color.RED, width=3)
    img.dl().polygon(blob.mConvexHull, color=Color.RED, width=3)
    img.show()
