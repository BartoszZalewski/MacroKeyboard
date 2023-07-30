from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode

class ShortCuts:
    def __init__(self, logger,kbd, cc, write_text):
        self.logger = logger
        self.kbd = kbd
        self.cc = cc
        self.write_text = write_text
        
    def resetZoom(self):
        self.logger.info('reset zoom')
        self.kbd.send(Keycode.CONTROL, Keycode.KEYPAD_ZERO)
        self.kbd.release_all()
    
    def revert(self):
        self.logger.info('revert')
        self.kbd.send(Keycode.CONTROL, Keycode.Z)
        self.kbd.release_all()
        
    def undoRevert(self):
        self.logger.info('undo revert')
        self.kbd.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.Z)
        self.kbd.release_all()
        
    def pause(self):
        self.logger.info('play / pause')
        self.cc.send(ConsumerControlCode.PLAY_PAUSE)
        
    def createTest(self):
        self.logger.info('create test')
        self.write_text.write('[Test]\npublic void ShouldTest()\n{\n\n}\n')
    
    def gitStatus(self):
        self.logger.info('git status command')
        self.write_text.write('git status')
        
    def zoomIn(self):
        self.logger.info('zoom in')
        self.kbd.send(Keycode.CONTROL, Keycode.KEYPAD_PLUS)
        self.kbd.release_all()
        
    def zoomOut(self):
        self.logger.info('zoom out')
        self.kbd.send(Keycode.CONTROL, Keycode.KEYPAD_MINUS)
        self.kbd.release_all()