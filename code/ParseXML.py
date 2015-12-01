import xml.etree.ElementTree as ET
import numpy as np
import os
import sys

class ParseXML:
    def __init__(self, inputxml):
        self.inputxml = inputxml

    def getViews(self, root, layer):
        returnList = []
        for child in root:
          returnList.append((child,layer))
          returnList.extend(self.getViews(child,layer+1))
        return returnList

    def printTree(self, xmlList):
        for index,view in enumerate(xmlList):
            print "view" + str(index)
            for attr in view[0].attrib:
                print str(attr) +" = "+ str(view[0].attrib[attr])
            print " "

    def readTree(self):
        #parse xml
        tree = ET.parse(self.inputxml)
        root = tree.getroot()
        viewList = self.getViews(root, 1)
        #self.printTree(viewList)
        return viewList

    def checkClickableButton(self, viewList):
        #for bounds in self.clickableButtonList:
        #bounds[0], bounds[1], bounds[2], bounds[3] -> bounds
        #bounds[4] -> package
        #bounds[5] -> resource-id
        #bounds[6] -> class
        #bounds[7] -> content-desc
        clickableXmlList = []
        for i, node in enumerate(viewList):
            listTempBounds = np.array([])
            if node[0].attrib['clickable'] == 'true':
                bounds = node[0].attrib['bounds']
                replacebounds = bounds.replace('][', ',').replace('[','').replace(']','')
                tempbounds = replacebounds.split(',')
                tempbounds.append(node[0].attrib['package'])
                tempbounds.append(node[0].attrib['resource-id'])
                tempbounds.append(node[0].attrib['class'])
                tempbounds.append(node[0].attrib['content-desc'])
                clickableXmlList.append(tempbounds)
        #print clickableXmlList
        return clickableXmlList
            
    def testFunc(self):
        tree = ET.parse(self.inputxml)
        root = tree.getroot()

        for child in root:
            print child.tag, child.attrib

        for neighbor in root.iter('neighbor'):
            print neighbor.attrib

        for country in root.findall('country'):
            rank = country.find('rank').text
            name = country.get('name')
            print name, rank
            
if __name__ == '__main__':
    x = ParseXML('0.xml')
    xml = x.readTree()
    x.checkClickableButton(xml)

