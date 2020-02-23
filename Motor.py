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

    def __init__(self, a, b, c, d, StepAngle, StepSequence):
        self.pins = [a, b, c, d]
        GPIO.setup(a, GPIO.OUT)
        GPIO.setup(b, GPIO.OUT)
        GPIO.setup(c, GPIO.OUT)
        GPIO.setup(d, GPIO.OUT)
        self.steps_per_rotation = int(360.0 / StepAngle * (len(StepSequence) / 4))
        self.sequence = StepSequence
        self.sequence_length = len(StepSequence)
        self.step = 0

    def step_forward(self):
        self.step += 1
        pattern = self.sequence[self.step % self.sequence_length]
        for i in range(4):
            GPIO.output(self.pins[i], pattern[i])

    def step_backward(self):
        self.step -= 1
        pattern = self.sequence[self.step % self.sequence_length]
        for i in range(4):
            GPIO.output(self.pins[i], pattern[i])

    def rotate_to(self, step, delay):
        number_of_steps = step - self.step
        forward = number_of_steps > 0
        number_of_steps = abs(number_of_steps)

        def threadfun():
            for _ in range(number_of_steps):
                if forward:
                    self.step_forward()
                else:
                    self.step_backward()
                sleep(delay)

        return Thread(target=threadfun)