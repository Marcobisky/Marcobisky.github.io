#include <pybind11/pybind11.h>

int add(int a, int b) {
    return a + b;
}

/// @param ops library name
PYBIND11_MODULE(ops, m) {
    m.def("add", &add);
}
