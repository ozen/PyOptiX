from pyoptix.objects.optix_variable import OptixVariable


class OptixScopedObject(object):
    def __init__(self):
        self._variables = dict()

    def __setitem__(self, key, value):
        # added_variable_to_optix = False
        #
        # native_variable = self._query_variable(key)
        # if native_variable == 0:
        #     native_variable = self._declare_variable(key)
        #     added_variable_to_optix = True

        native_variable = self._query_or_declare_variable(key)
        optix_variable = OptixVariable(native_variable)
        optix_variable.value = value
        self._variables[key] = optix_variable

        # try:
        #     optix_variable = OptixVariable(native_variable)
        #     optix_variable.value = value
        #     self._variables[key] = optix_variable
        # except Exception as e:
        #     if added_variable_to_optix:
        #         self._remove_variable(native_variable)
        #     raise e

    def __getitem__(self, key):
        return self._variables[key].value

    def __len__(self):
        return len(self._variables)

    def __delitem__(self, key):
        native_variable = self._query_variable(key)
        if native_variable == 0:
            raise ValueError("Variable not found")

        self._remove_variable(native_variable)
        del self._variables[key]

    def __contains__(self, item):
        return item in self._variables

    def get_scope(self):
        dict_ = {}
        for key, variable in self._variables.items():
            dict_[key] = variable.value
        return dict_
