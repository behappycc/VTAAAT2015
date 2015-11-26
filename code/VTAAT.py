import random
import time
import line_coverage as lc
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

    #initial
    lc.init(adb.appPackageName)

    #choose initial restart 
    adb.startAPP()
    time.sleep(10)

    #print adb.algorithm
    for i in xrange(500):
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
            
            #clickableCvButtonList = computerVision.findContoursForNoClickable(clickableButtonList)
            clickableCvButtonList = computerVision.findContoursForNoClickable(rAdClickableButtonLlist)
            testInput = gen.getTestInput(clickableCvButtonList)
            if testInput == 'empty':
                adb.adbExecute('keyevent', 0, 0)
            else:
                #if adFlag == True and len(adBounds) > 0:
                try: 
                    if len(adBounds) > 0:
                        inputX = (int(adBounds[0]) + int(adBounds[2])) / 2
                        inputY = (int(adBounds[1]) + int(adBounds[3])) / 2
                    else:   
                        inputX = (int(testInput[0]) + int(testInput[2])) / 2
                        inputY = (int(testInput[1]) + int(testInput[3])) / 2
                except  ValueError:
                    print 'ValueError'
                    time.sleep(2)
                try:
                    if clickableButtonList[0][4] == adb.appPackageName:
                        #computerVision.findContoursTest(clickableButtonList)
                        computerVision.compareState()
                        num = random.randint(0,99)
                        if num <= 30:
                            adb.adbExecute('keyevent', inputX, inputY)
                        else:
                            adb.adbExecute('click', inputX, inputY)
                    else:     
                        adb.restartAPP()
                except IndexError:
                    print 'IndexError'
                    time.sleep(2)

        elif taskSetting["algorithm"] == "monkeyXML":
            from TestCaseGenerator import Monkey
            gen = Monkey()
            testInput = gen.getTestInput(clickableButtonList)
            try :
                inputX = (int(testInput[0]) + int(testInput[2])) / 2
                inputY = (int(testInput[1]) + int(testInput[3])) / 2
            except  ValueError:
                print 'ValueError'
                time.sleep(2)

            try:
                if clickableButtonList[0][4] == adb.appPackageName:
                    num = random.randint(0,99)
                    if num <= 10:
                        adb.adbExecute('keyevent', inputX, inputY)
                    else:
                        adb.adbExecute('click', inputX, inputY)
                else:
                    adb.restartAPP()
            except IndexError:
                print 'IndexError'
                time.sleep(2)
        time.sleep(2)
        lc.calculate_line_coverage(adb.appPackageName)

    lc.report()
    #adb.restartAPP()

if __name__ == '__main__':
    main()