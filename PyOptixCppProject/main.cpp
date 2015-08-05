#include "Python.h"
#include <iostream>




int test_sum(int a, int b)
{
    return a + b;
}

int test_sum_2(int a, int b)
{
    return a + b;
}


#include <boost/python.hpp>
#include <boost/numpy.hpp>

int test_numpy_support(const boost::numpy::ndarray& numpy_array)
{
    using namespace std;
    cout<<"Dim : " << numpy_array.get_nd()<<endl;
    cout<<"Shape0 : " <<numpy_array.shape(0)<<endl;
    cout<<"Shape1 : " <<numpy_array.shape(1)<<endl;
    cout<<"Item size : " <<numpy_array.get_dtype().get_itemsize()<<endl;

    int first_element = reinterpret_cast<int*>(numpy_array.get_data())[0];
    return first_element;
}

#include "natives_package.h"
#include "core_package.h"
#include "enums_package.h"

BOOST_PYTHON_MODULE(PyOptixCpp)
{
     /* Initialize the Numpy support */
    Py_Initialize();
    boost::numpy::initialize();

    namespace bp = boost::python;

    bp::def("test_sum", test_sum);
    bp::def("test_sum_2", test_sum_2);
    bp::def("test_numpy_support", test_numpy_support);

    export_natives_package();
    export_enums_package();
    export_core_package();
}


