import cv2
import shutil
import os
import re
import sys
import numpy as np
import math
import random
import CalcImage as calc
from CheckNode import CheckNode
from HierarchyTree import Node, Tree
from collections import OrderedDict

# "Screen_Size" : [0,0,720,1280],
# "ROI": [0,48,720,1180],
# "Keyboard_Region":[0,732,720,452],

class ComputerVision:
    def __init__(self, xml, img, clickableButtonList):
        self.xml = xml
        self.img = img
        self.clickableButtonList = clickableButtonList

    #draw xml clickable buttons
    def drawBounds(self):
        drawBoundsImg = cv2.imread(self.img)
        for bounds in self.clickableButtonList:
            cv2.rectangle(drawBoundsImg, (int(bounds[0]), int(bounds[1])), (int(bounds[2]), int(bounds[3])), (255, 0, 0), 5)
        cv2.imwrite('123.png', drawBoundsImg)
        print drawBoundsImg.shape

    #draw xml clickable buttons and  ADs
    def drawAdBounds(self):
        drawAdBoundsImg = cv2.imread(self.img)
        print drawAdBoundsImg.shape
        rAdClickableButtonLlist = []
        for bounds in self.clickableButtonList:
            tempImg = drawAdBoundsImg[int(bounds[1]) : int(bounds[3]),  int(bounds[0]) : int(bounds[2])] 
            #print tempImg.shape
            #random choose
            #if self.checkAd(tempImg) == True:
            if self.checkAdddd(tempImg) == True:
                cv2.rectangle(drawAdBoundsImg, (int(bounds[0]), int(bounds[1])), (int(bounds[2]), int(bounds[3])), (0, 255, 0), 5)
            else:
                cv2.rectangle(drawAdBoundsImg, (int(bounds[0]), int(bounds[1])), (int(bounds[2]), int(bounds[3])), (255, 0, 0), 5)
                rAdClickableButtonLlist.append(bounds)
        cv2.imwrite('1234.png', drawAdBoundsImg)
        return rAdClickableButtonLlist

    def ccccheckAd(self):
        colorList = []
        img = cv2.imread('6.png')
        #imgInfo[0] = 1280, imgInfo[1] = 720
        imgInfo = img.shape

        for i in xrange(imgInfo[0]):
            for j in xrange(imgInfo[1]):
                color = img[i, j].tolist()
                if color not in colorList:
                    colorList.append(color)
        print len(colorList)

    def checkAd(self, img):
        colorList = []
        #img = cv2.imread('test.png')
        imgInfo = img.shape
        print 'imgInfo', imgInfo
        for i in xrange((imgInfo[0] * imgInfo[1]/100)):
            x = random.randint(0, imgInfo[0] - 1)
            y = random.randint(0, imgInfo[1] - 1)
            color = img[x, y].tolist()
            if color not in colorList:
                colorList.append(color)
        print len(colorList)
        if len(colorList) >= 200:
           boolAd = True
        else:
            boolAd = False
        return boolAd

    def checkAdddd(self, img):
        colorList = [[[ 0 for k in xrange(16)] for j in xrange(16)] for i in xrange(16)]
        #img = cv2.imread('test3.png')
        n = 0
        imgInfo = img.shape
        #print 'imgInfo', imgInfo
        for i in xrange((imgInfo[0] * imgInfo[1]) / 100):
            n +=1
            x = random.randint(0, imgInfo[0] - 1)
            y = random.randint(0, imgInfo[1] - 1)
            color = img[x, y].tolist()
            colorList[ color[0]/16][color[1]/16][ color[2]/16 ]  += 1
           # print color, int(color[0])/16, color[1]/16, color[2]/16

        N = 0
        for i in xrange(16):
            for j in xrange(16):
                for k in xrange(16):
                    if colorList[i][j][k] > 0:
                        N += 1 
        #print N
        if N >= 85:
           boolAd = True
        else:
            boolAd = False
        return boolAd

    def findContoursTest(self, clickableButtonList):
        im = cv2.imread('0.png')
        drawBoundsImg = im
        imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        imgray = cv2.bilateralFilter(imgray, 11, 17, 17)
        edged = cv2.Canny(imgray, 30, 200)
        cv2.imwrite('canny.png',edged)
        image, contours, hierarchy = cv2.findContours(edged,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        print 'origin ' + 'contours: ' + str(len(contours)) + ', ' + 'hierarchy: ' + str(len(hierarchy[0]))

        #build tree
        cn = CheckNode(123, '[0,48][720,1180]', 'removeExternalNode')
        cn.initialNode()
        tree = Tree()
        tree.add_node('root')
        listContours = []
        listPrintContours = [] #for tesing
        for i in xrange(len(contours)):
            tempCnt = []
            cnt = contours[i]
            hier = hierarchy[0][i]
            area = cv2.contourArea(cnt)
            x, y, w, h = cv2.boundingRect(cnt)
            tempCnt.append(x)
            tempCnt.append(y)
            tempCnt.append(x + w)
            tempCnt.append(y + h)
            listContours.append(tempCnt)
            if cn.checkNodeInRegion(tempCnt[0:2],tempCnt[2:4]) == True:
                if hier[3] ==  -1 and area > 600:
                    tree.add_node(str(tempCnt), 'root')
                    listPrintContours.append(tempCnt)
                    clickableButtonList.append(tempCnt)
                elif hier[3] != -1 and area > 600:
                    nodeParent = str(listContours[hier[3]])
                    if nodeParent != str(tempCnt):
                        tree.add_node(str(tempCnt), nodeParent)
                        listPrintContours.append(tempCnt)
                        clickableButtonList.append(tempCnt)
                        
        #tree.display('root')
        print "***** DEPTH-FIRST ITERATION *****"
        for node in tree.traverse('root'):
            print node 
        
        print 'remove small nodes and out of ROI nodes: ' + str(len(listPrintContours))

        #TODO click button and merge same state button



        #draw contours
        for i, bounds in enumerate(listPrintContours):
            cv2.rectangle(drawBoundsImg, (int(bounds[0]), int(bounds[1])), (int(bounds[2]), int(bounds[3])), (0, 255, 0), 5)
            cv2.putText(drawBoundsImg,str(i),(int(bounds[0]),int(bounds[1])), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),3)
        cv2.imwrite('12345.png', drawBoundsImg)

        #draw xml
        for i, bounds in enumerate(clickableButtonList):
            cv2.rectangle(drawBoundsImg, (int(bounds[0]), int(bounds[1])), (int(bounds[2]), int(bounds[3])), (255, 0, 0), 5)
            cv2.putText(drawBoundsImg,str(i),(int(bounds[0]),int(bounds[1])), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),3)
        cv2.imwrite('12345.png', drawBoundsImg)

        #print xml + CV
        file = open('xmlcv.txt', 'w')
        for bounds in clickableButtonList:
            file.write(str(bounds) + '\n')
        file.close

    def findContours(self):
        im = cv2.imread('0.png')
        drawBoundsImg = im
        imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        imgray = cv2.bilateralFilter(imgray, 11, 17, 17)
        edged = cv2.Canny(imgray, 30, 200)
        cv2.imwrite('canny.png',edged)
        image, contours, hierarchy = cv2.findContours(edged,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        print 'origin ' + 'contours: ' + str(len(contours)) + ', ' + 'hierarchy: ' + str(len(hierarchy[0]))

        #build tree
        cn = CheckNode(123, '[0,48][720,1180]', 'removeExternalNode')
        cn.initialNode()
        tree = Tree()
        tree.add_node('root')
        listContours = []
        listPrintContours = [] #for tesing
        for i in xrange(len(contours)):
            tempCnt = []
            cnt = contours[i]
            hier = hierarchy[0][i]
            area = cv2.contourArea(cnt)
            x, y, w, h = cv2.boundingRect(cnt)
            tempCnt.append(x)
            tempCnt.append(y)
            tempCnt.append(x + w)
            tempCnt.append(y + h)
            listContours.append(tempCnt)
            if cn.checkNodeInRegion(tempCnt[0:2],tempCnt[2:4]) == True:
                if hier[3] ==  -1 and area > 300:
                    tree.add_node(str(tempCnt), 'root')
                    listPrintContours.append(tempCnt)
                elif hier[3] != -1 and area > 300:
                    nodeParent = str(listContours[hier[3]])
                    if nodeParent != str(tempCnt):
                        tree.add_node(str(tempCnt), nodeParent)
                        listPrintContours.append(tempCnt)
        tree.display('root')
        print "***** DEPTH-FIRST ITERATION *****"
        for node in tree.traverse('root'):
            print node 
        print 'remove small nodes and out of ROI nodes: ' + str(len(listPrintContours))
        for i, bounds in enumerate(listPrintContours):
            cv2.rectangle(drawBoundsImg, (bounds[0], bounds[1]), (bounds[2], bounds[3]), (255, 0, 0), 5)
            cv2.putText(drawBoundsImg,str(i),(bounds[0],bounds[1]), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),3)
        cv2.imwrite('12345.png', drawBoundsImg)

        #click button and merge
        

    def compareState(self):
        pathToStateData = './state/'
        
        #initial first png and xml
        #shutil.copy('0.png', pathToStateData + str(0) + '.png')
        #shutil.copy('0.xml', pathToStateData + str(0) + '.xml')
        imgFiles = [name for name in os.listdir(pathToStateData) if name.endswith('.png')]
        xmlFiles = [name for name in os.listdir(pathToStateData) if name.endswith('.xml')]
        txtFiles = [name for name in os.listdir('./state/') if name.endswith('.txt')]
        print imgFiles
        print xmlFiles
        print txtFiles
        listCheckState = []
        for i in xrange(len(imgFiles)):
            listCheckState.append(calc.pixelCompare('0.png', pathToStateData + imgFiles[i], 0.1))
        print listCheckState
        #all -> and list, any or list
        if all(listCheckState) == True:
            for i in xrange(len(imgFiles) +1 ):
                if str(i) + '.png' not in imgFiles:
                    shutil.copy('0.png', pathToStateData + str(i) + '.png')
                    shutil.copy('0.xml', pathToStateData + str(i) + '.xml')
                    shutil.copy('xmlcv.txt', './state/' + str(i) + '.txt')

        '''
        #print rContours
        file = open('rcontours.txt', 'w')
        for cnt in rContours:
            x, y, w, h = cv2.boundingRect(cnt)
            bounds = '[' + str(x) + ','+ str(y) + ']' + '['  + str(x + w) + ',' + str(y + h) + ']' + '\n'
            file.write(bounds)
        file.close

        #print hierarchy
        file = open('hierarchy.txt', 'w')
        temphierarchy = hierarchy.tolist()
        for i in xrange(len(temphierarchy[0])):
            temp = str(temphierarchy[0][i]) + '\n'
            file.write(temp)
        file.close

        #print rhierarchy
        file = open('rhierarchy.txt', 'w')
        for hier in rHierarchy:
            file.write(str(hier) + '\n')
        file.close

        #print rContours
        file = open('rcontours.txt', 'w')
        for cnt in rContours:
            x, y, w, h = cv2.boundingRect(cnt)
            bounds = '[' + str(x) + ','+ str(y) + ']' + '['  + str(x + w) + ',' + str(y + h) + ']' + '\n'
            file.write(bounds)
        file.close

        #print hierarchy
        file = open('hierarchy.txt', 'w')
        temphierarchy = hierarchy.tolist()
        for i in xrange(len(temphierarchy[0])):
            temp = str(temphierarchy[0][i]) + '\n'
            file.write(temp)
        file.close

        #print rhierarchy
        file = open('rhierarchy.txt', 'w')
        for hier in rHierarchy:
            file.write(str(hier) + '\n')
        file.close
        '''

    def testDict1(self):
        d = OrderedDict()
        d['foo'] = 1
        d['bar'] = 2
        d['spam'] = 3

        for key in d:
            print key, d[key]

    def testDict2(self):
        dictLabelResult = {}
        dictLabelResult ['hi'] = [123]
        print dictLabelResult.get('hi')

    #str()  <- let list hashable
    def dedupe(self, items):
        seen = set()
        for item in items:
            if str(item) not in seen:
                yield item
                seen.add(str(item))
    #a = [1, 5, 2, 1, 9, 1, 5, 10]
    #print list(x.dedupe(a))


if __name__ == '__main__':
    x = ComputerVision(1, 2, 3)
    #print x.checkAdddd(123)
    x.findContours()