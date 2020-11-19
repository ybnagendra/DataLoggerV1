import os.path
import time
import analyserSensor
import zipfile
import serial, shutil
import RTC_Driver
from OmegaExpansion import oledExp
import oledScreens

ser = serial.Serial(port="/dev/ttyS1", baudrate=115200, timeout=100)
oled =oledScreens.OLEDSCREENS()
a = analyserSensor.ANALYSER_SENSOR()
usb_pth = '/mnt/sda1'
src = '/mnt/mmcblk0p1/DataLoggerV1/BkpDir/'


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


class MAKE_DIRECTORY:
    def __init__(self, pth, directory):
        self.parent_dir = pth
        self.directory = directory
        dst_dir_path = os.path.join(self.parent_dir, self.directory)
        os.mkdir(dst_dir_path)


class WRITE_DATA_IN_FILE:
    def __init__(self, pth, fileName, response):
        completeName = os.path.join(pth, fileName + ".txt")
        self.fileName = completeName
        self.response = response
        f = open(self.fileName, "a")
        f.write(self.response + '\n')
        f.close()


class RTC_DATE_TIME:
    def __init__(self):
        ds3231 = RTC_Driver.SDL_DS3231(0, 0x68)
        DS3231 = ds3231.read_datetime()
        ds = str(DS3231)
        self.seconds = ds[17:]
        self.minutes = ds[14:16]
        self.hours = ds[11:13]
        self.dir_format = ds[8:10] + ds[5:7] + ds[2:4]
        self.rtc_date = ds[8:10] + "/" + ds[5:7] + "/" + ds[2:4]
        self.rtc_time = ds[11:13] + ":" + ds[14:16] + ":" + ds[17:]
        self.rtc_dateTime = "Dt: " + self.rtc_date + " " + self.rtc_time
        self.bkpdt = ds[8:10] + ds[5:7] + ds[2:4] + "_" + ds[11:13] + ds[14:16] + ds[17:]


class EMMC_TO_USB_COPY:
    def __init__(self):
        # Creating object to extract time from RTC to create folder with date and time
        r = RTC_DATE_TIME()
        bkp_dir = 'BKP_' + r.bkpdt

        # Adds directory BKP_ddmmyy_hrmntsec to usb path
        dest = usb_pth + "/" + bkp_dir

        # Creates directory in usb path with date and time.
        # Copies directories from EMMC to USB
        shutil.copytree(src, dest)
        print("Copied directories from EMMC to USB")

        # deleted the object
        del r

class RUN_MODE:
    def __init__(self):
        print("System is in Run Mode")
        copyDone = 0
        isUSB = 0

        while True:
            # checks usb path
            isUSB = os.path.isdir(usb_pth)

            # If USB not inserted/removed from port sets copyDone = 0
            if isUSB == 0:
                copyDone = 0

            # If copyDone is 0, checks whether the usb is in connection or not.
            if copyDone == 0:
                isUSB = os.path.isdir(usb_pth)

            # If copyDone is 0, and USB connected then it copies all directories from EMMC to USB
            # After copying all, set copyDone to 1
            if copyDone == 0 and isUSB == 1:
                print("USB Connected")
                oled.UsbConnectedMsg()
                EMMC_TO_USB_COPY()
                oled.CopyDoneMsg()
                copyDone = 1

            # Creating object to extract time from DS3231 RTC
            r = RTC_DATE_TIME()
            secs = int(r.seconds)
            mnts = int(r.minutes)

            cdir = src + '/Date_' + r.dir_format
            isDir = os.path.isdir(cdir)
            while (isDir == 0):
                cdirectory = 'Date_' + r.dir_format
                MAKE_DIRECTORY(src, cdirectory)

                # date time synchronize
                # ds3231.write_now()  # through Wifi
                break

            if secs % 10 == 0:
                res1 = a.analyserRequest('rawData')
                res2 = a.analyserRequest('userData')

                ser.write('#01\r\n')
                resp1 = ser.read()  # read serial port
                time.sleep(0.03)
                data_left = ser.inWaiting()  # check for remaining byte
                resp1 += ser.read(data_left)

                ser.write('#02\r\n')
                resp2 = ser.read()  # read serial port
                time.sleep(0.03)
                data_left = ser.inWaiting()  # check for remaining byte
                resp2 += ser.read(data_left)

                oled.DisplayAnalyserData(resp1, resp2)

                if secs == 0:
                    resA = resp1 + '\n' + resp2 + '\n'
                    resB = res1 + '\n' + res2 + '\n'
                    res = resA + resB

                    fln = 'File_hr' + r.hours + '_mnts' + str(mnts - 1)
                    pth = '/mnt/mmcblk0p1/DataLoggerV1'
                    WRITE_DATA_IN_FILE(pth, fln, res)
                    print(res)


                    # create ZIp file
                    with zipfile.ZipFile('Files.zip', 'a', compression=zipfile.ZIP_DEFLATED) as my_zip:
                        my_zip.write(fln + ".txt")
                        # Send Zip file to server
                    os.remove(fln + ".txt")
                    # time.sleep(1)

                    pth2 = src + '/Date_' + r.dir_format
                    hbkp_fln = 'File_hr' + r.hours
                    WRITE_DATA_IN_FILE(pth2, hbkp_fln, res)
             del r


