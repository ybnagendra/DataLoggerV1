import time
import dlmode, oledScreens, configure

oled =oledScreens.OLEDSCREENS()

if __name__ == "__main__":
    oled.WelcomeMessage()
    while True:
        oled.ModesOfDataLogger()
        key='2'
        if (key == '1'):
            print("----------------------CONF MODE----------------------")
            configure.DL_SETTINGS()
            dlmode.RUN_MODE()
        elif (key == '2'):
            print("----------------------RUN MODE----------------------")
            dlmode.RUN_MODE()
