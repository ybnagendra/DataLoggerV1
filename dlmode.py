import os.path
import time
import analyser, oledScreens
import serial, shutil
import RTC_Driver
import fifoo

ser = serial.Serial(port="/dev/ttyS1", baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                    timeout=100)

ffo = fifoo.FIFFO()
oled = oledScreens.OLEDSCREENS()
a = analyser.ANALYSER_SENSOR()
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

            r = RTC_DATE_TIME()
            hdir = src + '/Date_' + r.dir_format
            ishdir = os.path.isdir(hdir)
            while (ishdir == 0):
                cdirectory = 'Date_' + r.dir_format
                ffo.CreateDirecory(src,cdirectory)
                # date time synchronize
                # ds3231.write_now()  # through Wifi
                break

        
                # Creating object to extract time from DS3231 RTC
            # r = RTC_DATE_TIME()
            secs = int(r.seconds)
            mnts = int(r.minutes)
            tz = r.rtc_dateTime
            oled.DisplayRTCTime(tz)
            if secs % 10 == 0:
                res1 = a.extractData('rawData')
                res2 = a.extractData('userData')
                print(res1)
                print(res2)
                # Commands sent to analyser
                resp1 = a.analyserResponse('#01\r\n')
                print(resp1)
                resp2 = a.analyserResponse('#02\r\n')
                print(resp2)

                oled.DisplayAnalyserData(resp1, resp2)
                if secs == 0:
                    resA = resp1 + '\n' + resp2 + '\n'
                    resB = res1 + '\n' + res2 + '\n'
                    res = resA + resB + tz + '\n'
                    print(res)

                    # Add Time String as per specification

                    fln = 'File_hr' + r.hours + '_mnts' + str(mnts - 1)
                    pth = '/mnt/mmcblk0p1/DataLoggerV1'
                    ffo.WriteDataInFile(pth, fln, res)
                    print("Writes data in minute file")

                    # create ZIp file
                    ffo.CreateZipFile(fln)
                    print("Created Zip file")
                    
                    # Bkp file of hourly data
                    # Append data to hourly file       
                    pth2 = src + '/Date_' + r.dir_format
                    hbkp_fln = 'File_hr' + r.hours
                    ffo.WriteDataInFile(pth2, hbkp_fln, res)
                    print('Data added to hourly backup file')
            time.sleep(1)
            oled.clear()
