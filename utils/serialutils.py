import serial
from typing import List


def get_serial_data(serial_port: serial.Serial) -> List[float] | None:
    try:
        # values = serial_port \
        #     .readline() \
        #     .decode("utf-8") \
        #     .rstrip() \
        #     .split(",")

        # return list(map(float, values))

        return [
            26.96,
26.61,
27.57,
27.64,
27.97,
28.46,
28.21,
27.58,
28.49,
28.54,
29.39,
28.06,
30.09,
30.44,
29.37,
30.75,
28.65,
29.61,
27.84,
28.88,
27.47,
27.86,
28.95,
26.92,
27.18,
26.13,
27.46,
26.62,
29.08,
27.97,
27.88,
27.73,
29.04,
28.56,
28.27,
27.59,
30.26,
29.71,
28.68,
30.01,
28.9,
29.65,
29.16,
29.04,
28.8,
27.45,
28.58,
27.98,
26.55,
27.45
        ]

    except ValueError:
        return None
