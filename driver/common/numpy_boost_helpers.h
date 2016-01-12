#ifndef NUMPY_BOOST_HELPERS_H
#define NUMPY_BOOST_HELPERS_H

#include <boost/python.hpp>
#include <boost/numpy.hpp>

long get_array_size_in_bytes(const boost::numpy::ndarray& numpy_array);
std::vector<int> get_array_sizes_as_vector_int(const boost::numpy::ndarray& numpy_array);

#endif
