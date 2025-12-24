import inspect
import executing
import types
import sys

__version__ = "1.0.2"

class vardict(dict):
    def __new__(cls, *args, _via_module=False, **kwargs):
        if len(args) == 0:
            dict(kwargs)
        call_frame = inspect.currentframe().f_back
        if _via_module:
            call_frame = call_frame.f_back
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

class _vardictModule(types.ModuleType):
    def __call__(self, *args, **kwargs):
        return vardict(*args, **kwargs, _via_module=True)

    def __setattr__(self, item, value):
        setattr(vardict, item, value)

    def __getattr__(self, item):
        return getattr(vardict, item)

if __name__ != "__main__":
    sys.modules["vardict"].__class__ = _vardictModule