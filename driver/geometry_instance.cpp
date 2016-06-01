#include "geometry_instance.h"


NativeGeometryInstanceWrapper::NativeGeometryInstanceWrapper(optix::GeometryInstance geometry_instance) {
    this->geometry_instance = geometry_instance;
    this->set_scoped_object(this->geometry_instance.get());
}

NativeGeometryInstanceWrapper::~NativeGeometryInstanceWrapper() {
    if(this->geometry_instance.get() != 0) this->geometry_instance->destroy();
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

void NativeGeometryInstanceWrapper::export_for_python() {
    boost::python::class_<NativeGeometryInstanceWrapper, boost::python::bases<NativeScopedWrapper> >(
                "NativeGeometryInstanceWrapper",
                "NativeGeometryInstanceWrapper docstring",
                boost::python::init<optix::GeometryInstance>())

            .def("_set_geometry", &NativeGeometryInstanceWrapper::set_geometry)
            .def("set_material_count", &NativeGeometryInstanceWrapper::set_material_count)
            .def("_get_material_count", &NativeGeometryInstanceWrapper::get_material_count)
            .def("_set_material", &NativeGeometryInstanceWrapper::set_material);
}
