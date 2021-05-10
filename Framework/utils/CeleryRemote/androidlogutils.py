####################################
# File name: androidlogutils.py    #
# Author: Varun Tyagi              #
# Submission:Feb 17, 2016          #
# Python: 2.7                      #
####################################

import os
import adb
import sys
import natsort

adbObj=''

class adbHelper(object):
    '''Class to work with Android Devices. Major functions are - checking the list of
    devices connected to the machine, truncating a file, copying a file from android device to
    local machine. Prerequisites for these modules to work is ADB, drivers for connected devices and Java.'''

    #sys.path.append('C:\\Users\\VTyagi\\PycharmProjects\\RoD\\AndroidLogUtils')
    def __init__(self):
        print("Checking Default Directory for adb on windows platform")
        self.adbDefaultLocation = "C:\Users\ShoreTel\Desktop\sdk\platform-tools"
        if os.path.exists(self.adbDefaultLocation):
            print('Android Debug Bridge found on default location, Changing Current Working Dir to:' + self.adbDefaultLocation)
            # os.chdir(self.adbDefaultLocation)
        else:
            print('Android Debug Bridge is not found on default path')
        self.adbObj = adb.ADB(self.adbDefaultLocation)
        if self.adbObj.devices() != []:
            print(self.adbObj.devices())
        else:
            print('No device is connected')
            # sys.exit()
        print('Android Object is ready to be used')


    def listDevices(self):
        for device in self.adbObj.devices():
            print('Found Device: ' + device)


    def isDevicesConnected(self, deviceSerialNumber):
        '''Function to check whether a device is connected to a local machine or not. Inputs are device adb serial number.'''
        if deviceSerialNumber in self.adbObj.devices():
            print('Device Connected --- %s' % deviceSerialNumber)
            return True
        else:
            print('Device is not Connected --- %s' % deviceSerialNumber)
            return False


    def truncateFile(self, device, file, filesDir):
        '''Function to truncate a given file on an android device. File name and path is required of the file to be truncated.'''
        if self.isDevicesConnected(device):
            print('Truncating File:' + file)
            if self.checkFile(device, file, filesDir):
                print("Deleting File:" + file)
                self.adbObj.shell(device, "rm -f " + filesDir+file)
                self.checkFile(device, file, filesDir)
                print("File Deletion Confirm: " + file)
            self.adbObj.shell(device, "touch " + filesDir+file)
            self.checkFile(device, file, filesDir)
            print("File Created With Same Name; Truncate Operation Completed")


    def checkFile(self, device, file, filesDir):
        '''Function to check if a file exists on an android filesystem. Device serial number, file name and file directory path is required.'''
        print('Searching for File: ' + filesDir+file)
        files = self.adbObj.shell(device,"ls "+filesDir).split()
        if file in files:
            print('File Found: ' + os.path.join(filesDir,file))
            return True
        else:
            print('File NOT Found: ' + os.path.join(filesDir,file))
            return False

    def copyFileFromDevice(self, device, file, filesDir, targetLocation):
        '''Function to copy a file from connected android device to local system. Requires Device serial number, file name, file directory, and
        target location on the local machine i.e. complete path to folder.'''
        if self.checkFile(device, file, filesDir):
            print('File Found Copying')
            print(self.adbObj.get(device, filesDir+file, targetLocation))
            print('Copied File %s to %s of device %s' % (filesDir+file,targetLocation,device))
        else:
            print('File Not Found Cannot be copied')

    def removeFiles(self, device, log_file_location):
        print("Removing Files from location: " + log_file_location)
        self.adbObj.shell(device,"rm -rf " + log_file_location + "*")

    def get_latest_file(self, device, files_location):
        print("Listing Files in Directory: " + files_location)
        res = self.adbObj.shell(device, "ls " + files_location)
        if res:
            res = natsort.natsorted(res.split('\n'), key=lambda y: y.lower())[-1]
        return res


if __name__== '__main__':
    '''Boiler Plate Code for Testing Purposes.'''
    devices = ["4d00b23e4f04a0ed",]
    file = "RALog20.txt"
    logFilesLocation = "/mnt/sdcard/com.shoretel.RADialer/files/"
    tarLocation = "C:\\"

    for dev in devices:
        adbHelper().listDevices()
        print("\n"*5)
        adbHelper().isDevicesConnected(dev)
        print("\n"*5)
        adbHelper().truncateFile(dev,file,logFilesLocation)
        print("\n"*5)
        adbHelper().copyFileFromDevice(dev,file,logFilesLocation, tarLocation)
