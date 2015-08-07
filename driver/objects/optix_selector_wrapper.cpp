#include "optix_selector_wrapper.h"

OptixSelectorWrapper::OptixSelectorWrapper(optix::Selector selector)
{
    this->selector = selector;
    this->set_destroyable_object(this->selector.get());
}

OptixSelectorWrapper::~OptixSelectorWrapper()
{
    std::cout<<"~OptixSelectorWrapper deconstruction"<<std::endl;

    if(this->selector.get() != 0)
        this->selector->destroy();
}

void OptixSelectorWrapper::set_visit_program(OptixProgramWrapper*  program)
{
    this->selector->setVisitProgram(program->get_native_program());
}

void OptixSelectorWrapper::set_child_count(unsigned int count)
{
    this->selector->setChildCount(count);
}
unsigned int OptixSelectorWrapper::get_child_count()
{
    return this->selector->getChildCount();
}

void OptixSelectorWrapper::set_child_geometry_group(unsigned int index, OptixGeometryGroupWrapper* child)
{
    this->selector->setChild(index, child->get_native());
}

void OptixSelectorWrapper::set_child_group(unsigned int index, OptixGroupWrapper* child)
{
    this->selector->setChild(index, child->get_native());
}

void OptixSelectorWrapper::set_child_selector(unsigned int index, OptixSelectorWrapper* child)
{
    this->selector->setChild(index, child->get_native());
}

void OptixSelectorWrapper::set_child_transform(unsigned int index, OptixTransformWrapper* child)
{
    this->selector->setChild(index, child->get_native());
}


//void set_child_transform(unsigned int index, OptixGeometryGroupWrapper* child);

void OptixSelectorWrapper::remove_child(unsigned int index)
{
    this->selector->removeChild(index);
}


optix::Selector OptixSelectorWrapper::get_native()
{
    return this->selector;
}


#include "Python.h"
#include <boost/python.hpp>
void OptixSelectorWrapper::export_for_python()
{
    namespace bp = boost::python;

    bp::class_<OptixSelectorWrapper, bp::bases<OptixDestroyableObject> >(
                "_OptixSelectorWrapper",
                "_OptixSelectorWrapper docstring",
                bp::init<optix::Selector>())
            //*****************
            // DIRECT ACCESS
            //*****************
            .def("_set_visit_program", &OptixSelectorWrapper::set_visit_program)
            .def("_set_child_count", &OptixSelectorWrapper::set_child_count)
            .def("get_child_count", &OptixSelectorWrapper::get_child_count)
            .def("_set_child_geometry_group", &OptixSelectorWrapper::set_child_geometry_group)
            .def("_set_child_group", &OptixSelectorWrapper::set_child_group)
            .def("_set_child_selector", &OptixSelectorWrapper::set_child_selector)
            .def("_remove_child", &OptixSelectorWrapper::remove_child);
}

