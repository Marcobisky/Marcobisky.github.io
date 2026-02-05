cmake_minimum_required(VERSION 3.16)
project(DemoInstall LANGUAGES CXX)

# 声明可能会使用子模块 math/CMakeLists.txt 中的所有 targets (mathlib 和 utilslib) 并跳到里面去执行!
add_subdirectory(math)

# 定义可执行的 target 名称: myapp
add_executable(myapp main.cc)

# 手动设置 RPATH, 让可执行文件能找到动态库
set_target_properties(myapp PROPERTIES
    INSTALL_RPATH "@executable_path/../lib"
    BUILD_WITH_INSTALL_RPATH TRUE
)

# 声明 myapp target 依赖 mathlib target 
# PRIVATE 的意思是 mathlib 仅为 myapp 服务, 不会暴露给 myapp 的使用者
# 如果是 PUBLIC 则表示 mathlib 也会暴露给 myapp 的使用者
# 如果是 INTERFACE 则表示 mathlib 只暴露给 myapp 的使用者, 而 myapp 自身不需要 mathlib
# 虽然 utilslib 也被引入了, 但这里没有使用
target_link_libraries(myapp PRIVATE mathlib)

# 将生成的可执行文件 myapp 放到 install/bin/ 目录下
install(TARGETS myapp RUNTIME DESTINATION bin)  # RUNTIME 表示可执行文件