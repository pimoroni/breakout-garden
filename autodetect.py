#!/usr/bin/env python
import smbus
import sys

I2C_BUS = 1
DEBUG = False

install_mode = False

if len(sys.argv) > 1:
    if "--install" in sys.argv:
        install_mode = True

try:
    bus = smbus.SMBus(I2C_BUS)
except IOError:
    print("Unable to access /dev/i2c-{}, please ensure i2c is enabled!".format(I2C_BUS))
    sys.exit()


def check_chip_id(i2c_addr, chip_ids):
    if len(chip_ids) == 0:
        return True

    for register in chip_ids:
        value, size, negate_match = chip_ids[register]
        reg, reg_size = register
        if reg_size == 1:
            if size == 1:
                read = bus.read_byte_data(i2c_addr, reg)
            elif size == 2:
                read = bus.read_word_data(i2c_addr, reg)
            else:
                raise RuntimeError("Unsupported Chip ID size: {} byte(s)".format(size))

            if negate_match and value != read:
                return True
            elif value == read:
                return True

        else:
            # TODO: Support 16-bit registers
            raise RuntimeError("Unsupported register size: {} byte(s)".format(size))

    return False


def get_device(line):
    parts=[x.strip() for x in line.split(":")]

    i2c_addr = int(parts[0][0:4], 16)

    chip_ids = {}

    if(len(parts[0]) > 4):
        register_map = parts[0][5:-1].split(',')
        for mapping in register_map:
            if '!=' in mapping:
                register, value = [(int(x, 16), (len(x) - 2) // 2) for x in mapping.split('!=')]
                chip_ids[register] = value[0], value[1], True
            else:
                register, value = [(int(x, 16), (len(x) - 2) // 2) for x in mapping.split('=')]
                chip_ids[register] = value[0], value[1], False

    return i2c_addr, parts[1], parts[2], parts[3], chip_ids

devices = [get_device(line) for line in open("breakouts.config").read().strip().split("\n")]

addresses = set([device[0] for device in devices])


def identify(find_i2c_addr):
    try:
        bus.read_byte_data(find_i2c_addr, 0x00)
    except IOError as e:
        pass

    for i2c_addr, library, module, name, chip_ids in devices:
        if i2c_addr == find_i2c_addr and check_chip_id(i2c_addr, chip_ids):
            installed = True
            try:
                __import__(module)
            except ImportError:
                installed = False
            return installed, library, name

    return None, None, None


found_addr = []
found_devices = {}

for i2c_addr in addresses:
    try:
        bus.read_byte_data(i2c_addr, 0x00)
        if DEBUG: print("Found device on: {:02x}".format(i2c_addr))
        found_addr.append(i2c_addr)
        installed, library, name = identify(i2c_addr)
        if installed is None:
            continue
        if name not in found_devices:
            found_devices[name] = [installed, library, [i2c_addr]]
        else:
            found_devices[name][2].append(i2c_addr)

    except IOError as e:
        if DEBUG: print("IOError reading: {:02x}".format(i2c_addr))
        continue

for name in found_devices:
    installed, library, i2c_addresses = found_devices[name]
    format_string = ""
    if install_mode:
        format_string = "{name}|{library}|{installed}"
    else:
        format_string = "{i2c_addresses}: {name} ({library} {installed})"

    print(format_string.format(
        i2c_addresses = ",".join(["0x{:02x}".format(i2c_addr) for i2c_addr in i2c_addresses]),
            name = name,
            library = library,
            installed = "installed" if installed else "required"
        ))
