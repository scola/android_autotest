"""
This program is used for testing android devices automatically.
It read device id and start thread to test multiple devices at 
the same time.Please check the details at 
http://developer.android.com/tools/help/monkeyrunner_concepts.html
http://developer.android.com/tools/help/MonkeyDevice.html

You just need to modify the code between line 27 and line 44 to 
finish your test.I only tested it on windows.You can find 
monkeyrunner.bat at /android_sdk_windows/tools
Command line usage:
$ monkeyrunner.bat android_autotest.py
"""
__author__ = "shaozheng.wu@gmail.com"
__version__ = "$Revision: 1.0.0 $"
__date__ = "$Date: 2012/08/30 19:51:13 $"

# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import os,sys
import threading, time

devices = os.popen('adb devices').read().strip().split('\n')[1:]
todeviceid = lambda f: MonkeyRunner.waitForConnection('', f.split('\t')[0]) 

deviceid = map(todeviceid, devices)
testcount = 0
cur_time = time.strftime('%Y%m%d%H%M')
filename = os.path.basename(__file__).split('.')[0]
Logdir = os.path.join(os.getcwd(),'Logs')
if not os.path.exists(Logdir):
    os.mkdir(Logdir) # make directory
    print 'Successfully created directory', Logdir

qlock = threading.Lock()
####################################################################################################
package = 'com.example.android.myapplication'

# sets a variable with the name of an Activity in the package
activity = 'com.example.android.myapplication.MainActivity'

# sets the name of the component to start
runComponent = package + '/' + activity

delaytime = 3
def phoneprocess(device):
    global testcount
    device.startActivity(component=runComponent)
    MonkeyRunner.sleep(delaytime)

    device.touch(73,600-100,  MonkeyDevice.DOWN_AND_UP)#touch setting
    MonkeyRunner.sleep(delaytime)

    # Takes a screenshot
    result = device.takeSnapshot()
    # Writes the screenshot to a file
    result.writeToFile('myproject/shot%s.png' %testcount,'png')
    MonkeyRunner.sleep(delaytime)

    device.touch(954,600-308,  MonkeyDevice.DOWN_AND_UP)#shot
    MonkeyRunner.sleep(delaytime)
    device.touch(954,600-308,  MonkeyDevice.DOWN_AND_UP)#shot
    MonkeyRunner.sleep(delaytime)

    device.press('KEYCODE_BACK', MonkeyDevice.DOWN_AND_UP)
    MonkeyRunner.sleep(delaytime)
####################################################################################################
def saveintofile(deviceNo):
    try:
        fd = open('Logs/%s%s.log' % (cur_time,filename),'a')
        fd.write("Testing\t%s.\tYou have tested %d times totally\n" %(devices[deviceNo].split('\t')[0],testcount))
    except IOError:
        pass
    finally:
        fd.close()
def threadcode(device):
    while True:
        global testcount
        time.sleep(1)
        deviceNo = deviceid.index(device)
        print "Testing\t%s.\tYou have tested %d times totally" %(devices[deviceNo].split('\t')[0],testcount)

        try:
            phoneprocess(device)
        except :
            print '**************error ocurr**************'
            sys.exit(1)

        qlock.acquire()
        testcount += 1
        try:
            saveintofile(deviceNo)
        finally:
            qlock.release()


for device in deviceid:
    t = threading.Thread(target = threadcode,args=(device,))
    t.setDaemon(1)
    t.start()

while True:
    time.sleep(100)
 