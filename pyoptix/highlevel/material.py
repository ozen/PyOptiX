import six
from pyoptix.objects import MaterialObj
from pyoptix.highlevel.shared import get_context


class Material(MaterialObj):
    def __init__(self, closest_hit=None, any_hit=None):
        context = get_context()
        native = context._create_material()
        MaterialObj.__init__(self, native=native, context=context)

        if closest_hit is None:
            closest_hit = {}
        if any_hit is None:
            any_hit = {}

        for key, value in six.iteritems(closest_hit):
            self.set_closest_hit_program(key, value)

        for key, value in six.iteritems(any_hit):
            self.set_any_hit_program(key, value)
