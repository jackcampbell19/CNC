import RPi.GPIO as GPIO
from time import sleep
from threading import Thread


GPIO.setmode(GPIO.BOARD)


class Stepper:

    FULL_STEP_SEQUENCE = [
        (1, 0, 0, 1),
        (1, 1, 0, 0),
        (0, 1, 1, 0),
        (0, 0, 1, 1)
    ]

    HALF_STEP_SEQUENCE = [
        (1, 0, 0, 0),
        (1, 1, 0, 0),
        (0, 1, 0, 0),
        (0, 1, 1, 0),
        (0, 0, 1, 0),
        (0, 0, 1, 1),
        (0, 0, 0, 1),
        (1, 0, 0, 1)
    ]

    SHORTEST_DELAY = 0.008

    def __init__(self, in1, in2, in3, in4, StepAngle, StepSequence):
        self.pins = [in1, in2, in3, in4]
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
        self.steps_per_rotation = int(360.0 / StepAngle * (len(StepSequence) / 4))
        self.sequence = StepSequence
        self.sequence_length = len(StepSequence)
        self.current_step = 0

    def step(self, forward):
        self.current_step += 1 if forward else -1
        pattern = self.sequence[self.current_step % self.sequence_length]
        for i in range(4):
            GPIO.output(self.pins[i], pattern[i])

    def rotate_to(self, step, delay=SHORTEST_DELAY):
        number_of_steps = step - self.current_step
        forward = number_of_steps > 0
        number_of_steps = abs(number_of_steps)

        def threadfun():
            for _ in range(number_of_steps):
                if forward:
                    self.step(True)
                else:
                    self.step(False)
                sleep(delay)

        return Thread(target=threadfun)

    def switch_off(self):
        for i in range(4):
            GPIO.output(self.pins[i], False)
