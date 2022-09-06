import pytest
import numpy as np
from CNN.dataset import *

def test_NBL_exception():
    image = np.array([[[0,0,0], [0,0,0]], [[0,0,0], [0,0,0]]])
    mask = np.array([0,0])
    print(image.shape)
    print(mask.shape)
    data = ([image], [mask])
    with pytest.raises(Exception):
        gen_NBL(data, "s")


def test_NBD_SN_exception():
    image = np.array([[[0,0,0], [0,0,0]], [[0,0,0], [0,0,0]]])
    mask = np.array([0,0])
    print(image.shape)
    print(mask.shape)
    data = ([image], [mask])
    with pytest.raises(Exception):
        gen_NBD_and_SN(data, "s")