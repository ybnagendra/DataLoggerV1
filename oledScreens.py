from OmegaExpansion import oledExp
import time

class OLEDSCREENS:
    def WelcomeMessage(self):
        try:
            oledExp.setVerbosity(0)
            oledExp.driverInit()
            oledExp.clear()
            oledExp.setCursor(3, 0)
            oledExp.write("Welcome to Sunjray")
            oledExp.setCursor(4, 0)
            oledExp.write("Data Logger Project")
            time.sleep(3)
            oledExp.clear()
        except:
            pass

    def ModesOfDataLogger(self):
        try:
            oledExp.setCursor(2, 0)
            oledExp.write("Modes of DataLogger:")
            oledExp.setCursor(3, 0)
            oledExp.write("1. CONFIGURE MODE")
            oledExp.setCursor(4, 0)
            oledExp.write("2. RUN MODE")
            oledExp.setCursor(5, 0)
            oledExp.write("3. BACKUP MODE")
            time.sleep(3)
            oledExp.clear()
        except:
            pass

    def UsbConnectedMsg(self):
        try:
            oledExp.clear()
            oledExp.setCursor(3, 0)
            oledExp.write("USB Connected")
            time.sleep(3)
        except:
            pass

    def CopyDoneMsg(self):
        try:
            oledExp.setCursor(4, 0)
            oledExp.write("copy Done")
            time.sleep(3)
            oledExp.clear()
        except:
            pass

    def DisplayAnalyserData(self,resp1,resp2):
        # 01 Request Response Parameters
        voltage = ''
        current = ''
        power = ''
        resistance = ''

        # 02 Request Response Parameters
        realPower = ''
        reactivePower = ''
        apparentPower = ''

        x1 = resp1.index('V')
        x2 = resp1.index('A')
        x3 = resp1.index('KW')
        x4 = resp1.index('R')

        voltage = resp1[x1 + 2:x2 - 1]
        current = resp1[x2 + 2:x3 - 1]
        power = resp1[x3 + 3:x4 - 1]
        resistance = resp1[x4 + 2:]

        y1 = resp2.index('KW')
        y2 = resp2.index('VAR')
        y3 = resp2.index('KVA')

        realPower = resp2[y1 + 3:y2 - 1]
        reactivePower = resp2[y2 + 4:y3 - 1]
        apparentPower = resp2[y3 + 4:]

        try:
            oledExp.setCursor(1, 0)
            oledExp.write("VOLTAGE = " + str(voltage) + " V")
            oledExp.setCursor(2, 0)
            oledExp.write("CURRENT = " + str(current) + " A")
            oledExp.setCursor(3, 0)
            oledExp.write("POWER = " + str(power) + " KW")
            oledExp.setCursor(4, 0)
            oledExp.write("RES = " + str(resistance) + " Ohm")
            oledExp.setCursor(5, 0)
            oledExp.write("P = " + str(realPower) + " KW")
            oledExp.setCursor(6, 0)
            oledExp.write("Q = " + str(reactivePower) + " KVAR")
            oledExp.setCursor(7, 0)
            oledExp.write("S = " + str(apparentPower) + " KVA")
        except:
            pass


    def WrongSelectionOfKey(self):
        oledExp.clear()
        oledExp.setCursor(3, 0)
        oledExp.write("Invalid Selection")
        oledExp.setCursor(4, 0)
        oledExp.write("Select 1 or 2 or 3")
        time.sleep(2)
        oledExp.clear()
        self.ModesOfDataLogger()

    def MenuOfConfigureMode(self):
        oledExp.clear()
        oledExp.setCursor(7, 0)
        oledExp.write("CONFIGURATION MODE")
        oledExp.setCursor(6, 0)
        oledExp.write("*********************")
        oledExp.setCursor(1, 0)
        oledExp.write("1. SET DATE AND TIME ")
        oledExp.setCursor(2, 0)
        oledExp.write("2. To Edit Other Parameters")
        oledExp.setCursor(3, 0)
        oledExp.write("3. To Read Configuration")
        oledExp.setCursor(4, 0)
        oledExp.write("Your Selection: ")

    def ConfigureMode_Page2(self):
        oledExp.clear()
        oledExp.setCursor(3, 0)
        oledExp.write("Invalid Selection")
        oledExp.setCursor(4, 0)
        oledExp.write("Select 1 or 2 or 3")
        time.sleep(2)
        oledExp.clear()
        self.MenuOfConfigureMode()

    def ConnectToPC(self):
        oledExp.setCursor(7, 0)
        oledExp.write("CONFIGURATION MODE")
        oledExp.setCursor(6, 0)
        oledExp.write("*********************")
        oledExp.setCursor(3, 0)
        oledExp.write("Connect to PC/Laptop ")
        oledExp.setCursor(4, 0)
        oledExp.write("through USB Cable ")

    def ConfDoneMsg(self):
        oledExp.clear()
        oledExp.setCursor(7, 0)
        oledExp.write("CONFIGURATION MODE")
        oledExp.setCursor(6, 0)
        oledExp.write("*********************")
        oledExp.setCursor(3, 0)
        oledExp.write("Configuartion done")

    def clear(self):
        try:
            oledExp.clear()
        except:
            pass
