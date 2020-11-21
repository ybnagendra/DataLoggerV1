import time
import oledScreens
import configure
import dlmode
import serial

oled = oledScreens.OLEDSCREENS()

ser1 = serial.Serial(port="/dev/ttyS1", baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                    timeout=100)


if __name__ == "__main__":
    oled.WelcomeMessage()
    
    loopBreak = 0
    while True:
        cmd = ''
        oled.ModesOfDataLogger()
        if ser1.is_open == False:
            ser1.open()
            print('serial Port Open')

        ser1.flush()
        ser1.flushInput()
        ser1.flushOutput()
        print('Flush serial before use')
        cmd = ser1.read()
        time.sleep(0.03)
        data_left = ser1.inWaiting()
        ser1.close()
        cmd += ser1.read(data_left)
        ser1.flush()
        ser1.flushInput()
        ser1.flushOutput()
        print('Flush serial port after use')
        ser1.close()

        if cmd == "CONF":
            print("Entering configure mode")
            #configure.DL_SETTINGS()
            #dlmode.RUN_MODE()
        else:
            ser1.open()
            ser1.write("give command 'CONF' to go to settings\r\n")
            ser1.close()

        loopBreak = loopBreak + 1
        if loopBreak == 3:
            break
    print("Entering Run mode")
    #dlmode.RUN_MODE()




