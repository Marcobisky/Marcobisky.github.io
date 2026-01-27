#include <iostream>

bool is_equal_float(
    const float *a, 
    const float *b
) {
    const float eps_f = std::numeric_limits<float>::epsilon();
    // const float eps_f = 1e-8f; // 比较 CPU 和 GPU 的计算结果.
    float diff = std::fabs(*a - *b);
    if (diff > eps_f) {
        std::cout << "Not Equal" << std::endl;
        return false;
    } else {
        std::cout << "Equal" << std::endl;
        return true;
    }
}

int main() {
    float a = 0.1f + 0.3f;
    float b = 0.4f;
    is_equal_float(&a, &b);
}