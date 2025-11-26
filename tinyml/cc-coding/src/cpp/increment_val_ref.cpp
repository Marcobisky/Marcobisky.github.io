#include <iostream>
void increment(int& num) {num++;}
int main()
{
	int value = 5;
	increment(value); // Pass by reference
	std::cout << "value = " << value << std::endl; // Outputs: value = 6
	return 0;
}