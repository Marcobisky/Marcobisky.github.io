#include <iostream>
using namespace std;

class Small 
{
public:
    Small()
    {
        cout << 1 << endl;
    }

    Small(int in)
    {
        cout << 2 << endl;
    }
};

class Big
{
private:
    Small small;
public:
    Big(int in) 
        : small(in)
    {
        cout << 3 << endl; 
    }
};

int main()
{
    Big big(7); // Output: 2 3
    return 0;
}