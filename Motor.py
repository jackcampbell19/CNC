import RPi.GPIO as GPIO
from time import sleep
from threading import Thread


GPIO.setmode(GPIO.BOARD)


class Stepper:

    SHORTEST_DELAY = 0.002

    def __init__(self, stp, dir, ms1, ms2, slp):
        self.stp = stp
        self.dir = dir
        self.ms1 = ms1
        self.ms2 = ms2
        self.slp = slp
        for pin in [self.stp, self.dir, self.ms1, self.ms2, self.slp]:
            GPIO.setup(pin, GPIO.OUT)
        self.current_step = 0
        self.switch_on()
        self.set_full_step()

    def step(self, forward):
        if forward:
            self.current_step += 1
            GPIO.output(self.dir, 0)
            GPIO.output(self.stp, 0)
            GPIO.output(self.stp, 1)
        else:
            self.current_step -= 1
            GPIO.output(self.dir, 1)
            GPIO.output(self.stp, 0)
            GPIO.output(self.stp, 1)

    def set_full_step(self):
        GPIO.output(self.ms1, 0)
        GPIO.output(self.ms2, 0)

    def set_half_step(self):
        GPIO.output(self.ms1, 1)
        GPIO.output(self.ms2, 0)

    def set_quarter_step(self):
        GPIO.output(self.ms1, 0)
        GPIO.output(self.ms2, 1)

    def set_eigth_step(self):
        GPIO.output(self.ms1, 1)
        GPIO.output(self.ms2, 1)

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
        GPIO.output(self.slp, 0)

    def switch_on(self):
        GPIO.output(self.slp, 1)
