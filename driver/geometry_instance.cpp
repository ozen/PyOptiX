#include "geometry_instance.h"


NativeGeometryInstanceWrapper::NativeGeometryInstanceWrapper(optix::GeometryInstance geometry_instance) {
    this->geometry_instance = geometry_instance;
    this->set_scoped_object(this->geometry_instance.get());
}

NativeGeometryInstanceWrapper::~NativeGeometryInstanceWrapper() {
    if (!is_destroyed) this->geometry_instance->destroy();
}

void NativeGeometryInstanceWrapper::set_geometry(NativeGeometryWrapper* geometry) {
    return this->geometry_instance->setGeometry(geometry->get_native());
}

void NativeGeometryInstanceWrapper::set_material_count(unsigned int count) {
    return this->geometry_instance->setMaterialCount(count);
}

unsigned int NativeGeometryInstanceWrapper::get_material_count() {
    return this->geometry_instance->getMaterialCount();
}

void NativeGeometryInstanceWrapper::set_material(unsigned int idx, NativeMaterialWrapper* material) {
    this->geometry_instance->setMaterial(idx, material->get_native());
}

optix::GeometryInstance NativeGeometryInstanceWrapper::get_native() {
    return geometry_instance;
}

void NativeGeometryInstanceWrapper::boost_python_expose() {
    boost::python::class_<NativeGeometryInstanceWrapper, boost::python::bases<NativeScopedWrapper> >(
                "NativeGeometryInstanceWrapper",
                "Wraps optix::GeometryInstance class",
                boost::python::no_init)

            .def("set_geometry", &NativeGeometryInstanceWrapper::set_geometry)
            .def("set_material_count", &NativeGeometryInstanceWrapper::set_material_count)
            .def("get_material_count", &NativeGeometryInstanceWrapper::get_material_count)
            .def("set_material", &NativeGeometryInstanceWrapper::set_material);
}
