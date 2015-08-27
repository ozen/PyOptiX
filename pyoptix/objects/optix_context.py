from pyoptix._driver import _OptixContextWrapper
from pyoptix._driver import RTbuffertype
from pyoptix.objects.commons.optix_scoped_object import OptixScopedObject


class OptixContext(_OptixContextWrapper, OptixScopedObject):
    _ray_generators = None

    def __init__(self):
        _OptixContextWrapper.__init__(self)
        OptixScopedObject.__init__(self)
        self._ray_generators = []

    def launch(self, ray_generator, width, height):
        index = self._ray_generators.index(ray_generator)
        self._launch_2d(index, width, height)

    def set_ray_type_count(self, ray_type_count):
        self._set_ray_type_count(ray_type_count)

    def add_ray_generator(self, ray_generator):
        from pyoptix.objects.optix_program import OptixProgram
        if not isinstance(ray_generator, OptixProgram):
            raise ValueError("Ray generator must be Optix Program not" + str(type(ray_generator)))

        self._ray_generators.append(ray_generator)
        self._sync_ray_generators()

    def remove_ray_generator(self, ray_generator):
        self._ray_generators.remove(ray_generator)
        self._sync_ray_generators()

    def _sync_ray_generators(self):
        total_ray_generation_count = len(self._ray_generators)
        self._set_entry_point_count(total_ray_generation_count)

        for i in range(total_ray_generation_count):
            self._set_ray_generation_program(i, self._ray_generators[i])

    def create_program_from_file(self, file_name, function_name):
        """
        :rtype : OptixProgram
        """
        # Compile it
        from pyoptix.compiler.optix_compiler import OptixCompiler
        compiler = OptixCompiler()
        compiled_file_path = compiler.compile(file_name)

        # Create program from compiled files
        from pyoptix.objects.optix_program import OptixProgram
        native = self._create_program_from_file(compiled_file_path, function_name)
        return OptixProgram(native, context=self)

    def create_buffer(self, buffer_type:RTbuffertype):
        """
        :param buffer_type:RTbuffertype
        :rtype : OptixBuffer
        """
        buffer_type_enum = None
        if buffer_type == 'i':
            buffer_type_enum = RTbuffertype.RT_BUFFER_INPUT
        elif buffer_type == 'o':
            buffer_type_enum = RTbuffertype.RT_BUFFER_OUTPUT
        elif buffer_type == 'io':
            buffer_type_enum = RTbuffertype.RT_BUFFER_INPUT_OUTPUT
        if buffer_type_enum is None:
            raise ValueError("Buffer type must be 'i' 'o' or 'io'")

        from pyoptix.objects.optix_buffer import OptixBuffer
        native = self._create_buffer(buffer_type_enum)
        return OptixBuffer(native, context=self)

    def create_texture_sampler(self):
        """
        :rtype : OptixTexture
        """
        from pyoptix.objects.optix_texture import OptixTexture
        native = self._create_texture_sampler()
        return OptixTexture(native, context=self)

    def create_geometry(self):
        """
        :rtype : OptixGeometry
        """
        from pyoptix.objects.optix_geometry import OptixGeometry
        native = self._create_geometry()
        return OptixGeometry(native, context=self)

    def create_material(self):
        """
        :rtype : OptixMaterial
        """
        from pyoptix.objects.optix_material import OptixMaterial
        native = self._create_material()
        return OptixMaterial(native, context=self)

    def create_geometry_instance(self):
        """
        :rtype : OptixGeometryInstance
        """
        from pyoptix.objects.optix_geometry_instance import OptixGeometryInstance
        native = self._create_geometry_instance()
        return OptixGeometryInstance(native, context=self)

    def create_group(self):
        """
        :rtype : OptixGroup
        """
        from pyoptix.objects.optix_group import OptixGroup
        native = self._create_group()
        return OptixGroup(native, context=self)

    def create_geometry_group(self):
        """
        :rtype : OptixGeometryGroup
        """
        from pyoptix.objects.optix_geometry_group import OptixGeometryGroup
        native = self._create_geometry_group()
        return OptixGeometryGroup(native, context=self)

    def create_transform(self):
        """
        :rtype : OptixTransform
        """
        from pyoptix.objects.optix_transform import OptixTransform
        native = self._create_transform()
        return OptixTransform(native, context=self)

    def create_selector(self):
        """
        :rtype : OptixSelector
        """
        from pyoptix.objects.optix_selector import OptixSelector
        native = self._create_selector()
        return OptixSelector(native, context=self)

    def create_acceleration(self, builder, traverser):
        """
        :rtype : OptixAcceleration
        """
        from pyoptix.objects.optix_acceleration import OptixAcceleration
        native = self._create_accelerator(builder, traverser)
        return OptixAcceleration(native, context=self)

    def create_buffer_from_numpy_array(self, buffer_type, numpy_array):
        buffer = self.create_buffer(buffer_type)
        buffer.restructure_and_copy_from_numpy_array(numpy_array)
        return buffer

    def create_buffer_empty_like(self, buffer_type, numpy_array):
        buffer = self.create_buffer(buffer_type)
        buffer.restructure_according_to_numpy_array(numpy_array)
        return buffer

