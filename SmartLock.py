import blynklib
import RPi.GPIO as GPIO
import time
import threading
from face2name import FaceDetection

BLYNK_AUTH = 'YOUR_AUTH'

# initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

# initialize Jetson.GPIO
output_pin = 33

# Pin Setup:
# Board pin-numbering scheme
GPIO.setmode(GPIO.BOARD)
# set pin as an output pin with optional initial state of HIGH
GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.HIGH)
servo = GPIO.PWM(output_pin, 50)
servo.start(0)
opendutycycle = 11.15 #regulate the value
closedutycycle = 7.00 #regulate the value

# initialize Face Detection
facedetection = FaceDetection()

class State():
    def drivethethumbturn(self):
        raise NotImplementedError("drivethethumbturn is abstractmethod")

    def displaythestate(self):
        raise NotImplementedError("displaythestate is abstractmethod")

class Open(State):
    def drivethethumbturn(self):
        pass

    def displaythestate(self):
        pass

class Close(State):
    def drivethethumbturn(self):
        pass

    def displaythestate(self):
        pass

class Close2Open(State):
    def __init__(self,opendutycycle):
        self.opendutycycle = opendutycycle

    def drivethethumbturn(self):
        servo.ChangeDutyCycle(self.opendutycycle)

    def displaythestate(self):
        blynk.virtual_write(2, "Open")

class Open2Close(State):
    def __init__(self,closedutycycle):
        self.closedutycycle = closedutycycle

    def drivethethumbturn(self):
        servo.ChangeDutyCycle(self.closedutycycle)

    def displaythestate(self):
        blynk.virtual_write(2, "Close")

class Context:
    def __init__(self):
        self.open = Open()
        self.close = Close()
        self.close2open = Close2Open(opendutycycle)
        self.open2close = Open2Close(closedutycycle)
        self.state = self.open2close
        self.laststate = self.open

    def change_state(self, event):
        if event == "Close2Open" and self.laststate == self.close:
            self.state = self.close2open
            self.laststate = self.close2open
        elif event == "Close2Open" and self.laststate == self.close2open:
            self.state = self.open
            self.laststate = self.open
        elif event == "Close2Open" and self.laststate == self.open:
            pass
        elif event == "Open2Close" and self.laststate == self.open:
            self.state = self.open2close
            self.laststate = self.open2close
        elif event == "Open2Close" and self.laststate == self.open2close:
            self.state = self.close
            self.laststate = self.close
        elif event == "Open2Close" and self.laststate == self.close:
            pass
        else:
            raise ValueError("change_state method must be in {}".format(["open", "close","close2Open","open2Close"]))

    def drivethethumbturn(self):
        self.state.drivethethumbturn()

    def displaythestate(self):
        self.state.displaythestate()

class Event():
    def __init__(self):
        self.event = "Open2Close"

    def setter(self,event):
        self.event = event

    def getter(self):
        return self.event

# Register virtual pin handler
@blynk.handle_event('write V0')
def close2open(pin, value):
    event.setter("Close2Open")

# Register virtual pin handler
@blynk.handle_event('write V1')
def open2close(pin, value):
    event.setter("Open2Close")

class Threadblynk(threading.Thread):
    def __init__(self):
        super(Threadblynk, self).__init__()
 
    def run(self):
        while True:
            blynk.run()

class ThreadFaceDetection(threading.Thread):
    def __init__(self):
        super(ThreadFaceDetection, self).__init__()

    def run(self):
        while True:
            flag = facedetection.run(True)
            if flag:
                event.setter("Close2Open")

class ThreadEvent(threading.Thread):
    def __init__(self):
        super(ThreadEvent, self).__init__()
 
    def run(self):
        while True:
            getevent = event.getter()
            obj.change_state(getevent)
            obj.drivethethumbturn()
            obj.displaythestate()

if __name__ == '__main__':
    event = Event()
    obj = Context()
    thblynk = Threadblynk()
    thfacedetection = ThreadFaceDetection()
    thevent = ThreadEvent()

    try:
        thblynk.start()
        thfacedetection.start()
        thevent.start()
    except:
        thfacedetection.start()
