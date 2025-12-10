class Point
{
public:
    double x, y;

    Point(double x_coor, double y_coor)
        : x(x_coor), y(y_coor) {}

    Point Add(const Point& other) const
    {
        return *this + other;
    }

    Point operator+(const Point& other) const
    {
        return Point(x + other.x, y + other.y);
    }
};