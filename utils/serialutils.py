import serial
from typing import List


def get_serial_data(serial_port: serial.Serial) -> List[float] | None:
    try:
        values = serial_port \
            .readline() \
            .decode("utf-8") \
            .rstrip() \
            .split(",")
        
        print(values)

        return list(map(float, values)) + list(map(float, values))

        # return [
        #     4000, 4000, 4000, 4095, 4095, 4095, 4095, 3000, 3000,
        #     0, 2000, 0, 0, 0, 0, 0,
        #     3000, 3000, 3000, 3500, 3500, 3500, 3500, 3000, 3000,
        #     0, 2000, 0, 0, 4095, 4095, 4095,
        # ]

    except ValueError:
        return None
