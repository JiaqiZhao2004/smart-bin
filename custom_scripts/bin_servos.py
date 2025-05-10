import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cv2
import numpy as np
from smartbin import SmartBin
from time import sleep
import readchar

manual = '''

Press any key to run the car. Press cmd+C to terminate.
'''


def show_info():
    print("\033[H\033[J", end='')  # clear terminal windows
    print(manual)


def main():
    px = SmartBin()
    show_info()
    try:
        while True:
            px.set_servo_p0_angle(0)
            px.set_servo_p1_angle(0)
            px.set_servo_p2_angle(0)
            px.set_servo_p3_angle(0)
            sleep(1)
            px.set_servo_p0_angle(10)
            px.set_servo_p1_angle(10)
            px.set_servo_p2_angle(10)
            px.set_servo_p3_angle(10)
            sleep(1)
    finally:
        px.stop()
        sleep(.2)


if __name__ == "__main__":
    main()
