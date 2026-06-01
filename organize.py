import os
import shutil
RULES = {
      ".jpg": "图片", ".png": "图片", ".gif": "图片",
      ".pdf": "文档", ".docx": "文档", ".txt": "文档",
      ".py": "代码", ".js": "代码", ".html": "代码",
  }
import argparse
parser = argparse.ArgumentParser(description="按扩展名整理文件")
parser.add_argument("path", help="要整理的文件夹路径")
args = parser.parse_args()

target_dir = args.path
if not os.path.exists(target_dir):
      print(f"路径不存在: {target_dir}")
      exit()
moved = 0
errors = 0 
for root, dirs, files in os.walk(target_dir):
    for filename in files:
        ext = os.path.splitext(filename)[1].lower()
        src = os.path.join(root, filename)   
        if ext not in RULES:
              continue

        folder = os.path.join(target_dir, RULES[ext])
        if not os.path.exists(folder):
              os.makedirs(folder)

        dst = os.path.join(folder, filename)

        try:
              shutil.move(src, dst)
              print(f"  ✓ {filename} → {RULES[ext]}/")
              moved = moved + 1
        except Exception as e:
              print(f"  ✗ {filename}: {e}")
              errors = errors + 1

print(f"\n完成。移了 {moved} 个文件，{errors} 个失败。")       