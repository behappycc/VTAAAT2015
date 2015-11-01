import numpy as np

class CheckNode:
    xregion = []
    yregion = []

    def __init__(self, inputNodeList, initialnode, removeType):
        self.inputNodeList = inputNodeList
        self.initialnode = initialnode
        self.removeType = removeType

    #define the boundary region, input list[x,y]
    def initialNode(self):
        listTempBounds = []
        bounds = self.initialnode
        replacebounds = bounds.replace('][', ',').replace('[','').replace(']','')
        tempbounds = replacebounds.split(',')
        for temp in tempbounds:
            listTempBounds = np.append(listTempBounds, int(temp))
        self.xregion.append(listTempBounds[0])
        self.xregion.append(listTempBounds[2])
        self.yregion.append(listTempBounds[1])
        self.yregion.append(listTempBounds[3])

    #input list[x,y]
    def checkNodeInRegion(self, firstBoundaryNode, secondBoundaryNode):
        if (firstBoundaryNode[0] >= self.xregion[0] and firstBoundaryNode[0]  <= self.xregion[1]) and \
            (firstBoundaryNode[1] >= self.yregion[0] and firstBoundaryNode[1] <= self.yregion[1]) and \
            (secondBoundaryNode[0] >= self.xregion[0] and secondBoundaryNode[0] <= self.xregion[1]) and \
            (secondBoundaryNode[1] >= self.yregion[0] and secondBoundaryNode[1] <= self.yregion[1]):
            #in the region
            return True
        else:
            # out of bound
            return False

    def removeNode(self):
        newNodeList = []
        for i, node in enumerate (self.inputNodeList):
            firstBoundaryNode = []
            secondBoundaryNode = []
            firstBoundaryNode.append(node[0])
            firstBoundaryNode.append(node[1])
            secondBoundaryNode.append(node[2])
            secondBoundaryNode.append(node[3])
            if self.removeType == 'removeExternalNode':
                if self.checkNodeInRegion(firstBoundaryNode, secondBoundaryNode) == True:
                    newNodeList.append(node)
            elif self.removeType == 'removeInternalNode':
                if self.checkNodeInRegion(firstBoundaryNode, secondBoundaryNode) == False:
                    newNodeList.append(node)
            else:
                print 'modify removeType'
        return newNodeList
        
if __name__ == '__main__':
    a = []
    nodelist1 = [2,2,3,3]
    nodelist2 = [6,6,9,9]
    nodelist3 = [1,2 ,3, 4]
    a.append(nodelist1)
    a.append(nodelist2)
    x = CheckNode(a, '[4, 4][5,5]', 'removeInternalNode')
    x.initialNode()
    print x.removeNode()
    x.CheckAd()