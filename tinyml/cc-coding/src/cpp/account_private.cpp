class Account {
private:
    double balance;

public:
    // const: no modification to member variables
    double getBalance() const { return balance; }

    void deposit(double amount) {
        if (amount > 0)
            balance += amount;
    }
};
