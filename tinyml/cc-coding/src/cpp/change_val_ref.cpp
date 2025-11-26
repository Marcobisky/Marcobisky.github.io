#include <iostream>
int main()
{
	int a = 5;
	int& ref = a; // ref is an alias to a
	ref = 10;     // Actually modifies a
	std::cout << "a = " << a << std::endl; // Outputs: a = 10
	return 0;
}