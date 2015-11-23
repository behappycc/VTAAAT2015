import os
import sys
import codecs
import time

denominator = []
numerator = []

def init():
    # find aim apk
    global apkname
    apkname = input("Please type your APK name: ")
    while (not os.path.isfile("./"+apkname+"/Denominator.txt")):
        print("Wrong APK name")
        apkname = input("Please type your APK name: ")

    print("---initalize--------------")
    # delete logcat
    os.system("adb logcat -c")

    # get denominator
    global denominator
    denominator_tmp = open("./"+apkname+"/Denominator.txt").read().splitlines()
    for child in denominator_tmp:
        denominator.append(child)
    
    #delete files and folders
    dirname=r"./"+str(apkname)+"/info"
    delete_file_folder(dirname)

    # inital calculate
    global step
    step=0
    calculate_line_coverage()

def delete_file_folder(src):
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass
    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc=os.path.join(src,item)
            delete_file_folder(itemsrc) 
        try:
            os.rmdir(src)
        except:
            pass

def calculate_line_coverage():
    global apkname
    global step
        
    print("--------------------------")
    print("step: "+str(step))
    
    # catch screenb
    os.system("adb shell screencap -p /sdcard/step"+str(step)+".png")
    os.system("adb pull /sdcard/step"+str(step)+".png"+" ./"+apkname+"/info/step"+str(step)+".png")
    os.system("adb shell rm /sdcard/step"+str(step)+".png")
    
    # dump
    os.system("adb logcat -d System.out:I *:S > "+os.path.join("./"+apkname+"/templog.txt"))

    # get step numerator
    step_numerator = []
    step_numeratorfile = open("./"+apkname+"/templog.txt",'r',encoding="utf8")
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
    line_coverage = 100*len(numerator)/len(denominator)
    increase = 100*(len(numerator)-before_numerator_number)/len(denominator)
    print("Line Coverage : "+str(line_coverage)+"%")
    print("increase : +"+str(increase)+"%")
    
    # output step report
    output = open("./"+apkname+"/info/step"+str(step)+".txt",'w')
    output.write("Line Coverage : "+str(line_coverage)+"%\n")
    output.write("increase : +"+str(increase)+"%")
    output.close

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
    output = open("./"+apkname+"/Numerator.txt",'w')
    for child in numerator:
           output.write(child+"\n")
    output.close
    print("--------------------------")
    print("---report-----------------")
    print("numerator number : "+str(len(numerator)))
    print("denominator number : "+str(len(denominator)))
    print("Line coverage : "+str(len(numerator)/len(denominator)*100)+"%")
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


