import random

def generate_netmask_values():
    # Generate possible netmask values
    values = [0]
    i = 128
    increment = 128
    while i < 256:
        values.append(int(i))
        increment = increment / 2
        if (increment < 1.0):
                break
        i += increment
    return values

# Functions below are for testing purposes
def generate_random_ip():
    ip = []
    i = 0
    while i < 4:
        ip.append(str(random.randint(0, 255)))
        i += 1
    return ip

def generate_random_netmask(netmask_values=generate_netmask_values()):
    nm = []
    i = 0
    lt255 = False
    while i < 4:
        if not lt255:
            x = random.randint(0, len(netmask_values)-1)
            nm.append(str(netmask_values[x]))
            if netmask_values[x] < 255:
                lt255 = True
        else:
            nm.append('0')
        i += 1
    return nm