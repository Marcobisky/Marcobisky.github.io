def student_info(name, age, *courses, **extras):
    """
    name: 必需参数
    age: 必需参数  
    *courses: 可变数量的课程
    **extras: 可变数量的额外信息
    """
    print(f"姓名: {name}")
    print(f"年龄: {age}")
    print(f"课程: {courses}")
    print(f"额外信息: {extras}")
    
# 使用, 从第一个格式为 "xxx=yyy" 的参数开始算 extras
student_info("张三", 18, "数学", "物理", "化学", hobby="篮球", score=95)
# 可以没有 courses
student_info("李四", 20, hobby="音乐")
# "历史" 不是 "xxx=yyy" 结构, 报错!
# student_info("王五", 22, "英语", hobby="阅读", "历史")  # SyntaxError