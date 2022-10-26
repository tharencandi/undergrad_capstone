from CNN.dataset import encode_label, decode_label
def test_encode():
    mask = decode_label("data/training/image01_mask.txt")[0]
    r = encode_label(mask, "src/tests/CNN_tests/diff/", "test_mask.txt")
    assert r == 0

    actual = open("src/tests/CNN_tests/diff/test_mask.txt", "r").readlines()
    expected = open("data/training/image01_mask.txt", "r").readlines()
    assert len(actual) == len(expected)
    assert all([((a != '0\n' and b != '0\n') or (a == '0\n' and b == '0\n')) for a, b in zip(actual, expected)])


