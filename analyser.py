import random
import jsonpickle,time
import serial

ser = serial.Serial(port="/dev/ttyS1", baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                    timeout=100)

class ANALYSER_SENSOR:
    def extractData(self, command):
        if command == 'rawData':
            barometricPressure = random.randint(500, 1200)
            temperature = random.randint(20, 60)
            humidity = random.randint(20, 60)
            packetNo = random.random()  # Return a float value between 0 and 1

            dataObj1 = {
                'BarometricPressure': barometricPressure,
                'Temperature': temperature,
                'Humidity': humidity,
                'PacketNo': packetNo
            }

            self.ds1 = jsonpickle.encode(dataObj1)
            return self.ds1

        elif command == 'userData':
            f = open('confdata.txt', 'r')
            lines = f.readlines()
            dataObj2 = {
                'SiteId': lines[0].rstrip('\n'),
                'MonitoringID': lines[1].rstrip('\n'),
                'AnalyzerID': lines[2].rstrip('\n'),
                'ParameterID': lines[3].rstrip('\n')
            }
            self.ds2 = jsonpickle.encode(dataObj2)
            return self.ds2

    def analyserResponse(self,cmd):
        print("Analyser Serial functions")

        if cmd == '#01\r\n':
            if ser.is_open == False:
                ser.open()
                print('Serial Port Open')

            ser.flush()
            ser.flushInput()
            ser.flushOutput()
            print('Flush serial port before use')
            ser.write('#01\r\n')
            print('#01 sent to analyser')
            hashOneResponse = ser.read()  # read serial port
            time.sleep(0.03)
            data_left = ser.inWaiting()  # check for remaining byte
            hashOneResponse += ser.read(data_left)
            print('Received #01 Response')
            ser.flush()
            ser.flushInput()
            ser.flushOutput()
            print('Flush serial port after use')
            ser.close()
            print('serial port closed')
            return hashOneResponse

        elif cmd == '#02\r\n':
            if ser.is_open == False:
                ser.open()
                print('Serial Port Open')

            ser.flush()
            ser.flushInput()
            ser.flushOutput()
            print('Flush serial port before use')
            ser.write('#02\r\n')
            print('#02 sent to analyser')
            hashTwoResponse = ser.read()  # read serial port
            time.sleep(0.03)
            data_left = ser.inWaiting()  # check for remaining byte
            hashTwoResponse += ser.read(data_left)
            print('Received #01 Response')
            ser.flush()
            ser.flushInput()
            ser.flushOutput()
            print('Flush serial port after use')
            ser.close()
            print('serial port closed')
            return  hashTwoResponse
        else:
            print("Invalid Serial request to analyser")
