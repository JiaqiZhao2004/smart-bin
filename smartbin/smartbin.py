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

    P0_OPEN_ANGLE = 55
    P1_OPEN_ANGLE = 40
    P2_OPEN_ANGLE = 45
    P3_OPEN_ANGLE = 55

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
        self.servo_p0_cali_val = float(self.config_flie.get("smartbin_servo_p0", default_value=55.))
        self.servo_p1_cali_val = float(self.config_flie.get("smartbin_servo_p1", default_value=80.))
        self.servo_p2_cali_val = float(self.config_flie.get("smartbin_servo_p2", default_value=-35.))
        self.servo_p3_cali_val = float(self.config_flie.get("smartbin_servo_p3", default_value=80.))

        # set servos to init angle
        self.servo_p0.angle(self.servo_p0_cali_val)
        self.servo_p1.angle(self.servo_p1_cali_val)
        self.servo_p2.angle(self.servo_p2_cali_val)
        self.servo_p3.angle(self.servo_p3_cali_val)

    def servo_p0_servo_calibrate(self, value):
        self.servo_p0_cali_val = value
        self.config_flie.set("smartbin_servo_p0", "%s" % value)
        self.servo_p0.angle(value)

    def servo_p1_servo_calibrate(self, value):
        self.servo_p1_cali_val = value
        self.config_flie.set("smartbin_servo_p1", "%s" % value)
        self.servo_p1.angle(value)

    def servo_p2_servo_calibrate(self, value):
        self.servo_p2_cali_val = value
        self.config_flie.set("smartbin_servo_p2", "%s" % value)
        self.servo_p2.angle(value)

    def servo_p3_servo_calibrate(self, value):
        self.servo_p3_cali_val = value
        self.config_flie.set("smartbin_servo_p3", "%s" % value)
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

    def open(self, pin_number):
        if pin_number == 0:
            self.set_servo_p0_angle(self.P0_OPEN_ANGLE)
        elif pin_number == 1:
            self.set_servo_p1_angle(self.P1_OPEN_ANGLE)
        elif pin_number == 2:
            self.set_servo_p2_angle(self.P2_OPEN_ANGLE)
        elif pin_number == 3:
            self.set_servo_p3_angle(self.P3_OPEN_ANGLE)

    def close_all(self):
        self.reset()

    def stop(self):
        pass

    def reset(self):
        self.stop()
        self.set_servo_p0_angle(self.servo_p0_cali_val)
        self.set_servo_p1_angle(self.servo_p1_cali_val)
        self.set_servo_p2_angle(self.servo_p2_cali_val)
        self.set_servo_p3_angle(self.servo_p3_cali_val)


if __name__ == "__main__":
    px = SmartBin()
    time.sleep(1)
    px.stop()
