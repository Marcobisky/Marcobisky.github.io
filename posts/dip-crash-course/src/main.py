import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.stats import norm

# --- 1. 数据准备 ---
def get_pdf_cdf():
    x = np.linspace(0, 1, 500)
    # 构造一个有起伏的 PDF
    pdf_raw = 0.4 * norm.pdf(x, 0.3, 0.08) + 0.6 * norm.pdf(x, 0.7, 0.12)
    pdf_raw /= np.trapz(pdf_raw, x)
    cdf_raw = np.cumsum(pdf_raw) * (x[1] - x[0])
    cdf_raw /= cdf_raw[-1]
    return x, pdf_raw, cdf_raw

x_base, pdf_base, cdf_base = get_pdf_cdf()

def y_to_x(y_vals):
    return np.interp(y_vals, cdf_base, x_base)

# --- 2. 画布与样式设置 ---
fig, ax = plt.subplots(figsize=(10, 7), dpi=100)
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.05, 1.1)

# 显式绘制坐标轴线条
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlabel(r"Original pixel value $\mathbb{Z}_{256}$", fontsize=12)
ax.set_ylabel(r"Equalized pixel value $\mathbb{Z}_{256}$", fontsize=12)

# 设置刻度显示为0-255
ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_xticklabels(['0', '64', '128', '192', '255'])
ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_yticklabels(['0', '64', '128', '192', '255'])

# 颜色
COLOR_CDF = '#1F77B4' # 深蓝
COLOR_PDF = '#FF7F0E' # 橙色
COLOR_DOT = '#D62728' # 红色
COLOR_LINE = '#7F7F7F' # 灰色虚线

# 初始化元素
line_cdf, = ax.plot(x_base, cdf_base, color=COLOR_CDF, lw=2.5, label='CDF', zorder=4)
# PDF 预设一个高度缩放系数 (例如 0.4)，使其不遮挡整个图
pdf_display_scale = 0.1
line_pdf, = ax.plot(x_base, pdf_base * pdf_display_scale, color=COLOR_PDF, lw=3, alpha=0, zorder=3)
dots_x, = ax.plot([], [], 'o', color=COLOR_DOT, markersize=3, alpha=0.6, zorder=5)
traj_lines = []
txt = ax.text(0.5, 1.05, "", ha='center', fontsize=13, fontweight='bold', color='#333333')

# --- 3. 动画逻辑 ---
# 阶段划分 (总共 240 帧)
# 0-80: 初始少量点映射 (含轨迹)
# 80-160: 增加点和虚线的密度
# 160-200: PDF 渐渐升起，虚线褪去
# 200-240: 静态展示结果
TOTAL_FRAMES = 240

def update(frame):
    global traj_lines
    # 清理旧虚线
    for l in traj_lines:
        try: l.remove()
        except: pass
    traj_lines = []

    if frame < 80: # 阶段 1: 演示映射轨迹
        txt.set_text("Step 1: Mapping uniform y to x via CDF")
        prog = frame / 80
        n_pts = 12
        y_pts = np.linspace(0.05, 0.95, n_pts)
        x_target = y_to_x(y_pts)
        
        curr_x, curr_y = [], []
        for i in range(n_pts):
            if prog < 0.5: # 横向移动
                p = prog * 2
                tx, ty = p * x_target[i], y_pts[i]
                l, = ax.plot([0, tx], [ty, ty], '--', color=COLOR_LINE, lw=1.5, alpha=0.4)
            else: # 纵向落下
                p = (prog - 0.5) * 2
                tx, ty = x_target[i], y_pts[i] * (1 - p)
                l1, = ax.plot([0, tx], [y_pts[i], y_pts[i]], '--', color=COLOR_LINE, lw=1.5, alpha=0.4)
                l2, = ax.plot([tx, tx], [y_pts[i], ty], '--', color=COLOR_LINE, lw=1.5, alpha=0.4)
                traj_lines.append(l1)
                l = l2
            traj_lines.append(l)
            curr_x.append(tx); curr_y.append(ty)
        dots_x.set_data(curr_x, curr_y)

    elif frame < 160: # 阶段 2: 增加密度
        txt.set_text("Step 2: Increasing sample density")
        prog = (frame - 80) / 80
        n_display = int(12 + 50 * prog)  # 显示的线条数量从12逐渐增加到62
        y_pts = np.linspace(0.01, 0.99, n_display)
        x_target = y_to_x(y_pts)
        
        # 绘制密集的映射虚线
        for i in range(n_display):
            l1, = ax.plot([0, x_target[i]], [y_pts[i], y_pts[i]], '--', color=COLOR_LINE, lw=1.0, alpha=0.5)
            l2, = ax.plot([x_target[i], x_target[i]], [y_pts[i], 0], '--', color=COLOR_LINE, lw=1.0, alpha=0.5)
            traj_lines.append(l1); traj_lines.append(l2)
        dots_x.set_data(x_target, np.zeros_like(x_target))

    elif frame < 200: # 阶段 3: PDF 升起
        txt.set_text("Step 3: Point density = PDF (Derivative of CDF)")
        prog = (frame - 160) / 40
        n_final = 132
        y_pts = np.linspace(0.01, 0.99, n_final)
        x_target = y_to_x(y_pts)
        dots_x.set_data(x_target, np.zeros_like(x_target))
        
        # PDF 渐显并固定
        line_pdf.set_alpha(prog)
        
        # 虚线渐隐 (从0.5渐隐到0)
        alpha_val = 0.5 * (1 - prog)
        if alpha_val > 0.01:
            for i in range(0, n_final, 2):
                l1, = ax.plot([0, x_target[i]], [y_pts[i], y_pts[i]], '--', color=COLOR_LINE, lw=1.0, alpha=alpha_val)
                l2, = ax.plot([x_target[i], x_target[i]], [y_pts[i], 0], '--', color=COLOR_LINE, lw=1.0, alpha=alpha_val)
                traj_lines.append(l1); traj_lines.append(l2)
    
    else: # 阶段 4: 静态停留
        line_pdf.set_alpha(1.0)
        txt.set_text("Final: The density distribution is the PDF")

    return [dots_x, line_pdf, txt] + traj_lines

ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, interval=40, blit=False)

# 保存
writer = PillowWriter(fps=25)
ani.save("histogram_logic_v2.gif", writer=writer)
plt.show()