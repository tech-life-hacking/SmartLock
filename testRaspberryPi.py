import pigpio
import blynklib
import threading
import socket
import time

################### setting ###################
BLYNK_AUTH = ''
RaspberryPi0IPAddress = ''
RaspberryPi1IPAddress = ''
portnumber0 = ''
portnumber1 = ''
gpio_pin = 12
initialdegree = 0
opendegree = -80
closedegree = 80
###############################################

# initialize
blynk = blynklib.Blynk(BLYNK_AUTH)
pi = pigpio.pi()
pi.set_mode(gpio_pin, pigpio.OUTPUT)


@blynk.handle_event('write V0')
def write_virtual_pin_handler(pin, value):
    if value == ['1']:
        state.drivethethumbturn()
        state.changestate()
        state.displaythestate()
        state.sleeping()


def angle2duty(angle):
    return int(95000 / 180 * angle + 72500)


class Threadblynk(threading.Thread):
    def __init__(self):
        super(Threadblynk, self).__init__()

    def run(self):
        while True:
            blynk.run()

class ThreadSendState(threading.Thread):
    def __init__(self):
        super(ThreadSendState, self).__init__()

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((RaspberryPi0IPAddress, portnumber0))
            while True:
                data, addr = s.recvfrom(1024)
                if data == b'ChangeState':
                    state.changestate()


class State():
    def drivethethumbturn(self):
        raise NotImplementedError("drivethethumbturn is abstractmethod")

    def displaythestate(self):
        raise NotImplementedError("displaythestate is abstractmethod")

    def sleeping(self):
        raise NotImplementedError("sleeping is abstractmethod")

    def sendstate(self):
        raise NotImplementedError("sendstate is abstractmethod")

    def changestate(self):
        raise NotImplementedError("changestate is abstractmethod")


class Open(State):
    def drivethethumbturn(self):
        thumbturn.turn(closedegree)

    def displaythestate(self):
        blynk.virtual_write(2, "Open")

    def sleeping(self):
        time.sleep(1)

    def sendstate(self):
        client.sendto(b'ChangeState', (RaspberryPi1IPAddress, portnumber1))

    def changestate(self):
        state.change_state("Close")


class Close(State):
    def drivethethumbturn(self):
        thumbturn.turn(opendegree)

    def displaythestate(self):
        blynk.virtual_write(2, "Close")

    def sleeping(self):
        time.sleep(1)

    def sendstate(self):
        client.sendto(b'ChangeState', (RaspberryPi1IPAddress, portnumber1))

    def changestate(self):
        state.change_state("Open")


class Context:
    def __init__(self):
        self.open = Open()
        self.close = Close()
        self.state = self.open

    def change_state(self, event):
        if event == "Open":
            self.state = self.open
        elif event == "Close":
            self.state = self.close
        else:
            raise ValueError(
                "change_state method must be in {}".format(["open", "close"]))

    def drivethethumbturn(self):
        self.state.drivethethumbturn()

    def displaythestate(self):
        self.state.displaythestate()

    def sleeping(self):
        self.state.sleeping()

    def sendstate(self):
        self.state.sendstate()

    def changestate(self):
        self.state.changestate()

class Thumbturn():
    def __init__(self, initialdegree):
        self.degree = initialdegree

    def turn(self, degree=0):
        self.degree += degree
        pi.hardware_PWM(gpio_pin, 50, angle2duty(self.degree))


if __name__ == '__main__':

    # initialization
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    thumbturn = Thumbturn(initialdegree)
    state = Context()
    thumbturn.turn()

    thsendstate = ThreadSendState()
    thsendstate.start()

    # start blynk
    thblynk = Threadblynk()
    thblynk.start()

