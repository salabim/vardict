import pytest

if __name__ == "__main__":  # to make the tests run without the pytest cli
    import os, sys  # three lines to use the local package and chdir
    os.chdir(os.path.dirname(__file__))
    sys.path.insert(0, os.path.dirname(__file__) + "/../")

from vardict import vardict

def test_normal():
    one = 1
    two = 2
    numbers12 = {"one": 1, "two": 2}
    numbers3 = {"three": 3}

    assert vardict(one, two, three=3) == {"one": 1, "two": 2, "three": 3}
    assert vardict(numbers12, three=3) == {"numbers12": {"one": 1, "two": 2}, "three": 3}
    assert vardict(numbers12, numbers3) == {"numbers12": {"one": 1, "two": 2}, "numbers3": {"three": 3}}
    assert vardict(three=3) == {"three": 3}

if __name__ == "__main__":
    pytest.main(["-vv", "-s", "-x", __file__])
