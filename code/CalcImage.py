import numpy as np
import math
import cv2
#from matplotlib import pyplot as plt

def calcPSNR(i1, i2):
    s1 = cv2.absdiff(i1, i2)
    s1 = np.float32(s1)
    s1 = cv2.multiply(s1, s1)
    s = cv2.sumElems(s1)

    sse = s[0] + s[1] + s[2]
    print s[0], s[1], s[2]
    if (sse <= 1e-10):
        return 0
    else:
        print i1.shape[0], i1.shape[1]
        #len(i1.shape) -> colorful image should divide 3 
        mse = sse / (len(i1.shape) * i1.shape[0] *  i1.shape[1])
        psnr = 10 * math.log((255 * 255) / mse, 10)
    return psnr

import cv2

def pixelCompare(i1, i2, ratio):
    img1 = cv2.imread(i1)
    img2 = cv2.imread(i2)
    imgray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    imgray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    #imgInfo[0] = 1280, imgInfo[1] = 720
    imgInfo = img1.shape
    diff = 0
    for i in xrange(imgInfo[0]):
        for j in xrange(imgInfo[1]):
            if imgray1[i, j] != imgray2[i, j]:
                diff += 1
    compare = float(diff) / float((imgInfo[0] * imgInfo[1]))
    #print str(compare * 100) + '%'
    if compare > ratio:
        #there are differnt
        return True
    else:
        return False

def nodeCenter(node):
    centerX = (float(node[0]) + float(node[2])) / 2
    centerY = (float(node[1]) + float(node[3])) / 2
    return centerX, centerY

def euclideanDistance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)


'''
def findSIFT():
    img1 = cv2.imread('box.png',0)          # queryImage
    img2 = cv2.imread('box_in_scene.png',0) # trainImage

    # Initiate SIFT detector
    sift = cv2.SIFT()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    #BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)

    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])

    # cv2.drawMatchesKnn expects list of lists as matches.
    img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,flags=2)

    plt.imshow(img3),plt.show()
'''
if __name__ == '__main__':
    '''
    img1 = cv2.imread('1.jpg',0)
    img2 = cv2.imread('1.jpg',0)
    measurePSNR(img1, img2)
    '''
    '''
    #findSIFT()
    img = cv2.imread('test3.png',0)
    sift = cv2.xfeatures2d.SIFT_create()
    sift.detect(img)
    '''
    pixelCompare('0.png', '123.png', 0.1)
    print euclideanDistance(3,5,5,0)
    a = [1,3,4,4]
    print nodeCenter(a)