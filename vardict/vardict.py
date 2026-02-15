import inspect
import executing
import types
import sys

__version__ = "1.0.4"


def vardict(*args, **kwargs):
    if len(args) == 0:
        return dict(kwargs)

    frame = inspect.currentframe()
    vardict_filename=frame.f_code.co_filename
    while frame is not None and frame.f_code.co_filename==vardict_filename:
        frame=frame.f_back

    # call_frame = inspect.currentframe()
    # while call_frame.f_code.co_filename== call_frame.f_back.f_code.co_filename:
    #     call_frame=call_frame.f_back
    # call_frame=call_frame.f_back        
#    if _via:
#        call_frame = call_frame.f_back
#    peek(inspect.currentframe().f_code.co_filename)
#    call_frame = inspect.currentframe().f_back
#    peek(call_frame.f_code.co_filename, call_frame.f_back.f_code.co_filename,__file__)
#    if _via:
#        call_frame = call_frame.f_back
    call_node = executing.Source.executing(frame).node
    if call_node is None:
        raise ValueError("could not determine variables")
    source = executing.Source.for_frame(frame)
    result = {}
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
        return vardict(*args, **kwargs)


if __name__ != "__main__":
    sys.modules["vardict"].__class__ = _vardictModule

