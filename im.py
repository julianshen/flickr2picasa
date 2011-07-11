import Image

def resizeImg(imageFile):
    im1 = Image.open(imageFile)
    base = 2048
    if im1.size[0]>base or im1.size[1]>base:
        wp1 = base/float(im1.size[0])
        wp2 = base/float(im1.size[1])
        wp = wp1 if wp1<wp2 else wp2 
        new_size = (int(im1.size[0]*wp), int(im1.size[1]*wp))
        im2 = im1.resize(new_size, Image.ANTIALIAS)
        im2.save(imageFile)
