from pyoptix import OptixContext

_context_stack = [OptixContext()]


def get_context():
    return _context_stack[-1]


def push_context(ctx):
    if not isinstance(ctx, OptixContext):
        raise TypeError('context must be an instance of OptixContext')

    _context_stack.append(ctx)


def pop_context():
    return _context_stack.pop()


def create_context():
    _context_stack.append(OptixContext())
    return get_context()


def destroy_context():
    ctx = _context_stack.pop()
    ctx.destroy()
    return get_context()


class InitChildrenMixin(object):
    def __init__(self, children=None):
        if children is not None:
            if not isinstance(children, list):
                raise TypeError('children parameter must be a list')

            for child in children:
                self.add_child(child)
