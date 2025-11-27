#include <iostream>

class Point {
private:
    int x_ = 0; int y_ = 0;

public:
    Point& setX(int x) {
        x_ = x;
        return *this; 
    }

    Point& setY(int y) {
        y_ = y;
        return *this;
    }
};

int main() {
    Point p;
    // Set values by chaining
    p.setX(10).setY(20);
}
