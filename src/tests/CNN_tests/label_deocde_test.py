
import numpy as np
from src.CNN.dataset import decode_label

def test_mask():
    e_out = np.array([[0,0,0,0,0], [0,255,255,0,0], [255,255,255,0,0], [0,255,255,255,0]])
    data = decode_label("src/tests/dif/test_label.in")
    np.testing.assert_array_equal(np.float32(e_out), np.float32(data[0]))
    
def test_comp_masks():
    mask_1 = np.array([[0,0,0,0,0], [0,255,255,0,0], [255,255,0,0,0], [0,0,0,0,0]])
    mask_2 = np.array([[0,0,0,0,0], [0,0,0,0,0], [0,0,255,0,0], [0,255,255,255,0]])
    comp_masks = np.array([mask_1, mask_2])
    data = decode_label("src/tests/dif/test_label.in")
    np.testing.assert_array_equal(np.float32(comp_masks), np.float32(data[1]))

