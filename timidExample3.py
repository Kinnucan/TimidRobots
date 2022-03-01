"""
File: timidExample3.py
This example does not use the SturdyBot at all, but creates a Tank motorset to control the robot. a bit more clunky,
but works.
"""

from ev3dev2.motor import MoveTank
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.button import Button
from ev3dev2.sound import Sound
import time

class TimidControl(object):

    def __init__(self, tankset, ultraSensor):
        self.myTank = tankset
        self.ultra = ultraSensor
        self.state = 'found'
        self.threshold = 30
        self.bttn = Button()
        self.snd  = Sound()


    def runRobot(self, runTime = None):
        """Takes in an optional time to run. It runs a loop that calls the behaviorStep method over and over until
        either the time runs out or a button is pressed."""
        startTime = time.time()
        elapsedTime = time.time() - startTime
        self.snd.speak("Starting")
        while (not self.bttn.any()) and ((runTime is None) or (elapsedTime < runTime)):
            self.behaviorStep()
            # Could add time.sleep here if need to slow loop down
            elapsedTime = time.time() - startTime
        self.snd.speak("Done")
        self.myTank.stop()

    def behaviorStep(self):
        """Performs one step of the behavior. Checks the state and the ultrasonic sensor, and either moves forward or stops."""
        distValue = self.ultra.distance_centimeters
        if self.state == 'found' and distValue >= self.threshold:
            self.myTank.on(40, 40)
            self.state = 'seeking'
        elif self.state == 'seeking' and distValue < self.threshold:
            self.myTank.stop()
            self.state = 'found'



if __name__ == '__main__':
    # set up robot object here if using it
    myTank = MoveTank(OUTPUT_C, OUTPUT_B) # TODO: Change this to match your robot's output to motors
    uSense = UltrasonicSensor(INPUT_1)  # TODO: Change this to match your robot's input from ultrasonic sensor
    timidRunner = TimidControl(myTank, uSense)
    timidRunner.runRobot(60)  # Time is set to 60 seconds, but you can always stop it early with a button

    # add code to stop robot motors
    myTank.stop()  # probably redundant, but not going to chance it