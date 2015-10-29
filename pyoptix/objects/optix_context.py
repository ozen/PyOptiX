from pyoptix._driver import _OptixContextWrapper, RTbuffertype, RTfiltermode, RTformat
from pyoptix.objects.commons.optix_scoped_object import OptixScopedObject
from pyoptix.compiler import OptixCompiler
from pyoptix.objects.optix_program import OptixProgram
from pyoptix.objects.optix_acceleration import OptixAcceleration
from pyoptix.objects.optix_selector import OptixSelector
from pyoptix.objects.optix_transform import OptixTransform
from pyoptix.objects.optix_geometry_group import OptixGeometryGroup
from pyoptix.objects.optix_group import OptixGroup
from pyoptix.objects.optix_geometry_instance import OptixGeometryInstance
from pyoptix.objects.optix_material import OptixMaterial
from pyoptix.objects.optix_geometry import OptixGeometry
from pyoptix.objects.optix_texture_sampler import OptixTextureSampler
from pyoptix.objects.optix_buffer import OptixBuffer

import numpy


class OptixContext(_OptixContextWrapper, OptixScopedObject):

    def __init__(self):
        _OptixContextWrapper.__init__(self)
        OptixScopedObject.__init__(self)
        self.compiler = None
        self._miss_programs = {}

    def init_compiler(self, output_path=None, include_paths=None, arch=None, use_fast_math=None):
        kwargs = {}

        if output_path:
            kwargs['output_path'] = output_path

        if include_paths:
            kwargs['include_paths'] = include_paths

        if use_fast_math:
            kwargs['use_fast_math'] = use_fast_math

        if arch:
            kwargs['arch'] = arch
        else:
            sm_major, sm_minor = self.get_device_compute_capability(0)
            kwargs['arch'] = "sm_%s%s" % (sm_major, sm_minor)

        self.compiler = OptixCompiler(**kwargs)

    def create_acceleration(self, builder, traverser):
        """
        :rtype : OptixAcceleration
        """
        native = self._create_accelerator(builder, traverser)
        return OptixAcceleration(native, self, builder, traverser)

    def create_buffer(self, buffer_type):
        """
        :param buffer_type
        :rtype : OptixBuffer
        """
        native_buffer_type = None
        if buffer_type == 'i':
            native_buffer_type = RTbuffertype.RT_BUFFER_INPUT
        elif buffer_type == 'o':
            native_buffer_type = RTbuffertype.RT_BUFFER_OUTPUT
        elif buffer_type == 'io':
            native_buffer_type = RTbuffertype.RT_BUFFER_INPUT_OUTPUT
        if native_buffer_type is None:
            raise ValueError("Buffer type must be 'i' 'o' or 'io'")

        native = self._create_buffer(native_buffer_type)
        return OptixBuffer(native, context=self)

    def create_buffer_from_numpy_array(self, buffer_type, numpy_array, drop_last_dim=False):
        buffer = self.create_buffer(buffer_type)
        buffer.restructure_and_copy_from_numpy_array(numpy_array, drop_last_dim)
        return buffer

    def create_empty_buffer(self, buffer_type, numpy_shape, dtype=numpy.float32, drop_last_dim=False):
        buffer = self.create_buffer(buffer_type)
        buffer.reset_buffer(numpy_shape, dtype, drop_last_dim)
        return buffer

    def create_zeros_buffer(self, buffer_type, numpy_shape, dtype=numpy.float32, drop_last_dim=False):
        buffer = self.create_buffer(buffer_type)
        temp_numpy_array = numpy.zeros(numpy_shape, dtype=dtype)
        buffer.restructure_and_copy_from_numpy_array(temp_numpy_array, drop_last_dim)
        return buffer

    def create_texture_sampler(self, buffer=None, array_size=1, wrap_mode=None, indexing_mode=None, read_mode=None,
                               filter_mode=None):
        """
        :rtype : OptixTextureSampler
        """
        native = self._create_texture_sampler()
        instance = OptixTextureSampler(native, context=self)

        if indexing_mode is not None:
            instance.set_indexing_mode(indexing_mode)

        if wrap_mode is not None:
            instance.set_wrap_mode(0, wrap_mode)
            instance.set_wrap_mode(1, wrap_mode)
            instance.set_wrap_mode(2, wrap_mode)

        if read_mode is not None:
            instance.set_read_mode(read_mode)

        if filter_mode is not None:
            instance.set_filtering_modes(filter_mode, filter_mode, RTfiltermode.RT_FILTER_NONE)

        instance.set_max_anisotropy(1.0)
        instance.set_mip_level_count(1)
        instance.set_array_size(array_size)

        if buffer is not None:
            if buffer.get_format() == RTformat.RT_FORMAT_USER:
                raise TypeError("Texture sampler cannot be associated with a user-typed buffer")
            instance.set_buffer(0, 0, buffer)

        return instance

    def create_geometry(self):
        """
        :rtype : OptixGeometry
        """
        native = self._create_geometry()
        return OptixGeometry(native, context=self)

    def create_material(self):
        """
        :rtype : OptixMaterial
        """
        native = self._create_material()
        return OptixMaterial(native, context=self)

    def create_geometry_instance(self):
        """
        :rtype : OptixGeometryInstance
        """
        native = self._create_geometry_instance()
        return OptixGeometryInstance(native, context=self)

    def create_group(self):
        """
        :rtype : OptixGroup
        """
        native = self._create_group()
        return OptixGroup(native, context=self)

    def create_geometry_group(self):
        """
        :rtype : OptixGeometryGroup
        """
        native = self._create_geometry_group()
        return OptixGeometryGroup(native, context=self)

    def create_transform(self):
        """
        :rtype : OptixTransform
        """
        native = self._create_transform()
        return OptixTransform(native, context=self)

    def create_selector(self):
        """
        :rtype : OptixSelector
        """
        native = self._create_selector()
        return OptixSelector(native, context=self)

    def create_program_from_file(self, file_path, function_name, ptx_name=None):
        """
        :rtype : OptixProgram
        """
        if not self.compiler:
            self.init_compiler()

        # Compile program
        compiled_file_path = self.compiler.compile(file_path, ptx_name)

        # Create program object from compiled file
        native = self._create_program_from_file(compiled_file_path, function_name)
        return OptixProgram(native, context=self, file_path=file_path, function_name=function_name)

    def launch(self, entry_point_index, width, height=None, depth=None):
        if not height:
            self._launch_1d(entry_point_index, width)
        elif not depth:
            self._launch_2d(entry_point_index, width, height)
        else:
            self._launch_3d(entry_point_index, width, height, depth)

    def set_miss_program(self, ray_type_index, program):
        self._miss_programs[ray_type_index] = program
        self._set_miss_program(ray_type_index, program)

    def get_miss_program(self, ray_type_index):
        return self._miss_programs[ray_type_index]
