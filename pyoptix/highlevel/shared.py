from pyoptix import OptixContext

context = OptixContext()


def use_context(ctx):
    if not isinstance(ctx, OptixContext):
        raise TypeError('context must be an instance of OptixContext')
    global context
    context = ctx


class InitChildrenMixin(object):
    def __init__(self, children=None):
        if children is not None:
            if not isinstance(children, list):
                raise TypeError('children parameter must be a list')

            for child in children:
                self.add_child(child)
