from pyoptix.mixins.destroyable import DestroyableObject


class ScopedObject(DestroyableObject):
    def __init__(self, native):
        DestroyableObject.__init__(self, native)
        self._variables = {}

    def __setitem__(self, key, value):
        from pyoptix.variable import Variable

        variable_wrapper = self._safe_native.query_variable(key)
        declared = False

        if variable_wrapper is None:
            variable_wrapper = self._safe_native.declare_variable(key)
            declared = True

        try:
            optix_variable = Variable(variable_wrapper)
            optix_variable.value = value
            self._variables[key] = optix_variable
        except Exception as e:
            if declared:
                self._safe_native.remove_variable(variable_wrapper)
            raise e

    def __getitem__(self, key):
        return self._variables[key].value

    def __len__(self):
        return len(self._variables)

    def __delitem__(self, key):
        wrapped_variable = self._safe_native.query_variable(key)
        if not wrapped_variable.is_valid():
            raise ValueError("Variable not found")

        self._safe_native.remove_variable(wrapped_variable)
        del self._variables[key]

    def __contains__(self, item):
        return item in self._variables
