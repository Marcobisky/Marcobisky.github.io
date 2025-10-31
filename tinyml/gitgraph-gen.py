import requests
import os

from traitlets import default


OWNER = "Marcobisky"
REPO  = "my-riscv"
BRANCH = "main"       # 或者你想展示的分支
N = 20                # 获取最近 N 条提交

token = os.getenv("GITHUB_TOKEN")  # 如果有 token 可以设环境变量 GITHUB_TOKEN
headers = {"Accept": "application/vnd.github+json"}
if token:
    headers["Authorization"] = f"Bearer {token}"

url = f"https://api.github.com/repos/{OWNER}/{REPO}/commits"
params = {"sha": BRANCH, "per_page": N}

resp = requests.get(url, headers=headers, params=params)
resp.raise_for_status()
commits = resp.json()

# Reverse the commits to show oldest first (chronological order)
commits = list(reversed(commits))

filename = "my-riscv-gitgraph.mmd"
with open(filename, "w", encoding="utf-8") as f:
    f.write("---\nconfig:\n\ttheme: 'default'\n\tthemeVariables:\n\t\t'git0': '#ffb700ff'\n---\n")
    f.write("gitGraph\n")
    for c in commits:
        sha = c["sha"][:7]
        # 用第一行 commit message 做 tag（如长度太长你可做截断）
        msg0 = c["commit"]["message"].splitlines()[0]
        tag = msg0.replace('"', "'")  # 避免双引号冲突
        # 如果 tag 长度超过 30，截断并加上 ...
        if len(tag) > 30:
            tag = tag[:27] + "..."
        # line = f'  commit id: "{sha}" tag: "{tag}"\n'
        line = f'  commit id: "{tag}"\n'  # 只用 tag，避免 sha 太长
        f.write(line)

print(f"Wrote {filename} with {len(commits)} commits")