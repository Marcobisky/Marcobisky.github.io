# 定义两个 target: mathlib 和 utilslib 库, 并使用动态链接
add_library(mathlib SHARED add.cc)
add_library(utilslib SHARED utils.cc)

# 头文件搜索路径
target_include_directories(mathlib PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})      # 当前目录下的文件会自动暴露给 mathlib 的使用者 (main.cc)
target_include_directories(utilslib PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})    # 仅当前目录下的文件不会暴露给 utilslib 的使用者

# 设置一些 target 行为 (示例)
set_target_properties(mathlib PROPERTIES
    CXX_STANDARD 17
    POSITION_INDEPENDENT_CODE ON
)

# 安装规则：安装库本身 (可选, 这里主要示范)
install(TARGETS mathlib 
    LIBRARY DESTINATION lib     # LIBRARY 表示 SHARED 动态库 (.dylib) 的安装路径
    ARCHIVE DESTINATION lib     # ARCHIVE 表示 STATIC 静态库 (.a) 的安装路径 (该文件可忽略)
)
install(TARGETS utilslib 
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)

# 复制一份头文件, 这样基于 demo-proj 的项目可以用 include 引用这些头文件. (但别安装源文件)
install(FILES add.h utils.h DESTINATION include)