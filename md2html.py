import re
import argparse


def read_md(path):
      with open(path, "r", encoding="utf-8") as f:
          return f.read()


parser = argparse.ArgumentParser(description="Markdown 转 HTML")
parser.add_argument("input", help="输入的 .md 文件路径")
parser.add_argument("-o", "--output", default="output.html", help="输出的 .html 文件名")
args = parser.parse_args()

md = read_md(args.input)
lines = md.split("\n")
html_lines = []

for line in lines:
      if line.startswith("# "):
          html_lines.append(f"<h1>{line[2:]}</h1>")
      elif line.startswith("## "):
          html_lines.append(f"<h2>{line[3:]}</h2>")
      elif line.startswith("### "):
          html_lines.append(f"<h3>{line[4:]}</h3>")
      elif line.strip() == "---":
          html_lines.append("<hr>")
      elif line.strip() == "":
          html_lines.append("")
      else:
          line = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
          line = re.sub(r"\*(.+?)\*", r"<em>\1</em>", line)
          line = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', line)
          line = re.sub(r"`(.+?)`", r"<code>\1</code>", line)
          html_lines.append(f"<p>{line}</p>")

html = "\n".join(html_lines)

template = f"""<!DOCTYPE html>
  <html lang="zh">
  <head>
  <meta charset="UTF-8">
  <title>Converted</title>
  </head>
  <body>
  {html}
  </body>
  </html>"""

with open(args.output, "w", encoding="utf-8") as f:
      f.write(template)

print(f"完成。输出: {args.output}")