import board
import busio
import rotaryio
import board
import digitalio
import usb_hid
import time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.keycode import Keycode
from shortCuts import ShortCuts
from logger import ConsoleLogger
from leds import Led
from leds import LedSwitch

cc = ConsumerControl(usb_hid.devices)
kbd = Keyboard(usb_hid.devices)
write_text = KeyboardLayoutUS(kbd)
hc05 = busio.UART(board.GP0, board.GP1, baudrate=9600, timeout=0.01)

class BluetoothDevice:
    def __init__(self,logger, hc05):
        self.logger = logger
        self.hc05 = hc05
        
    def read(self):
        request = self.hc05.readline()
        if request is not None:
            formatted = str(request, 'utf-8')
            response = 'received: {}'.format(formatted)
            self.logger.info(response)
            hc05.write(bytes(response, 'ascii'))
            try:
                integer = int(formatted, 0)
                return integer
            except ValueError:
                pass
            return formatted.strip()
        return None

class Command:
    def __init__(self, logger, pin, actions):
        self.logger = logger
        self.pin = pin
        self.actions = actions
    
    def execute(self, index):
        if len(self.actions) <= index:
            self.logger.info('Command for pin {} does not support index {}'.format(self.pin, index))
            self.logger.info('Use index 0 instead')
            index = 0 
        action = self.actions[index]
        action()
        
    def gp(self):
        if self.pin == 7:
            return board.GP7
        if self.pin == 8:
            return board.GP8
        if self.pin == 9:
            return board.GP9
        if self.pin == 10:
            return board.GP10
        if self.pin == 11:
            return board.GP11
        if self.pin == 12:
            return board.GP12
        if self.pin == 20:
            return board.GP20

        self.logger.info('Pin is not supported yet: '+ pin)
        return None
        
class Button:
    def __init__(self, command):
        self.state = None
        self.command = command
        pin = command.gp()
        self.button = digitalio.DigitalInOut(pin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP
    
    def click(self, index):
        value = self.button.value
        if not value and self.state is None:
            self.state = "pressed"
        if value and self.state == "pressed":
            self.state = None
            self.command.execute(index)
            
class State:
    def __init__(self, logger, initialValue, numberOfStates, actionOnChange):
        self.logger = logger
        self.value = initialValue
        self.numberOfStates = numberOfStates
        self.actionOnChange = actionOnChange
    
    def update(self):
        self.value = (self.value + 1) % self.numberOfStates
        self.actionOnChange(self.value)
        self.logger.info(self.value)
        
    def getValue(self):
        return self.value
    

class Encoder:
    def __init__(self, logger, rotor, rightCommands, leftCommands):
        self.logger = logger
        self.rotor = rotor
        self.rightCommands = rightCommands
        self.leftCommands = leftCommands
        self.position = None
        self.last_position = 0
    
    def update(self, index):
        self.position = self.rotor.position
        if self.last_position is None or self.position != self.last_position:
            self.logger.info('Current encoder position is {}'.format(self.position))
            if self.last_position < self.position:
                self.rightCommands.execute(index)
            else:
                self.leftCommands.execute(index)
        self.last_position = self.position

logger = ConsoleLogger()

rotor = rotaryio.IncrementalEncoder(board.GP18, board.GP19)

stateLeds = [
    Led(board.GP14),
    Led(board.GP15),
    #Led(board.GP28)
    ]

ledSwitch = LedSwitch(logger, stateLeds)

initialState = 0
ledSwitch.switch(initialState)
state = State(logger, initialState, len(stateLeds), ledSwitch.switch)

shortCuts = ShortCuts(logger, kbd, cc, write_text)

commands = {
    7 : Command(logger, 7, [shortCuts.revert, shortCuts.undoRevert]),
    8 : Command(logger, 8, [shortCuts.undoRevert, shortCuts.revert]),
    9 : Command(logger, 9, [shortCuts.gitStatus]),
    10: Command(logger, 10, [shortCuts.createTest]),
    11 : Command(logger, 11, [shortCuts.pause]),
    12 : Command(logger, 12, [state.update]),
    20 : Command(logger, 20, [shortCuts.resetZoom]),
    '+' : Command(logger, -1, [shortCuts.zoomIn]),
    '-' : Command(logger, -1, [shortCuts.zoomOut])
    }

encoder = Encoder(logger, rotor, commands['+'], commands['-'])

buttons = [Button(commands[7]),
           Button(commands[8]),
           Button(commands[9]),
           Button(commands[10]),
           Button(commands[11]),
           Button(commands[12]),
           Button(commands[20])]

bluetooth = BluetoothDevice(logger, hc05)

def handleRemoteCommand(remoteValue):
    if remoteValue in commands:
        commands[remoteValue].execute(state.getValue())
    else:
        if remoteValue is not None:
            logger.info('Remote value {} is not supported!'.format(remoteValue))

while True:
    encoder.update(state.getValue())
        
    for button in buttons:
        button.click(state.getValue())
    
    handleRemoteCommand(bluetooth.read())

        
    