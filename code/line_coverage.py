import os
import sys
import codecs
import time
from SetConfig import SetConfig
from AdbExecutor import AdbExecutor

denominator = []
numerator = []

def init():
    '''
    # find aim apk
    global apkname
    apkname = input("Please type your APK name: ")
    while (not os.path.isfile("./"+apkname+"/Denominator.txt")):
        print("Wrong APK name")
        apkname = input("Please type your APK name: ")
    '''
    config = SetConfig()
    taskSetting = config.readJson()
    adb =  AdbExecutor(taskSetting)
    apkname = adb.appPackageName

    print "---initalize--------------"
    # delete logcat
    os.system("adb logcat -c")

    # get denominator
    global denominator
    denominator_tmp = open("SUT/"+apkname+"/Denominator.txt").read().splitlines()
    for child in denominator_tmp:
        denominator.append(child)

    # inital calculate
    global step
    step=0
    calculate_line_coverage()

def calculate_line_coverage():
    config = SetConfig()
    taskSetting = config.readJson()
    adb =  AdbExecutor(taskSetting)
    apkname = adb.appPackageName
    global apkname
    global step
        
    print "--------------------------"
    print"step: "+str(step)
    
    # dump
    os.system("adb logcat -d System.out:I *:S > "+os.path.join("SUT/"+apkname+"/templog.txt"))

    # get step numerator
    step_numerator = []
    step_numeratorfile = open("SUT/"+apkname+"/templog.txt",'r')
    step_numerator_lines = step_numeratorfile.readlines()
    step_numeratorfile.close
    for line in step_numerator_lines:
        if line.find("Linenumber: #")>0:
            step_numerator.append(line.split("Linenumber: #")[1].split(" Statement: #")[0])
        # arrange numerator
    step_numerator=arrange_list(step_numerator)

    # get total numerator
    global numerator
    before_numerator_number = len(numerator)
    numerator.extend(step_numerator)
        # arrange numerator
    numerator=arrange_list(numerator)

    # step report
    #line_coverage = float(100*len(numerator)/len(denominator))
    line_coverage = 100*float(len(numerator))/len(denominator)
    print 'hi' + str(len(numerator))
    print 'yo' + str(len(denominator))

    increase = 100*(float(len(numerator))-before_numerator_number)/len(denominator)
    print "Line Coverage : "+str(line_coverage)+"%"
    print "increase : +"+str(increase)+"%"
    
    # delete logcat
    os.system("adb logcat -c")
    # add step number
    step+=1

def arrange_list(listtmp):
    listtmp.sort(key=int)
    listout = []
    for line in listtmp:
        if (listout==[]):
            listout.append(line)
        elif(line!=listout[-1]):
            listout.append(line)
    return listout

def report():
    global numerator
    global denominator

    # output numerator
    output = open("SUT/"+apkname+"/Numerator.txt",'w')
    for child in numerator:
           output.write(child+"\n")
    output.close
    print "--------------------------"
    print "---report-----------------"
    print "numerator number : "+str(len(numerator))
    print "denominator number : "+str(len(denominator))
    print "Line coverage : "+str(len(numerator)/len(denominator)*100)+"%"
    return


def main():

    init()

    command = input("Press <Enter> to Dump / Enter: exit to finish >>")
    while (1):
        if command=="exit":
            break
        elif command=="":
            calculate_line_coverage()
            command = input("Press <Enter> to Dump / Enter: exit to finish >>")
        else:
            command = input("Press <Enter> to Dump / Enter: exit to finish >>")

    report()
    
if __name__ == "__main__":
    main()


