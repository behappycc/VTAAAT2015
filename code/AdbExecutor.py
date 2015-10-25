import os
import time
import json
import shutil
import SetConfig

class AdbExecutor:
    def __init__(self, taskSetting):
        os.system("echo init")
        self.userName = taskSetting["userName"]
        self.appPackageName = taskSetting["appPackageName"]
        self.firstActivityName = taskSetting["firstActivityName"]
        self.serialNumber = taskSetting["serialNumber"]
        self.algorithm = taskSetting["algorithm"]

    def uiDump(self):
        os.system("adb shell uiautomator dump /data/local/tmp/0.xml")
        os.system("adb pull /data/local/tmp/0.xml")

    def screencapDump(self):
        os.system('adb shell screencap -p /sdcard/0.png')
        os.system('adb pull /sdcard/0.png')

    def adbExecute(self, actionType, inputX, inputY):
        adb = 'adb -s ' + self.serialNumber + ' shell input '
        if actionType == 'click':
            adb = adb + 'tap ' + str(inputX) + ' ' + str(inputY)

        elif actionType == 'keyevent': 
            #adb shell input keyevent 4
            adb = adb + 'keyevent 4'

        #using adb
        os.system(adb)

    def restartAPP(self):
        #os.system("adb root")
        os.system("adb -s "+self.serialNumber+" shell am force-stop "+self.appPackageName)
        os.system("adb -s "+self.serialNumber+" shell am start "+self.appPackageName+"/"+self.firstActivityName)
        time.sleep(4)

