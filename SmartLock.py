import blynklib
import pigpio

# set value
BLYNK_AUTH = 'YourAuthToken'
output_pin = 12
open_pulsewidth = 2500
close_pulsewidth = 1600

# initialize
blynk = blynklib.Blynk(BLYNK_AUTH)
pi = pigpio.pi()

# register handler for virtual pin V0 write event
@blynk.handle_event('write V0')
def open(pin, value):
    pi.set_servo_pulsewidth(output_pin, open_pulsewidth)

# register handler for virtual pin V1 write event
@blynk.handle_event('write V1')
def close(pin, value):
    pi.set_servo_pulsewidth(output_pin, close_pulsewidth)


###########################################################
# infinite loop that waits for event
###########################################################
while True:
    blynk.run()
