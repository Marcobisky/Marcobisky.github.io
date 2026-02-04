#include <iostream>

class Speaker {
public:
    virtual void speak() = 0; // pure virtual
};

class Dog : public Speaker {
public:
    void speak() override {
        std::cout << "Woof" << std::endl;
    }
};

class Cat : public Speaker {
public:
    void speak() override {
        std::cout << "Nya" << std::endl;
    }
};

class SpeakerWrapper : public Speaker {
private:
    Speaker* speaker_;
public:
    SpeakerWrapper(Speaker* speaker) : speaker_(speaker) {}
    void speak() override {
        std::cout << "Wrapper begins: " << std::endl;
        speaker_->speak();
        std::cout << "Wrapper ends." << std::endl;
    }
};

int main() {
    // 不能实例化抽象类
    // Speaker* sp = new Speaker(); // error!

    // 用子类 Dog 声明 dog
    Dog* dog = new Dog();
    // 用抽象类 Speaker 声明 cat
    Speaker* cat = new Cat();
    // 用 wrapper 包装 cat
    Speaker* wrapped_cat = new SpeakerWrapper(cat);

    dog->speak(); // Woof
    cat->speak(); // Nya
    wrapped_cat->speak(); // Wrapper begins: Nya Wrapper ends.

    delete dog;
    delete cat; // Warning! 因为抽象类的析构函数不是虚函数
    delete wrapped_cat; // Warning! 同上
}