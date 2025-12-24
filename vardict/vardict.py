import inspect
import executing

__version__ = "1.0.0"

class vardict(dict):
    def __new__(cls, *args, **kwargs):
        if len(args) == 0:
            dict(kwargs)
        call_frame = inspect.currentframe().f_back
        call_node = executing.Source.executing(call_frame).node
        if call_node is None:
            raise ValueError("could not assess variables")
        result = {}
        source = executing.Source.for_frame(call_frame)
        for node, right in zip(call_node.args, args):
            left = source.asttokens().get_text(node)
            if not left.isidentifier():
                raise ValueError(f"{left!r} not a valid identifier")
            if left in kwargs:
                raise ValueError(f"parameter {left!r} repeated")
            result[left] = right
        return result | kwargs

if __name__ == "__main__":
    one = 1
    two = 2
    numbers12 = {"one": 1, "two": 2}
    numbers3 = {"three": 3}

    assert vardict(one, two, three=3) == {"one": 1, "two": 2, "three": 3}
    assert vardict(numbers12, three=3) == {"numbers12": {"one": 1, "two": 2}, "three": 3}
    assert vardict(numbers12, numbers3) == {"numbers12": {"one": 1, "two": 2}, "numbers3": {"three": 3}}
    assert vardict(three=3) == {"three": 3}
