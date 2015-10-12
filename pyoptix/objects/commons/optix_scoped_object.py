from pyoptix.objects.optix_variable import OptixVariable


class OptixScopedObject(object):
    def __init__(self):
        self._variables = dict()

    def __setitem__(self, key, value):
        added_variable_to_optix = False

        wrapped_variable = self._query_variable(key)
        if not wrapped_variable.is_valid():
            wrapped_variable = self._declare_variable(key)
            added_variable_to_optix = True

        try:
            optix_variable = OptixVariable(wrapped_variable)
            optix_variable.value = value
            self._variables[key] = optix_variable
        except Exception as e:
            if added_variable_to_optix:
                self._remove_variable(wrapped_variable)
            raise e

    def __getitem__(self, key):
        return self._variables[key].value

    def __len__(self):
        return len(self._variables)

    def __delitem__(self, key):
        wrapped_variable = self._query_variable(key)
        if not wrapped_variable.is_valid():
            raise ValueError("Variable not found")

        self._remove_variable(wrapped_variable)
        del self._variables[key]

    def __contains__(self, item):
        return item in self._variables

    def get_scope(self):
        dict_ = {}
        for key, variable in self._variables.items():
            dict_[key] = variable.value
        return dict_
