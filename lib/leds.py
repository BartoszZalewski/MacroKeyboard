import digitalio

class Led:
    def __init__(self, pin):
        self.led = digitalio.DigitalInOut(pin)
        self.led.direction = digitalio.Direction.OUTPUT
    
    def On(self):
        self.led.value = True

    def Off(self):
        self.led.value = False

class LedSwitch:
    def __init__(self, logger, leds):
        self.logger = logger
        self.leds = leds
    
    def switch(self, index):
        for led in self.leds:
            led.Off()
        ledsSize = len(self.leds)
        if ledsSize <= index:
            self.logger.info('Number of supported leds ({}) is lover than index {}'.format(ledsSize, index))
            index = 0
        self.leds[index].On()