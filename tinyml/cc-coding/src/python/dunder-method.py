def addone(x):
    return x + 1

class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __str__(self):  # 决定了当你使用 print() 或 str() 时的输出内容
        return f"The book is '{self.title}' by {self.author}"

    def __len__(self):  # 决定了当你使用 len() 时的返回值
        return self.pages
    
    def __eq__(self, other):    # 决定了当你使用 == 时的比较行为
        if isinstance(other, Book):
            return self.title == other.title and self.author == other.author
        return False
    
    def __call__(self): # 允许实例像函数一样被调用
        return f"Reading '{self.title}'..."
    
    def __addone__(self):   # 不能自定义魔法方法
        return self.pages + 1
    
# Example usage
book1 = Book("1984", "George Orwell", 328)
book2 = Book("1984", "George Orwell", 328)
book3 = Book("Brave New World", "Aldous Huxley", 288)
print(book1)                  # Output: The book is '1984' by George Orwell
print(len(book1))             # Output: 328
print(book1 == book2)         # Output: True
print(book1 == book3)         # Output: False
print(book1())                # Output: Reading '1984'...
print(addone(book1))          # Error!