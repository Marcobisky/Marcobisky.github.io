#include <pybind11/pybind11.h>

namespace ml {

class Model {
public:
    Model() = default;
    virtual ~Model() = default; // 虚析构函数以确保派生类正确析构

    virtual double forward(double x) const {
        return x;
    }
};

class LinearModel : public Model {
public:
    double weight;
    LinearModel(double w = 1.0) : weight(w) {}

    double forward(double x) const override {
        return weight * x;
    }
};

} // namespace ml

PYBIND11_MODULE(ml_ops, m) {
    pybind11::class_<ml::Model>(m, "Model")     // ml::Model 映射到 Python 里的 Model
        .def(pybind11::init<>())                // 绑定类的默认构造函数
        .def("forward", &ml::Model::forward);   // 绑定类的成员函数 `forward`.

    pybind11::class_<ml::LinearModel, ml::Model>(m, "LinearModel")
        .def(pybind11::init<double>(), pybind11::arg("weight") = 1.0)
        .def("forward", &ml::LinearModel::forward) // 绑定类的成员函数 `forward`.
        .def_readwrite("weight", &ml::LinearModel::weight);
}
