import numpy as np


class BasicLight(object):
    dtype = np.dtype([
        ('pos', np.float32, 3),
        ('color', np.float32, 3),
        ('casts_shadow', np.int32),
        ('padding', np.int32),
    ])

    """
    __array__ is called when a BasicLight is being converted to a numpy array.
    Then, one can assign that numpy array to an optix variable/buffer. The format will be user format.
    Memory layout (dtype) must match with the corresponding C struct in the device code.
    """
    def __array__(self):
        np_array = np.zeros(1, dtype=BasicLight.dtype)
        np_array['pos'] = self._pos
        np_array['color'] = self._color
        np_array['casts_shadow'] = 1 if self._casts_shadow else 0
        np_array['padding'] = 0
        return np_array

    def __init__(self, pos, color, casts_shadow):
        self._pos = pos
        self._color = color
        self._casts_shadow = casts_shadow
