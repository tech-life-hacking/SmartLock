import pigpio
import blynklib
import threading

################### setting ###################
BLYNK_AUTH = 'BW-OY7yiT4hVfh2BzXR_x3xy23j7Nkyr'
RaspberryPiIPAdress = '192.168.11.7'
gpio_pin = 12
initialdegree = 20
opendegree = 20
closedegree = 100
###############################################

# initialize
blynk = blynklib.Blynk(BLYNK_AUTH)
pi = pigpio.pi()
pi.set_mode(gpio_pin, pigpio.OUTPUT)

@blynk.handle_event('write V0')
def write_virtual_pin_handler(pin, value):
    if value == ['1']:
        tvstate.turnTV()
        tvstate.changingtimer()

def angle2duty(angle):
    return int(95000 / 180 * angle + 72500)

class Threadblynk(threading.Thread):
    def __init__(self):
        super(Threadblynk, self).__init__()

    def run(self):
        while True:
            blynk.run()

class State():
    def drivethethumbturn(self):
        raise NotImplementedError("drivethethumbturn is abstractmethod")

    def displaythestate(self):
        raise NotImplementedError("displaythestate is abstractmethod")

class Open(State):
    def drivethethumbturn(self):
        pi.hardware_PWM(gpio_pin,50,angle2duty(closedegree))
        time.sleep(3)
        state.change_state("Close")

    def displaythestate(self):
        blynk.virtual_write(2, "Open")

class Close(State):
    def drivethethumbturn(self):
        pi.hardware_PWM(gpio_pin,50,angle2duty(closedegree))
        time.sleep(3)
        state.change_state("Open")

    def displaythestate(self):
        blynk.virtual_write(2, "Close")

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
            raise ValueError("change_state method must be in {}".format(["open", "close"]))

    def drivethethumbturn(self):
        self.state.drivethethumbturn()

    def displaythestate(self):
        self.state.displaythestate()

if __name__ == '__main__':

    # initialization
    pi.hardware_PWM(gpio_pin,50,angle2duty(initialdegree))

    state = Context()

    # start blynk
    thblynk = Threadblynk()
    thblynk.start()

    # start communication
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((''+RaspberryPiIPAdress+'', 50007))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    data = b''
                    data = conn.recv(1024)
                    if data == b'Me':
                        state.drivethethumbturn()
                    else:
                        pass