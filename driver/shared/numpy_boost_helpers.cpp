#include "numpy_boost_helpers.h"


long get_array_size_in_bytes(const boost::numpy::ndarray& numpy_array)
{
    int dim = numpy_array.get_nd();
    long total_count_of_elements = static_cast<long>(numpy_array.shape(0));

    for(int i = 1; i < dim; i++)
        total_count_of_elements *= static_cast<long>(numpy_array.shape(i));

    int item_size = numpy_array.get_dtype().get_itemsize();

    return item_size * total_count_of_elements;
}

std::vector<int> get_array_sizes_as_vector_int(const boost::numpy::ndarray& numpy_array)
{
    int dim = numpy_array.get_nd();
    std::vector<int> sizes_vector = std::vector<int>();

    for(int i = 0; i < dim; i++)
        sizes_vector.push_back(static_cast<int>(numpy_array.shape(i)));

    return sizes_vector;
}

