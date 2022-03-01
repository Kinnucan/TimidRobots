"""
File: timidExample1.py
Note that this example uses the SturdyBot. To do this, you would need to extend our definition of the SturdyBot from HW1
so that it handles the ultrasonic sensor. This is part of the first question on HW2, so feel free to do that. There is a second
version that doesn't use the SturdyBot for the sensor part...
"""

from SturdyBot import SturdyBot
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
import time

class TimidControl(object):

    def __init__(self, robot):
        self.myRobot = robot
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
        self.myRobot.stop()

    def behaviorStep(self):
        """Performs one step of the behavior. Checks the state and the ultrasonic sensor, and either moves forward or stops."""
        distValue = self.myRobot.readDistance()
        if self.state == 'found' and distValue >= self.threshold:
            self.myRobot.forward(40)
            self.state = 'seeking'
        elif self.state == 'seeking' and distValue < self.threshold:
            self.myRobot.stop()
            self.state = 'found'



if __name__ == '__main__':
    # set up robot object here if using it
    # TODO: Fill in specification of robot here to use ultrasonic sensor
    myConfig = {SturdyBot.LEFT_MOTOR: OUTPUT_C,
                SturdyBot.RIGHT_MOTOR: OUTPUT_B,
                SturdyBot.ULTRA_SENSOR: INPUT_1}
    myBot = SturdyBot("Your name here", myConfig)

    timidRunner = TimidControl(myBot)

    timidRunner.runRobot(60)  # Time is set to 60 seconds, but you can always stop it early with a button
    # add code to stop robot motors
    myBot.stop()  # probably redundant, but not going to chance it