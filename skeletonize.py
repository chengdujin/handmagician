from SimpleCV import Image
img = Image('hand_pic.JPG')

while True:
    b = img.binarize().invert()
    s = b.skeletonize()
    r = b - s
    r.show()

# Image.track(), mask, findAndRecognizeFaces
#  findBlobsFromHueHistogram(self, model, threshold=1, smooth=True, minsize=10, maxsize=None)
