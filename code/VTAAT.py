import time
import line_coverage as lc
from SetConfig import SetConfig
from AdbExecutor import AdbExecutor
from TraceCollector import TraceCollector

def main():
    config = SetConfig()
    taskSetting = config.readJson()
    adb =  AdbExecutor(taskSetting)

    if taskSetting["instrument"] == "True":
        #initial
        lc.init(adb.appPackageName)

        #choose initial restart 
        adb.restartAPP()
        time.sleep(5)

        #collect trace
        tc = TraceCollector(taskSetting, adb)
        tc.generateTrace()
        
        #report
        lc.report()
        #adb.restartAPP()
    elif taskSetting["instrument"] == "False":
        #choose initial restart 
        adb.restartAPP()
        time.sleep(5)

        #collect trace
        tc = TraceCollector(taskSetting, adb)
        tc.generateTrace()

        #report

if __name__ == '__main__':
    main()