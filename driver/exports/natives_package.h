#ifndef NATIVES_PACKAGE_H
#define NATIVES_PACKAGE_H

#include "Python.h"
#include <boost/python.hpp>

#include "optix_shared_includes.h"



void export_natives_package()
{
    namespace bp = boost::python;

    bp::object natives_module(bp::handle<>(bp::borrowed(PyImport_AddModule("PyOptixCpp.Natives"))));
    bp::scope().attr("Natives") = natives_module;
    bp::scope natives_scope = natives_module;

    using namespace optix;
    bp::class_<Acceleration>("_Acceleration", "_Acceleration docstring", bp::no_init);
    bp::class_<Buffer>("_Buffer", "_Buffer docstring", bp::no_init);
    bp::class_<Context>("_Context", "_Context docstring", bp::no_init);
    bp::class_<Geometry>("_Geometry", "_Geometry docstring", bp::no_init);
    bp::class_<GeometryGroup>("_GeometryGroup", "_GeometryGroup docstring", bp::no_init);
    bp::class_<GeometryInstance>("_GeometryInstance", "_GeometryInstance docstring", bp::no_init);
    bp::class_<Group>("_Group", "_Group docstring", bp::no_init);
    bp::class_<Material>("_Material", "_Material docstring", bp::no_init);
    bp::class_<Program>("_Program", "_Program docstring", bp::no_init);
    bp::class_<Selector>("_Selector", "_Selector docstring", bp::no_init);
    bp::class_<TextureSampler>("_TextureSampler", "_TextureSampler docstring", bp::no_init);
    bp::class_<Transform>("_Transform", "_Transform docstring", bp::no_init);
    bp::class_<Variable>("_Variable", "_Variable docstring", bp::no_init);

}





#endif
