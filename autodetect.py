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
found_devices = {}

for i2c_addr in addresses:
    try:
        bus.read_byte_data(i2c_addr, 0x00)
        found_addr.append(i2c_addr)
        library, name = identify(i2c_addr)
        if name not in found_devices:
            found_devices[name] = [library, [i2c_addr]]
        else:
            found_devices[name][1].append(i2c_addr)
    except IOError as e:
        continue

for name in found_devices:
    library, i2c_addresses = found_devices[name]
    format_string = ""
    if install_mode:
        format_string = "{library}"
    else:
        format_string = "{i2c_addresses}: {name} ({library})"

    print(format_string.format(
        i2c_addresses = ",".join(["0x{:02x}".format(i2c_addr) for i2c_addr in i2c_addresses]),
            name = name,
            library = library
        ))
