#include <iostream>

class Speaker {
public:
    virtual void speak() = 0; // pure virtual
};

class Dog : public Speaker {
public:
    void speak() override {
        std::cout << "Woof\n";
    }
};

class Cat : public Speaker {
public:
    void speak() override {
        std::cout << "Nya\n";
    }
};

int main() {
    // 不能实例化抽象类
    // Speaker* sp = new Speaker(); // error!
    // 用子类声明
    Dog* dog = new Dog();
    // 用 Speaker 声明
    Speaker* cat = new Cat();

    dog->speak(); // Woof
    cat->speak(); // Nya

    delete dog;
    delete cat; // Warning!
}