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
import os
import threading, time

devices = os.popen('adb devices').read().strip().split('\n')[1:]
todeviceid = lambda f: MonkeyRunner.waitForConnection('', f.split('\t')[0]) 

deviceid = map(todeviceid, devices)
####################################################################################################
package = 'com.example.android.myapplication'

# sets a variable with the name of an Activity in the package
activity = 'com.example.android.myapplication.MainActivity'

# sets the name of the component to start
runComponent = package + '/' + activity

delaytime = 3
def phoneprocess(device):
    
    device.startActivity(component=runComponent)
    MonkeyRunner.sleep(delaytime)
    
    device.press('KEYCODE_HOME', MonkeyDevice.DOWN_AND_UP)
    MonkeyRunner.sleep(delaytime)
####################################################################################################           
def threadcode(device):
    while True:
        time.sleep(1)
        print 'Testing\t' + devices[deviceid.index(device)]
        phoneprocess(device)           
        
        
for device in deviceid:
    t = threading.Thread(target = threadcode,args=(device,))
    t.setDaemon(1)
    t.start()

while True:
    time.sleep(100)
 