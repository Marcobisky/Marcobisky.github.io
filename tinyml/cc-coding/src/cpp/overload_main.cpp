#include <iostream>
#include "overload_op_calls_method.cpp"

int main()
{
    Point p1(1.0, 2.0);
    Point p2(3.0, 4.0);

    Point p3 = p1 + p2;  // i.e., p3 = p1.operator+(p2);
    std::cout << "p3: (" << p3.x << ", " << p3.y << ")\n"; // p3: (4, 6)

    return 0;
}