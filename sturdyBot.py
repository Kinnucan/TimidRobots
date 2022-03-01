from ev3dev2.motor import MediumMotor, LargeMotor, MotorSet, MoveTank, MoveSteering
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.motor import SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor, GyroSensor, ColorSensor
from ev3dev2.sound import Sound
import time


class SturdyBot(object):
    """The class to create a manager for robot"""

    # ---------------------------------------------------------------------------
    # Constants for the configDict
    LEFT_MOTOR = 'left-motor'
    RIGHT_MOTOR = 'right-motor'
    MEDIUM_MOTOR = 'medium-motor'
    LEFT_TOUCH = 'left-touch'
    RIGHT_TOUCH = 'right-touch'
    ULTRA_SENSOR = 'ultra-sensor'
    COLOR_SENSOR = 'color-sensor'
    GYRO_SENSOR = 'gyro-sensor'

    # ---------------------------------------------------------------------------
    # The default config that the program will use if no config is given
    DEFAULT_CONFIG = {ULTRA_SENSOR: INPUT_1, LEFT_TOUCH: INPUT_4,
                      COLOR_SENSOR: INPUT_2, RIGHT_TOUCH: INPUT_3,
                      LEFT_MOTOR: OUTPUT_C, RIGHT_MOTOR: OUTPUT_A}

    # ---------------------------------------------------------------------------

    def __init__(self, name, configDict=None):
        """ Take the configuration of the robot and set up the robot
        If no configuration is given, then the robot will not set up motors
        or sensors, and the robot will fail
        """
        self.name = name

        self.tankMover = None
        self.steerMover = None
        self.mediumMotor = None
        self.leftTouch = None
        self.rightTouch = None
        self.ultraSensor = None
        self.colorSensor = None
        self.gyroSensor = None
        if configDict is None:
            configDict = self.DEFAULT_CONFIG
        assert (self.LEFT_MOTOR in configDict) and (
            self.RIGHT_MOTOR in configDict)
        self.setupSensorsAndMotors(configDict)

    def setupSensorsAndMotors(self, configDict):
        """Method to set up the sensors and motors based on the input configuration"""
        # TODO: Iterate through the configDict, and for each sensor or motor, set the instance variable
        #  to the right kind of object, and set any other values needed. At the end, define the tankMover
        #  and the steerMover
        map = {
            self.MEDIUM_MOTOR: self.mediumMotor,
            self.LEFT_TOUCH: self.leftTouch,
            self.RIGHT_TOUCH: self.rightTouch,
            self.ULTRA_SENSOR: self.ultraSensor,
            self.COLOR_SENSOR: self.colorSensor,
            self.GYRO_SENSOR: self.gyroSensor
        }
        for key, value in configDict.items():
            map[key] = value
        self.tankMover = MoveTank(
            configDict[self.LEFT_MOTOR], configDict[self.RIGHT_MOTOR])
        self.steerMover = MoveSteering(
            configDict[self.LEFT_MOTOR], configDict[self.RIGHT_MOTOR])

    def readTouch(self):
        """Reports the value of both touch sensors, OR just one if only one is connected, OR
        prints an alert and returns nothing if neither is connected."""
        pass  # TODO: Complete this
        if self.leftTouch is not None and self.rightTouch is not None:
            return self.leftTouch.is_pressed, self.rightTouch.is_pressed
        elif self.leftTouch is not None:
            return self.leftTouch.is_pressed, None
        elif self.rightTouch is not None:
            return None, self.rightTouch.is_pressed
        else:
            print("Warning, no touch sensor connected")
            return None, None

    # TODO: Fill in the rest of the methods according to the description in the homework assignments

    def forward(self, speed, time=None):
        if (time is None):
            self.tankMover.on(SpeedPercent(speed),
                              SpeedPercent(speed), brake=False)
        else:
            self.tankMover.on_for_seconds(SpeedPercent(
                speed), SpeedPercent(speed), time, brake=False)

    def backward(self, speed, time=None):
        if (time is None):
            self.tankMover.on(SpeedPercent(-1*speed),
                              SpeedPercent(-1*speed), brake=False)
        else:
            self.tankMover.on_for_seconds(
                SpeedPercent(-1*speed), SpeedPercent(-1*speed), time, brake=False)

    def turnLeft(self, speed, time=None):
        if (time is None):
            self.tankMover.on(SpeedPercent(-1*speed),
                              SpeedPercent(speed), brake=False)
        else:
            self.tankMover.on_for_seconds(
                SpeedPercent(-1*speed), SpeedPercent(speed), time, brake=False)

    def turnRight(self, speed, time=None):
        if (time is None):
            self.tankMover.on(SpeedPercent(speed),
                              SpeedPercent(-1*speed), brake=False)
        else:
            self.tankMover.on_for_seconds(SpeedPercent(
                speed), SpeedPercent(-1*speed), time, brake=False)

    def stop(self):
        self.tankMover.stop()

    def curve(self, leftSpeed, rightSpeed, time=None):
        self.tankMover.on_for_seconds(leftSpeed, rightSpeed, time)

    def pointerTurn(self, speed=-20, time=None):
        self.mediumMotor.on_for_seconds(speed, time)

    def pointerTurnBy(self, angle, speed=-20):
        self.mediumMotor.on_for_degrees(speed, angle)

    def zeroPointer(self):
        self.mediumMotor.on_to_position(20, 0)

    def pointerTurnTo(self, angle):
        self.mediumMotor.on_to_position(20, angle)


# Sample of how to use this
if __name__ == "__main__":
    firstConfig = {
        SturdyBot.LEFT_MOTOR: OUTPUT_C,
        SturdyBot.RIGHT_MOTOR: OUTPUT_B,
        SturdyBot.LEFT_TOUCH: INPUT_4,
        SturdyBot.RIGHT_TOUCH: INPUT_1,
        SturdyBot.MEDIUM_MOTOR: OUTPUT_A,
    }

    # SturdyBot.MEDIUM_MOTOR: OUTPUT_D}
    # SturdyBot.COLOR_SENSOR: INPUT_1}
    touchyRobot = SturdyBot('Touchy', firstConfig)
    print("Setup done")
