import os
import cv2
import numpy as np
from typing import List
from numpy.typing import NDArray
from matplotlib.pyplot import cm
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression


WIDTH = 960
HEIGHT = 720
MIN_TEMP = 0.0
MAX_TEMP = 4095.0
TEMP_RANGE = MAX_TEMP - MIN_TEMP
AUTO_ADJUST = False

KNN = KNeighborsRegressor(3)

SENSOR_X = np.array([
    655, 722, 780, 633, 689, 750, 800, 684, 777, 684, 755, 
    675, 743, 661, 740, 698, 300, 239, 178, 325, 266, 207, 
    156, 276, 180, 270, 202, 286, 213, 298, 221, 258
])

SENSOR_Y = np.array([
    117, 97, 126, 204, 202, 213, 244, 299, 319, 377, 396, 
    488, 504, 581, 579, 623, 118, 100, 127, 203, 203, 212, 
    244, 298, 318, 379, 397, 487, 503, 578, 577, 624
])

TRAIN_X = np.stack([SENSOR_X, SENSOR_Y], axis=1)

X1 = np.repeat(np.arange(WIDTH), HEIGHT)
X2 = np.tile(np.arange(HEIGHT), WIDTH)

TEST_X = np.stack([X1, X2], axis=1)

TEMPLATE_PATH = os.path.join(os.getcwd(), "assets", "template.png")
TEMPLATE = cv2.imread(TEMPLATE_PATH, cv2.IMREAD_GRAYSCALE)
MASK = TEMPLATE == 255

BLUR_SIZE = 101


class Thermogram(object):

    @staticmethod
    def apply_brightness_contrast(
        image: NDArray[np.uint8],
        brightness: int = 64,
        contrast: int = 32
    ) -> NDArray[np.uint8]:
        if brightness != 0:
            if brightness > 0:
                shadow = brightness
                highlight = 255
            else:
                shadow = 0
                highlight = 255 + brightness
            alpha_b = (highlight - shadow) / 255
            gamma_b = shadow

            buffer = cv2.addWeighted(image, alpha_b, image, 0, gamma_b)
        else:
            buffer = image.copy()

        if contrast != 0:
            f = 131 * (contrast + 127) / (127 * (131 - contrast))
            alpha_c = f
            gamma_c = 127 * (1 - f)

            buffer = cv2.addWeighted(buffer, alpha_c, buffer, 0, gamma_c)

        return buffer

    @staticmethod
    def interpolate(image: NDArray, scale: int = 30) -> NDArray[np.uint8]:
        return cv2.resize(
            image,
            dsize=None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_LINEAR
        )

    @staticmethod
    def gaussian_blur(image: NDArray, ksize: int = 7) -> NDArray[np.uint8]:
        return cv2.GaussianBlur(image, (ksize, ksize), 0) * 3

    @staticmethod
    def average_blur(image: NDArray, ksize: int = 31) -> NDArray[np.uint8]:
        return cv2.blur(image, ksize=(ksize, ksize))

    @staticmethod
    def generate_thermogram(
        pressure: NDArray[np.float32] | List[float]
    ) -> NDArray[np.uint8]:
        pressure = np.array(pressure, dtype=np.float32)

        pressure = pressure / TEMP_RANGE

        KNN.fit(TRAIN_X, pressure)
        thermogram = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        thermogram[X2, X1, :] = cm.jet(KNN.predict(TEST_X))[:, :-1] * 255
        thermogram = cv2.GaussianBlur(thermogram, (BLUR_SIZE, BLUR_SIZE), 0)
        thermogram[MASK, :] = [40, 44, 52]

        return thermogram
