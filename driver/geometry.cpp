#include "geometry.h"


NativeGeometryWrapper::NativeGeometryWrapper(optix::Geometry geometry) {
    this->geometry = geometry;
    this->set_scoped_object(this->geometry.get());
}

NativeGeometryWrapper::~NativeGeometryWrapper() {
    if (!is_destroyed) {
        this->geometry->destroy();
        is_destroyed = true;
    }
}

void NativeGeometryWrapper::mark_dirty() {
    this->geometry->markDirty();
}

bool NativeGeometryWrapper::is_dirty() {
    return this->geometry->isDirty();
}

void NativeGeometryWrapper::set_primitive_count(unsigned int num_primitives) {
    this->geometry->setPrimitiveCount(num_primitives);
}

unsigned int NativeGeometryWrapper::get_primitive_count() {
    return this->geometry->getPrimitiveCount();
}

void NativeGeometryWrapper::set_primitive_index_offset(unsigned int index_offset) {
    this->geometry->setPrimitiveIndexOffset(index_offset);
}

unsigned int NativeGeometryWrapper::get_primitive_index_offset() {
    return this->geometry->getPrimitiveIndexOffset();
}

void NativeGeometryWrapper::set_bounding_box_program(NativeProgramWrapper* program) {
    this->geometry->setBoundingBoxProgram(program->get_native());
}

void NativeGeometryWrapper::set_intersection_program(NativeProgramWrapper* program) {
    this->geometry->setIntersectionProgram(program->get_native());
}

optix::Geometry NativeGeometryWrapper::get_native() {
    return this->geometry;
}

void NativeGeometryWrapper::boost_python_expose() {
    boost::python::class_<NativeGeometryWrapper, boost::python::bases<NativeScopedWrapper> >(
                "NativeGeometryWrapper",
                "Wraps optix::Geometry class",
                boost::python::no_init)

            .def("mark_dirty", &NativeGeometryWrapper::mark_dirty)
            .def("is_dirty", &NativeGeometryWrapper::is_dirty)
            .def("set_primitive_count", &NativeGeometryWrapper::set_primitive_count)
            .def("get_primitive_count", &NativeGeometryWrapper::get_primitive_count)
            .def("set_primitive_index_offset", &NativeGeometryWrapper::set_primitive_index_offset)
            .def("get_primitive_index_offset", &NativeGeometryWrapper::get_primitive_index_offset)
            .def("set_bounding_box_program", &NativeGeometryWrapper::set_bounding_box_program)
            .def("set_intersection_program", &NativeGeometryWrapper::set_intersection_program);
}
