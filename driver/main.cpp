#include "Python.h"
#include <boost/python.hpp>
#include <boost/numpy.hpp>
#include "natives_package.h"
#include "core_package.h"
#include "enums_package.h"

BOOST_PYTHON_MODULE(_driver)
{
    Py_Initialize();
    boost::numpy::initialize();
    export_natives_package();
    export_enums_package();
    export_core_package();
}
