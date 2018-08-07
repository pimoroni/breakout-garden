import smbus
import sys

I2C_BUS = 1

install_mode = False

if len(sys.argv) > 1:
    if "--install" in sys.argv:
        install_mode = True

try:
    bus = smbus.SMBus(I2C_BUS)
except IOError:
    print("Unable to access /dev/i2c-{}, please ensure i2c is enabled!".format(I2C_BUS))
    sys.exit()

devices = [(int(line.split(":")[0].replace('0x',''), 16), line.split(":")[1].strip(), line.split(":")[2].strip()) for line in open("breakouts.config").read().strip().split("\n")]

addresses = [device[0] for device in devices]

def identify(find_i2c_addr):
    for i2c_addr, library, name in devices:
        if i2c_addr == find_i2c_addr:
            return library, name
    return None

found_addr = []

for i2c_addr in addresses:
    try:
        bus.read_byte_data(i2c_addr, 0x00)
        found_addr.append(i2c_addr)
    except IOError as e:
        continue

for i2c_addr in found_addr:
    library, name = identify(i2c_addr)
    if install_mode:
        print("{library}".format(library=library))
    else:
        print("0x{addr:02x}: {name} (https://github.com/pimoroni/{library})".format(addr=i2c_addr, name=name, library=library))
