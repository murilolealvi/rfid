from serial import Serial

ser = Serial(port="/dev/ttyUSB0", baudrate=9600)

tag_id = ser.readline().decode("utf-8")[:-2]
print(tag_id)