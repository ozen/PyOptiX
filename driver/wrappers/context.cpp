#include "context.h"


NativeContextWrapper::NativeContextWrapper(): NativeScopedWrapper() {
    this->context = optix::Context::create();
    this->set_scoped_object(this->context.get());
}

NativeContextWrapper::~NativeContextWrapper() {
    if(this->context.get() != 0) this->context->destroy();
}

optix::Variable NativeContextWrapper::get_assignable_variable(const std::string& variable_name) {
    return this->context[variable_name];
}

unsigned int NativeContextWrapper::get_ray_type_count() {
    return this->context->getRayTypeCount();
}

unsigned int NativeContextWrapper::get_entry_point_count() {
    return this->context->getEntryPointCount();
}

void NativeContextWrapper::set_ray_type_count(unsigned int ray_type_count) {
    this->context->setRayTypeCount(ray_type_count);
}

void NativeContextWrapper::set_entry_point_count(unsigned int entry_point_count) {
    this->context->setEntryPointCount(entry_point_count);
}

void NativeContextWrapper::set_ray_generation_program(unsigned int entry_point_index, NativeProgramWrapper* ray_generation_program) {
    this->context->setRayGenerationProgram(entry_point_index, ray_generation_program->get_native());
}

void NativeContextWrapper::set_exception_program(unsigned int entry_point_index, NativeProgramWrapper* exception_program) {
    this->context->setExceptionProgram(entry_point_index, exception_program->get_native());
}

void NativeContextWrapper::set_miss_program(unsigned int ray_type_index, NativeProgramWrapper* miss_program) {
    this->context->setMissProgram(ray_type_index, miss_program->get_native());
}

void NativeContextWrapper::compile() {
    this->context->compile();
}

void NativeContextWrapper::launch_1d(unsigned int entry_point_index, int width) {
    this->context->launch(entry_point_index, width);
}

void NativeContextWrapper::launch_2d(unsigned int entry_point_index, int width, int height) {
    this->context->launch(entry_point_index, width, height);
}

void NativeContextWrapper::launch_3d(unsigned int entry_point_index, int width, int height, int depth) {
    this->context->launch(entry_point_index, width, height, depth);
}

int NativeContextWrapper::get_cpu_num_of_threads() {
    return context->getCPUNumThreads();
}

void NativeContextWrapper::set_cpu_num_of_threads(int threadCount) {
    context->setCPUNumThreads(threadCount);
}

int NativeContextWrapper::get_stack_size() {
    return context->getStackSize();
}

void NativeContextWrapper::set_stack_size(int stack_size_bytes) {
    context->setStackSize(stack_size_bytes);
}


int NativeContextWrapper::get_available_devices_count() {
    return optix::Context::getDeviceCount();
}

std::string NativeContextWrapper::get_device_name(int device_id) {
    return context->getDeviceName(device_id);
}

boost::python::tuple NativeContextWrapper::get_device_compute_capability(int device_id) {
    int computeCapabilities[2];
    context->getDeviceAttribute(device_id, RT_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY, sizeof(computeCapabilities), computeCapabilities);
    return boost::python::make_tuple(computeCapabilities[0], computeCapabilities[1]);
}

int NativeContextWrapper::get_enabled_device_count() {
    return context->getEnabledDeviceCount();
}

std::vector<int> NativeContextWrapper::get_enabled_devices() {
    return context->getEnabledDevices();
}

void NativeContextWrapper::set_devices(std::vector<int> devices) {
    context->setDevices(devices.begin(), devices.end());
}

unsigned long NativeContextWrapper::get_used_host_memory() {
    return static_cast<unsigned long>(context->getUsedHostMemory());
}

unsigned long NativeContextWrapper::get_available_device_memory(int device_id) {
    return static_cast<unsigned long>(context->getAvailableDeviceMemory(device_id));
}

void NativeContextWrapper::set_exception_enabled(RTexception exception, bool enabled) {
    this->context->setExceptionEnabled(exception, enabled);
}

bool NativeContextWrapper::get_exception_enabled(RTexception exception) {
    return this->context->getExceptionEnabled(exception);
}

void NativeContextWrapper::set_print_enabled(bool enabled){
    this->context->setPrintEnabled(enabled);
}

bool NativeContextWrapper::get_print_enabled() {
    return this->context->getPrintEnabled();
}

void NativeContextWrapper::set_print_buffer_size(int buffer_size_bytes){
    this->context->setPrintBufferSize(buffer_size_bytes);
}

int NativeContextWrapper::get_print_buffer_size() {
    return this->context->getPrintBufferSize();
}

optix::Program NativeContextWrapper::create_program_from_file(std::string file_name, std::string program_name) {
    return this->context->createProgramFromPTXFile(file_name, program_name);
}

optix::Buffer NativeContextWrapper::create_buffer(int buffer_type) {
    return this->context->createBuffer(buffer_type);
}

optix::TextureSampler NativeContextWrapper::create_texture_sampler() {
    return this->context->createTextureSampler();
}

optix::Geometry NativeContextWrapper::create_geometry() {
    return this->context->createGeometry();
}

optix::Material NativeContextWrapper::create_material() {
    return this->context->createMaterial();
}

optix::GeometryInstance NativeContextWrapper::create_geometry_instance() {
    return this->context->createGeometryInstance();
}

optix::Group NativeContextWrapper::create_group() {
    return this->context->createGroup();
}

optix::GeometryGroup NativeContextWrapper::create_geometry_group() {
    return this->context->createGeometryGroup();
}

optix::Transform NativeContextWrapper::create_transform() {
    return this->context->createTransform();
}

optix::Selector NativeContextWrapper::create_selector() {
    return this->context->createSelector();
}

optix::Acceleration NativeContextWrapper::create_accelerator(std::string builder, std::string traverser) {
    return this->context->createAcceleration(builder.c_str(), traverser.c_str());
}

template<class T>
struct VecToList
{
    static PyObject* convert(const std::vector<T>& vec)
    {
        boost::python::list* l = new boost::python::list();
        for(size_t i = 0; i < vec.size(); i++)
            (*l).append(vec[i]);

        return l->ptr();
    }
};

void NativeContextWrapper::export_for_python() {
    boost::python::to_python_converter<std::vector<int,class std::allocator<int> >, VecToList<int> >();

    boost::python::class_<NativeContextWrapper, boost::python::bases<NativeScopedWrapper> >(
                "NativeContextWrapper",
                "NativeContextWrapper docstring",
                boost::python::init<>())

            .def("get_ray_type_count", &NativeContextWrapper::get_ray_type_count)
            .def("set_ray_type_count", &NativeContextWrapper::set_ray_type_count)
            .def("get_entry_point_count", &NativeContextWrapper::get_entry_point_count)
            .def("set_entry_point_count", &NativeContextWrapper::set_entry_point_count)
            .def("get_cpu_num_of_threads", &NativeContextWrapper::get_cpu_num_of_threads)
            .def("set_cpu_num_of_threads", &NativeContextWrapper::set_cpu_num_of_threads)
            .def("get_stack_size", &NativeContextWrapper::get_stack_size)
            .def("set_stack_size", &NativeContextWrapper::set_stack_size)
            .def("get_available_devices_count", &NativeContextWrapper::get_available_devices_count)
            .def("get_device_name", &NativeContextWrapper::get_device_name)
            .def("get_device_compute_capability", &NativeContextWrapper::get_device_compute_capability)
            .def("get_enabled_device_count", &NativeContextWrapper::get_enabled_device_count)
            .def("get_enabled_devices", &NativeContextWrapper::get_enabled_devices)
            .def("set_devices", &NativeContextWrapper::set_devices)
            .def("get_used_host_memory", &NativeContextWrapper::get_used_host_memory)
            .def("get_available_device_memory", &NativeContextWrapper::get_available_device_memory)
            .def("get_exception_enabled", &NativeContextWrapper::get_exception_enabled)
            .def("set_exception_enabled", &NativeContextWrapper::set_exception_enabled)
            .def("get_print_enabled", &NativeContextWrapper::get_print_enabled)
            .def("set_print_enabled", &NativeContextWrapper::set_print_enabled)
            .def("get_print_buffer_size", &NativeContextWrapper::get_print_buffer_size)
            .def("set_print_buffer_size", &NativeContextWrapper::set_print_buffer_size)
            .def("set_ray_generation_program", &NativeContextWrapper::set_ray_generation_program)
            .def("set_exception_program", &NativeContextWrapper::set_exception_program)
            .def("compile", &NativeContextWrapper::compile)
            .def("_create_program_from_file", &NativeContextWrapper::create_program_from_file)
            .def("_create_buffer", &NativeContextWrapper::create_buffer)
            .def("_create_texture_sampler", &NativeContextWrapper::create_texture_sampler)
            .def("_create_geometry", &NativeContextWrapper::create_geometry)
            .def("_create_material", &NativeContextWrapper::create_material)
            .def("_create_geometry_instance", &NativeContextWrapper::create_geometry_instance)
            .def("_create_group", &NativeContextWrapper::create_group)
            .def("_create_geometry_group", &NativeContextWrapper::create_geometry_group)
            .def("_create_transform", &NativeContextWrapper::create_transform)
            .def("_create_selector", &NativeContextWrapper::create_selector)
            .def("_create_accelerator", &NativeContextWrapper::create_accelerator)
            .def("_set_miss_program", &NativeContextWrapper::set_miss_program)
            .def("_launch_1d", &NativeContextWrapper::launch_1d)
            .def("_launch_2d", &NativeContextWrapper::launch_2d)
            .def("_launch_3d", &NativeContextWrapper::launch_3d);
}
