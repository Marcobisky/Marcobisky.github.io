```{.c filename="a.c" #lst-ac}
#include <stdio.h>
int my_add(int, int);
int main() {
    int result = my_add(3, 5);
    printf("Result: %d\n", result);
    return 0;
}
```

:::: {.columns}
::: {.column width="52%"}
不用 `extern "C"` 时:

```{.cpp filename="b.cc" #lst-bcc}
int my_add(int x, int y) {return x + y;}
 
 
```

```bash
gcc -c a.c -o a.o
g++ -c b.cc -o b.o
nm a.o  # 查看符号表
nm b.o
g++ a.o b.o -o program # Linking error!
 
```

输出:

```bash
# C 语言的函数名没有变化
0000000000000000 T main         
                 U my_add
                 U printf
# b.o 里的函数名被改成了 _Z6my_addii
0000000000000000 T _Z6my_addii 
# linking error
/bin/ld: a.o: in function `main':
a.c:(.text+0x15): undefined reference to `my_add'
collect2: error: ld returned 1 exit status
```
:::

::: {.column width="2%"}
:::

::: {.column width="46%"}
使用 `extern "C"` 时:

```{.cpp filename="b.cc" #lst-bcc}
extern "C" {
int my_add(int x, int y) {return x + y;}
}
```

```bash
gcc -c a.c -o a.o
g++ -c b.cc -o b.o
nm a.o  # 查看符号表
nm b.o
g++ a.o b.o -o program
./program
```

输出:

```bash
# C 语言的函数名没有变化
0000000000000000 T main         
                 U my_add
                 U printf
# b.o 里的函数名也没有变化
0000000000000000 my_add         
# ./program 执行结果
Result: 8
 
 
```
:::
::::