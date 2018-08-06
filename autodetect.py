import smbus

bus = smbus.SMBus(1)

devices = [(int(line.split(":")[0].replace('0x',''), 16), line.split(":")[1].strip(), line.split(":")[2].strip()) for line in open("breakouts.config").read().strip().split("\n")]

def identify(find_i2c_addr):
    for i2c_addr, library, name in devices:
        if i2c_addr == find_i2c_addr:
            return library, name
    return None

found_addr = []

for i2c_addr in range(0x03,0x77):
    try:
        bus.read_byte_data(i2c_addr, 0x00)
        found_addr.append(i2c_addr)
    except IOError:
        continue

for i2c_addr in found_addr:
    library, name = identify(i2c_addr)
    print("0x{addr:02x}: {name} (https://github.com/pimoroni/{library})".format(addr=i2c_addr, name=name, library=library))
