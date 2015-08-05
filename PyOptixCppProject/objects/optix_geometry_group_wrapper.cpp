#include "optix_geometry_group_wrapper.h"



OptixGeometryGroupWrapper::OptixGeometryGroupWrapper(optix::GeometryGroup geometry_group)
{
    this->geometry_group = geometry_group;
    this->set_destroyable_object(this->geometry_group.get());
}

OptixGeometryGroupWrapper::~OptixGeometryGroupWrapper()
{
    std::cout<<"~OptixGeometryGroupWrapper deconstruction"<<std::endl;
    if(this->geometry_group.get() != 0)
        this->geometry_group->destroy();
}

void OptixGeometryGroupWrapper::set_acceleration(OptixAccelerationWrapper* acceleration)
{
    this->geometry_group->setAcceleration(acceleration->get_native());
}


void OptixGeometryGroupWrapper::set_child_count(unsigned int count)
{
    this->geometry_group->setChildCount(count);
}

unsigned int OptixGeometryGroupWrapper::get_child_count()
{
    return this->geometry_group->getChildCount();
}

void OptixGeometryGroupWrapper::set_child_geometry_group_instance(unsigned int index, OptixGeometryInstanceWrapper* geometryinstance)
{
    this->geometry_group->setChild(index, geometryinstance->get_native());
}

void OptixGeometryGroupWrapper::remove_child(unsigned int index)
{
    this->geometry_group->removeChild(index);
}

optix::GeometryGroup OptixGeometryGroupWrapper::get_native()
{
    return this->geometry_group;
}

#include "Python.h"
#include <boost/python.hpp>
void OptixGeometryGroupWrapper::export_for_python()
{
    namespace bp = boost::python;

    bp::class_<OptixGeometryGroupWrapper, bp::bases<OptixDestroyableObject> >(
                "_OptixGeometryGroupWrapper",
                "_OptixGeometryGroupWrapper docstring",
                bp::init<optix::GeometryGroup>())

            //*****************
            // DIRECT ACCESS
            //*****************
            .def("_set_acceleration", &OptixGeometryGroupWrapper::set_acceleration)

            .def("_set_child_count", &OptixGeometryGroupWrapper::set_child_count)
            .def("get_child_count", &OptixGeometryGroupWrapper::get_child_count)
            .def("_set_child_geometry_group_instance", &OptixGeometryGroupWrapper::set_child_geometry_group_instance)
            .def("_remove_child", &OptixGeometryGroupWrapper::remove_child);

}



