# MacroKeyboard Raspberry Pi Pico

Macro keyboard project using Raspberry Pi Pico and CircuitPython from Adafruit.

Actions can be triggered by buttons and by bluetooth requests.

#########################
Code.py walkthroug below
#########################

The most important is the commands dictionary:
```python
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
```
Key is used by the bluetooth device.
Command requires 
- logger - by default I recommned ConsoleLogger
- pin - GPIO pin number
- array of actions - array because you can specify a number of profiles

Short cut examples:
Creating C# nunit test empty method
```python
def createTest(self):
        self.logger.info('create test')
        self.write_text.write('[Test]\npublic void ShouldTest()\n{\n\n}\n')
```
Revert change
```python
def revert(self):
        self.logger.info('revert')
        self.kbd.send(Keycode.CONTROL, Keycode.Z)
        self.kbd.release_all()
```
Currently number of supported profiles is related to the stateLeds array:
```python
stateLeds = [
    Led(board.GP14),
    Led(board.GP15),
    #Led(board.GP28)
    ]
```
By default pin 12 change profiles - triggers state.Update action.

numberOfStates = number of profiles - it is injected through the constructor so it can be easlity change to make it not related to the stateLeds array.
```python
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
```

Encoder uses commands + and -
```python
encoder = Encoder(logger, rotor, commands['+'], commands['-'])
```

Supported buttons are defined in the following way:
```python
buttons = [Button(commands[7]),
           Button(commands[8]),
           Button(commands[9]),
           Button(commands[10]),
           Button(commands[11]),
           Button(commands[12]),
           Button(commands[20])]
```
Number is a GPIO pin.

Bluetooth device uses keys from the commands dictionary.
```python
bluetooth = BluetoothDevice(logger, hc05)
```
For example by sending + you will trigger zoom in.

By the way bluetooth device has very short timeout to make it quickly reponse.
In other words - default timeout made keyboard very slowly responsive that is not acceptable for me.
```python
hc05 = busio.UART(board.GP0, board.GP1, baudrate=9600, timeout=0.01)
```
