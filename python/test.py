from fallDetection import fall_detection, magnitudes, calc_params

def test_fall_detection_positive():
    will_fall = fall_detection()
    assert will_fall == 1

def test_fall_detection_negative():
    will_fall = fall_detection()
    assert will_fall == 0

def test_magnitudes():
    data =
    type =
    sol =
    mag = magnitudes(data, type)
    assert mag == sol

def test_params():
    window =
    sol =
    params = calc_params(window)
    assert params == sol