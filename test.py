import pigpio

def angle2duty(angle):
    return int(95000 / 180 * angle + 72500)

if __name__ == '__main__':

    pi = pigpio.pi()
    gpio_pin = 12
    pi.set_mode(gpio_pin, pigpio.OUTPUT)

    x = 0
    pi.hardware_PWM(gpio_pin,50,angle2duty(x))