import random
import time
import line_coverage as lc
from SetConfig import SetConfig
from AdbExecutor import AdbExecutor
from ParseXML import ParseXML
from ComputerVision import ComputerVision

class TraceCollector:
    def __init__(self, taskSetting, adb):
        self.taskSetting = taskSetting
        self.adb = adb

    def generateTrace(self):
        numTestCase = int(self.taskSetting['monkeyLength']) / int(self.taskSetting['traceLength'])
        traceLength = int(self.taskSetting["traceLength"])
        sleepTime = int(self.taskSetting["sleepTime"])

        #record start
        file = open('./state/trace.txt', 'w')
        file.write('********** start **********' + '\n')  
        file.close

        for i in xrange(numTestCase):
            adbList = []
            isPass = True
            if i != 0:
                self.adb.restartAPP()
                time.sleep(sleepTime)
            for j in xrange(traceLength):
                print 'testcase: ' + str(i)
                print 'tracelength: ' + str(j)               
                self.adb.uiDump()
                self.adb.screencapDump()               
                parseXML = ParseXML('0.xml')
                xml = parseXML.readTree()
                clickableButtonList = parseXML.checkClickableButton(xml)
                computerVision = ComputerVision('0.xml', '0.png', clickableButtonList, self.adb.appPackageName)
                computerVision.drawBounds()    
                rAdClickableButtonLlist = computerVision.drawAdBounds()

                if self.taskSetting["algorithm"] == "monkeyCV":
                    from TestCaseGenerator import Monkey
                    gen = Monkey()
                    adFlag, adBounds = computerVision.checkInterstitial()
                    
                    #clickableCvButtonList = computerVision.findContoursForNoClickable(clickableButtonList)
                    clickableCvButtonList = computerVision.findContoursForNoClickable(rAdClickableButtonLlist, self.taskSetting["ROI"])
                    testInput = gen.getTestInput(clickableCvButtonList)
                    if testInput == 'empty':
                        adbList.append('adb -s ' + str(self.adb.serialNumber) +  ' shell input ' + 'keyevent 4') 
                        self.adb.adbExecute('keyevent', 0, 0)
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
                            time.sleep(sleepTime)
                        try:
                            if clickableButtonList[0][4] == self.adb.appPackageName:
                                #computerVision.findContoursTest(clickableButtonList)
                                computerVision.compareState()
                                num = random.randint(0,99)
                                if num <= 10:                          
                                    adbList.append('adb -s ' + str(self.adb.serialNumber) +  ' shell input ' + 'keyevent 4') 
                                    self.adb.adbExecute('keyevent', inputX, inputY)
                                else:
                                    adbList.append('adb -s ' + str(self.adb.serialNumber) +  ' shell input ' + 'tap ' + str(inputX) + ' ' + str(inputY))
                                    self.adb.adbExecute('click', inputX, inputY)
                            else:
                                adbList.append('adb -s ' + str(self.adb.serialNumber) + " shell am force-stop " + str(self.adb.appPackageName))
                                adbList.append('adb -s ' + str(self.adb.serialNumber) + " shell am start " + str(self.adb.appPackageName) + '/' + str(self.adb.firstActivityName))
                                self.adb.restartAPP()
                        except IndexError:
                            print 'IndexError'
                            time.sleep(sleepTime)

                elif self.taskSetting["algorithm"] == "monkeyXML":
                    from TestCaseGenerator import Monkey
                    gen = Monkey()
                    testInput = gen.getTestInput(clickableButtonList)
                    try :
                        inputX = (int(testInput[0]) + int(testInput[2])) / 2
                        inputY = (int(testInput[1]) + int(testInput[3])) / 2
                    except  ValueError:
                        print 'ValueError'
                        time.sleep(sleepTime)

                    try:
                        if clickableButtonList[0][4] == self.adb.appPackageName:
                            num = random.randint(0,99)
                            if num <= 10:
                                adbList.append('adb -s ' + str(self.adb.serialNumber) +  ' shell input ' + 'keyevent 4')
                                self.adb.adbExecute('keyevent', inputX, inputY)
                            else:
                                adbList.append('adb -s ' + str(self.adb.serialNumber) +  ' shell input ' + 'tap ' + str(inputX) + ' ' + str(inputY))
                                self.adb.adbExecute('click', inputX, inputY)
                        else:
                            adbList.append('adb -s ' + str(self.adb.serialNumber) + " shell am force-stop " + str(self.adb.appPackageName))
                            adbList.append('adb -s ' + str(self.adb.serialNumber) + " shell am start " + str(self.adb.appPackageName) + '/' + str(self.adb.firstActivityName))
                            self.adb.restartAPP()
                    except IndexError:
                        print 'IndexError'
                        time.sleep(sleepTime)
                time.sleep(sleepTime)

                #check code stack and log files
                self.adb.generateLog()
                csResult = self.checkCodeStack('./state/log.txt')
                if csResult != "pass":
                    isPass = False
                    adbList.append(str(csResult))
                    print '-------------------------------------------------------'
                    break

                if self.taskSetting["instrument"] == "True":
                    lc.calculate_line_coverage(self.adb.appPackageName)
                else:
                    print '-------------------------------------------------------'

                print adbList
            #End of a trace, and start writing trace.txt
            if isPass == True:
                print 'testcase: pass'
                file = open('./state/trace.txt', 'a')
                file.write('---------- testcase ' + str(i) + ' pass----------' + '\n')  
                for adb in adbList:                  
                    file.write(str(adb) + '\n')
                file.close
            else:
                print 'testcase: fail'
                file.write('---------- testcase ' + str(i) + ' fail----------' + '\n')
                file = open('./state/trace.txt', 'a')
                for adb in adbList:
                    file.write(str(adb) + '\n')
                file.close
                    
    def checkCodeStack(self,log):
        logFile = open(log,"r")
        form = logFile.readlines()
        logFile.close()

        for line in form[:]:
            if line.startswith("--------- beginning"):
                form.remove(line)
            if line == "\n":
                form.remove(line)

        if len(form) != 0:
            print("[Error] code stack = ")
            print form
            return form
        else:
            return "pass"