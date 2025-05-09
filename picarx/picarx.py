from robot_hat import Pin, ADC, PWM, Servo, fileDB
from robot_hat import Grayscale_Module, Ultrasonic, utils
import time
import os


def constrain(x, min_val, max_val):
    '''
    Constrains value to be within a range.
    '''
    return max(min_val, min(max_val, x))


class SmartBin(object):
    CONFIG = '/opt/picar-x/picar-x.conf'

    SERVO_P0_MIN = -180
    SERVO_P0_MAX = 180
    SERVO_P1_MIN = -180
    SERVO_P1_MAX = 180
    SERVO_P2_MIN = -180
    SERVO_P2_MAX = 180
    SERVO_P3_MIN = -180
    SERVO_P3_MAX = 180

    PERIOD = 4095
    PRESCALER = 10
    TIMEOUT = 0.02

    # servo_pins: camera_pan_servo, camera_tilt_servo, direction_servo
    # motor_pins: left_swicth, right_swicth, left_pwm, right_pwm
    # grayscale_pins: 3 adc channels
    # ultrasonic_pins: trig, echo2
    # config: path of config file
    def __init__(self,
                 servo_pins: list = ['P0', 'P1', 'P2', 'P3'],
                 motor_pins: list = ['D4', 'D5', 'P13', 'P12'],
                 grayscale_pins: list = ['A0', 'A1', 'A2'],
                 ultrasonic_pins: list = ['D2', 'D3'],
                 config: str = CONFIG,
                 ):
        # reset robot_hat
        utils.reset_mcu()
        time.sleep(0.2)

        # --------- config_flie ---------
        self.config_flie = fileDB(config, 777, os.getlogin())

        # --------- servos init ---------
        self.servo_p0 = Servo(servo_pins[0])
        self.servo_p1 = Servo(servo_pins[1])
        self.servo_p2 = Servo(servo_pins[2])
        self.servo_p3 = Servo(servo_pins[3])
        # get calibration values
        self.servo_p0_cali_val = float(self.config_flie.get("picarx_servo_p0", default_value=0))
        self.servo_p1_cali_val = float(self.config_flie.get("picarx_servo_p1", default_value=0))
        self.servo_p2_cali_val = float(self.config_flie.get("picarx_servo_p2", default_value=0))
        self.servo_p3_cali_val = float(self.config_flie.get("picarx_servo_p3", default_value=0))

        # set servos to init angle
        self.servo_p0.angle(self.servo_p0_cali_val)
        self.servo_p1.angle(self.servo_p1_cali_val)
        self.servo_p2.angle(self.servo_p2_cali_val)
        self.servo_p3.angle(self.servo_p3_cali_val)

    def servo_p0_servo_calibrate(self, value):
        self.servo_p0_cali_val = value
        self.config_flie.set("picarx_servo_p0", "%s" % value)
        self.servo_p0.angle(value)

    def servo_p1_servo_calibrate(self, value):
        self.servo_p1_cali_val = value
        self.config_flie.set("picarx_servo_p1", "%s" % value)
        self.servo_p1.angle(value)

    def servo_p2_servo_calibrate(self, value):
        self.servo_p2_cali_val = value
        self.config_flie.set("picarx_servo_p2", "%s" % value)
        self.servo_p2.angle(value)

    def servo_p3_servo_calibrate(self, value):
        self.servo_p3_cali_val = value
        self.config_flie.set("picarx_servo_p3", "%s" % value)
        self.servo_p3.angle(value)

    def set_servo_p0_angle(self, value):
        value = constrain(value, self.SERVO_P0_MIN, self.SERVO_P0_MAX)
        self.servo_p0.angle(-1 * (value + -1 * self.servo_p0_cali_val))

    def set_servo_p1_angle(self, value):
        value = constrain(value, self.SERVO_P1_MIN, self.SERVO_P1_MAX)
        self.servo_p1.angle(-1 * (value + -1 * self.servo_p1_cali_val))

    def set_servo_p2_angle(self, value):
        value = constrain(value, self.SERVO_P2_MIN, self.SERVO_P2_MAX)
        self.servo_p2.angle(-1 * (value + -1 * self.servo_p2_cali_val))

    def set_servo_p3_angle(self, value):
        value = constrain(value, self.SERVO_P3_MIN, self.SERVO_P3_MAX)
        self.servo_p3.angle(-1 * (value + -1 * self.servo_p3_cali_val))

    def stop(self):
        pass

    def reset(self):
        self.stop()
        self.set_servo_p2_angle(0)
        self.set_servo_p1_angle(0)
        self.set_servo_p0_angle(0)


if __name__ == "__main__":
    px = SmartBin()
    time.sleep(1)
    px.stop()
