#include "variable.h"
#include "buffer.h"
#include "texture_sampler.h"
#include "group.h"
#include "geometry_group.h"
#include "transform.h"
#include "selector.h"
#include "program.h"


NativeVariableWrapper::NativeVariableWrapper(optix::Variable variable) {
    this->variable = variable;
}

bool NativeVariableWrapper::is_valid() {
    if (this->variable == 0)
        return false;
    else
        return true;
}

std::string NativeVariableWrapper::get_name() {
    return this->variable->getName();
}

std::string NativeVariableWrapper::get_annotation() {
    return this->variable->getAnnotation();
}

RTobjecttype NativeVariableWrapper::get_type() {
    return this->variable->getType();
}

unsigned long NativeVariableWrapper::get_size_in_bytes() {
    return this->variable->getSize();
}

void NativeVariableWrapper::set_buffer(NativeBufferWrapper* buffer_wrapper) {
    this->variable->setBuffer(buffer_wrapper->get_native_buffer());
}

void NativeVariableWrapper::set_texture(NativeTextureSamplerWrapper* texture_wrapper) {
    this->variable->setTextureSampler(texture_wrapper->get_native());
}

void NativeVariableWrapper::set_group(NativeGroupWrapper* group_wrapper) {
    this->variable->set(group_wrapper->get_native());
}

void NativeVariableWrapper::set_geometry_group(NativeGeometryGroupWrapper* geometry_group_wrapper) {
    this->variable->set(geometry_group_wrapper->get_native());
}

void NativeVariableWrapper::set_transform(NativeTransformWrapper* transform_wrapper) {
    this->variable->set(transform_wrapper->get_native());
}

void NativeVariableWrapper::set_selector(NativeSelectorWrapper* selector_wrapper) {
    this->variable->set(selector_wrapper->get_native());
}

void NativeVariableWrapper::set_program_id_with_program(NativeProgramWrapper* program_wrapper) {
    this->variable->setProgramId(program_wrapper->get_native());
}

void NativeVariableWrapper::set_from_array(PyObject* array, RTobjecttype object_type) {
    Py_buffer pb;
    PyObject_GetBuffer(array, &pb, PyBUF_SIMPLE);

    switch(object_type)
    {
    case RT_OBJECTTYPE_FLOAT:
        this->variable->setFloat(((float*)pb.buf)[0]);
        break;
    case RT_OBJECTTYPE_FLOAT2:
        this->variable->setFloat(((optix::float2*)pb.buf)[0]);
        break;
    case RT_OBJECTTYPE_FLOAT3:
        this->variable->setFloat(((optix::float3*)pb.buf)[0]);
        break;
    case RT_OBJECTTYPE_FLOAT4:
        this->variable->setFloat(((optix::float4*)pb.buf)[0]);
        break;
    case RT_OBJECTTYPE_INT:
        this->variable->setInt(((int*)pb.buf)[0]);
        break;
    case RT_OBJECTTYPE_INT2:
        this->variable->setInt(((optix::int2*)pb.buf)[0]);
        break;
    case RT_OBJECTTYPE_INT3:
        this->variable->setInt(((optix::int3*)pb.buf)[0]);
        break;
    case RT_OBJECTTYPE_INT4:
        this->variable->setInt(((optix::int4*)pb.buf)[0]);
        break;
    case RT_OBJECTTYPE_UNSIGNED_INT:
        this->variable->setUint(((unsigned int*)pb.buf)[0]);
        break;
    case RT_OBJECTTYPE_UNSIGNED_INT2:
        this->variable->setUint(((optix::uint2*)pb.buf)[0]);
        break;
    case RT_OBJECTTYPE_UNSIGNED_INT3:
        this->variable->setUint(((optix::uint3*)pb.buf)[0]);
        break;
    case RT_OBJECTTYPE_UNSIGNED_INT4:
        this->variable->setUint(((optix::uint4*)pb.buf)[0]);
        break;
    case RT_OBJECTTYPE_MATRIX_FLOAT2x2:
        this->variable->setMatrix2x2fv(false, (float*) pb.buf);
        break;
    case RT_OBJECTTYPE_MATRIX_FLOAT2x3:
        this->variable->setMatrix2x3fv(false, (float*) pb.buf);
        break;
    case RT_OBJECTTYPE_MATRIX_FLOAT2x4:
        this->variable->setMatrix2x4fv(false, (float*) pb.buf);
        break;
    case RT_OBJECTTYPE_MATRIX_FLOAT3x2:
        this->variable->setMatrix3x2fv(false, (float*) pb.buf);
        break;
    case RT_OBJECTTYPE_MATRIX_FLOAT3x3:
        this->variable->setMatrix3x3fv(false, (float*) pb.buf);
        break;
    case RT_OBJECTTYPE_MATRIX_FLOAT3x4:
        this->variable->setMatrix3x4fv(false, (float*) pb.buf);
        break;
    case RT_OBJECTTYPE_MATRIX_FLOAT4x2:
        this->variable->setMatrix4x2fv(false, (float*) pb.buf);
        break;
    case RT_OBJECTTYPE_MATRIX_FLOAT4x3:
        this->variable->setMatrix4x3fv(false, (float*) pb.buf);
        break;
    case RT_OBJECTTYPE_MATRIX_FLOAT4x4:
        this->variable->setMatrix4x4fv(false, (float*) pb.buf);
        break;
    case RT_OBJECTTYPE_USER:
        this->variable->setUserData(pb.len, pb.buf);
        break;
    default:
        PyErr_SetString(PyExc_RuntimeError, "Cannot assign variable");
        boost::python::throw_error_already_set();
    };

    PyBuffer_Release(&pb);
}

optix::Variable NativeVariableWrapper::get_native() {
    return variable;
}

void NativeVariableWrapper::export_for_python() {
    boost::python::class_<NativeVariableWrapper>(
                "NativeVariableWrapper",
                "NativeVariableWrapper docstring",
                 boost::python::init<optix::Variable>())

            .add_property("name", &NativeVariableWrapper::get_name)
            .add_property("annotation", &NativeVariableWrapper::get_annotation)
            .add_property("type", &NativeVariableWrapper::get_type)
            .add_property("nbytes", &NativeVariableWrapper::get_size_in_bytes)
            .add_property("_native", &NativeVariableWrapper::get_native)
            .def("is_valid", &NativeVariableWrapper::is_valid)
            .def("_set_buffer", &NativeVariableWrapper::set_buffer)
            .def("_set_texture", &NativeVariableWrapper::set_texture)
            .def("_set_program_id_with_program", &NativeVariableWrapper::set_program_id_with_program)
            .def("_set_group", &NativeVariableWrapper::set_group)
            .def("_set_geometry_group", &NativeVariableWrapper::set_geometry_group)
            .def("_set_transform", &NativeVariableWrapper::set_transform)
            .def("_set_selector", &NativeVariableWrapper::set_selector)
            .def("_set_from_array", &NativeVariableWrapper::set_from_array);
}
