library(staticryptR)

staticryptR::staticryptr(
  # files     = "../docs/tinyml/eda-3d-placement/", # 要加密的目录
  files = c("../docs/tinyml/eda-3d-placement/eda-3d-placement.html"), 
  directory = "../docs/tinyml/eda-3d-placement/",  # 用 “.” 表示在输出目录内部替换文件
  password  = "142857",         # 建议长度较长
  short     = TRUE,                    # 如果密码长度太短可设 TRUE
  # recursive = TRUE,                    # 遍历子目录
  # 可选：定制加密页面的外观
  template_color_primary   = "#6667AB",
  template_color_secondary = "#f9f9f3",
  template_title           = "Protected Page",
  template_instructions    = "Please enter the password to access this page:",
  template_button          = "Access"
)
