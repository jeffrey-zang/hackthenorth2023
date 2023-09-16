from serial import Serial
from time import sleep

arduino = Serial(port="/dev/ttyUSB0 - 1a86", baudrate=115200, timeout=1)

def write(data):
    arduino.write(bytes(data, "utf-8"))
    print(f"wrote {data}")
    sleep(0.05)
    response = arduino.readline().decode()
    print(response)
    return response

