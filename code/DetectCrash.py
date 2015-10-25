from threading import Thread
from Queue import Queue
import os
import subprocess

class LogcatThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        print 'logcat'
        readLogcat()

def readLogcat():
    os.system("adb logcat")

def main():
    logcatThread = LogcatThread()
    logcatThread.start()

if __name__ == '__main__':
    #main()
    #subprocess.call(['adb', 'logcat'])
    queue = Queue()
    child = subprocess.Popen(['ls'], stdout = subprocess.PIPE)
    print child.communicate()
    queue.put(child.communicate)