import random
from SetConfig import SetConfig
from AdbExecutor import AdbExecutor
from ParseXML import ParseXML
from ComputerVision import ComputerVision

#initial config in main and pass them to adbExecutor
def main():
    config = SetConfig()
    taskSetting = config.readJson()
    #print taskSetting["sleepTime"]
    adb =  AdbExecutor(taskSetting)

    #choose initial restart 
    adb.restartAPP()

    #print adb.algorithm
    for i in xrange(5):
        adb.uiDump()
        adb.screencapDump()
        parseXML = ParseXML('0.xml')
        xml = parseXML.readTree()
        clickableButtonList = parseXML.checkClickableButton(xml)
        computerVision = ComputerVision('0.xml', '0.png', clickableButtonList, adb.appPackageName)
        computerVision.drawBounds()    
        rAdClickableButtonLlist = computerVision.drawAdBounds()

        if taskSetting["algorithm"] == "monkey":
            from TestCaseGenerator import Monkey
            gen = Monkey()
            adFlag, adBounds = computerVision.checkInterstitial()
            #testInput = gen.getTestInput(rAdClickableButtonLlist)
            
            clickableCvButtonList = computerVision.findContoursForNoClickable(clickableButtonList)
            testInput = gen.getTestInput(clickableCvButtonList)
            if adFlag == True and len(adBounds) > 0:
                inputX = (int(adBounds[0]) + int(adBounds[2])) / 2
                inputY = (int(adBounds[1]) + int(adBounds[3])) / 2
            else:   
                inputX = (int(testInput[0]) + int(testInput[2])) / 2
                inputY = (int(testInput[1]) + int(testInput[3])) / 2
            
            if testInput[4] == adb.appPackageName:
                #computerVision.findContoursTest(clickableButtonList)
                computerVision.compareState()
                num = random.randint(0,99)
                if num <= 10:
                    adb.adbExecute('keyevent', inputX, inputY)
                else:
                    adb.adbExecute('click', inputX, inputY)
            else:     
                adb.restartAPP()
    #adb.restartAPP()

if __name__ == '__main__':
    main()