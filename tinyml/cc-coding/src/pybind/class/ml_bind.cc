#include <pybind11/pybind11.h>

namespace ml {

class Model {
public:
    Model() = default;

    virtual double forward(double x) const {
        return x;
    }
};

class LinearModel : public Model {
public:
    LinearModel(double w = 1.0) : weight(w) {}

    double forward(double x) const override {
        return weight * x;
    }

    double weight;
};

} // namespace ml

PYBIND11_MODULE(ml_ops, m) {
    pybind11::class_<ml::Model>(m, "Model")
        .def(pybind11::init<>())
        .def("forward", &ml::Model::forward);

    pybind11::class_<ml::LinearModel, ml::Model>(m, "LinearModel")
        .def(pybind11::init<double>(), pybind11::arg("weight") = 1.0)
        .def("forward", &ml::LinearModel::forward)
        .def_readwrite("weight", &ml::LinearModel::weight);
}
