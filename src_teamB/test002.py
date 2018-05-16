import smbus

bus = smbus.SMBus(4)

bus.write_i2c_block_data(addr, ord("abc"), ord("efg"))
