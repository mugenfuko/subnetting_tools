import random

def is_integer(str):
    try:
        str = float(str)
    except ValueError:
        return False
    return True

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

def is_ipv4_address(str):
    # Check if address has 3 dots
    if str.count('.') != 3:
        return False
    
    # Convert to array if there are 3 dots
    arr = str.split('.')
    
    for n in arr:
        # Check if each variable in array is integer
        if not is_integer(n):
            return False
        # Check if each variable in array is 0-255
        if int(n) < 0 or int(n) > 255:
            return False
    return True

def is_netmask(str):
    NETMASK_VALUES = generate_netmask_values()
    # Check if IPv4 address format
    if not is_ipv4_address(str):
        return False
    arr = str.split('.')
    for i, n in enumerate(arr):
        n = int(n)
        # Check if values are possible netmask values
        if n not in NETMASK_VALUES:
            return False
            break
        if i > 0:
            # Check for logical sequencing of netmask
            prev = int(arr[i-1])
            if n > 0 and prev != 255:
                return False
                break
            if n > prev:
                return False
                break
    return True

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