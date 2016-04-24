import numpy
from pyoptix._driver import NativeContextWrapper, OPTIX_VERSION, RTbuffertype, RTfiltermode, RTformat, RTexception
from pyoptix.objects.shared.optix_scoped_object import OptixScopedObject
from pyoptix.compiler import OptixCompiler
from pyoptix.objects.program import ProgramObj
from pyoptix.objects.acceleration import AccelerationObj
from pyoptix.objects.selector import SelectorObj
from pyoptix.objects.transform import TransformObj
from pyoptix.objects.geometry_group import GeometryGroupObj
from pyoptix.objects.group import GroupObj
from pyoptix.objects.geometry_instance import GeometryInstanceObj
from pyoptix.objects.material import MaterialObj
from pyoptix.objects.geometry import GeometryObj
from pyoptix.objects.texture_sampler import TextureSamplerObj
from pyoptix.objects.buffer import BufferObj
from pyoptix.types import convert_buffer_type


class OptixContext(NativeContextWrapper, OptixScopedObject):
    def __init__(self):
        NativeContextWrapper.__init__(self)
        OptixScopedObject.__init__(self)
        self._compiler = None
        self._miss_programs = {}

    @property
    def compiler(self):
        if self._compiler is None:
            self.init_compiler()
        return self._compiler

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
            kwargs['arch'] = "sm_{0}{1}".format(sm_major, sm_minor)

        self._compiler = OptixCompiler(**kwargs)

    def create_acceleration(self, builder, traverser):
        """
        :rtype : AccelerationObj
        """
        native = self._create_accelerator(builder, traverser)
        return AccelerationObj(native, self, builder, traverser)

    def create_buffer(self, buffer_type):
        """
        :param buffer_type
        :rtype : BufferObj
        """
        native = self._create_buffer(convert_buffer_type(buffer_type))
        return BufferObj(native, context=self)

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

    def create_texture_sampler(self, buffer, wrap_mode=None, indexing_mode=None,
                               read_mode=None, filter_mode=None, max_anisotropy=1):
        """
        :rtype : TextureSamplerObj
        """
        if buffer.get_format() == RTformat.RT_FORMAT_USER:
            raise TypeError("Texture sampler cannot be associated with a user-typed buffer")

        native = self._create_texture_sampler()
        instance = TextureSamplerObj(native, context=self)

        if indexing_mode is not None:
            instance.set_indexing_mode(indexing_mode)

        if wrap_mode is not None:
            instance.set_wrap_mode(0, wrap_mode)
            instance.set_wrap_mode(1, wrap_mode)
            instance.set_wrap_mode(2, wrap_mode)

        if read_mode is not None:
            instance.set_read_mode(read_mode)

        if filter_mode is not None:
            if OPTIX_VERSION >= 3090 and buffer.get_mip_level_count() > 1:
                instance.set_filtering_modes(filter_mode, filter_mode, filter_mode)
            else:
                instance.set_filtering_modes(filter_mode, filter_mode, RTfiltermode.RT_FILTER_NONE)

        instance.set_max_anisotropy(max_anisotropy)

        if OPTIX_VERSION < 3090:
            # required with OptiX < 3.9.0
            instance.set_mip_level_count(1)
            instance.set_array_size(1)

        instance.set_buffer(0, 0, buffer)

        return instance

    def create_geometry(self):
        """
        :rtype : GeometryObj
        """
        native = self._create_geometry()
        return GeometryObj(native, context=self)

    def create_material(self):
        """
        :rtype : MaterialObj
        """
        native = self._create_material()
        return MaterialObj(native, context=self)

    def create_geometry_instance(self):
        """
        :rtype : GeometryInstanceObj
        """
        native = self._create_geometry_instance()
        return GeometryInstanceObj(native, context=self)

    def create_group(self):
        """
        :rtype : GroupObj
        """
        native = self._create_group()
        return GroupObj(native, context=self)

    def create_geometry_group(self):
        """
        :rtype : GeometryGroupObj
        """
        native = self._create_geometry_group()
        return GeometryGroupObj(native, context=self)

    def create_transform(self):
        """
        :rtype : TransformObj
        """
        native = self._create_transform()
        return TransformObj(native, context=self)

    def create_selector(self):
        """
        :rtype : SelectorObj
        """
        native = self._create_selector()
        return SelectorObj(native, context=self)

    def compile_program(self, file_path, ptx_name=None):
        return self._compiler.compile(file_path, ptx_name)

    def create_program(self, file_path, function_name, ptx_name=None, compiled_file_path=None):
        if compiled_file_path is None:
            # Compile program
            compiled_file_path, is_compiled = self.compile_program(file_path, ptx_name)

        # Create program object from compiled file
        native = self._create_program_from_file(compiled_file_path, function_name)
        return ProgramObj(native, context=self, file_path=file_path, function_name=function_name)

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

    def set_all_exceptions_enabled(self, is_enabled):
        self.set_exception_enabled(RTexception.RT_EXCEPTION_ALL, is_enabled)