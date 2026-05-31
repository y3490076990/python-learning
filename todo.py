import json
import os

FILE = "todos.json"

def load():
      if os.path.exists(FILE):
          with open(FILE, "r", encoding="utf-8") as f:
              return json.load(f)
      return []

def save(todos):
      with open(FILE, "w", encoding="utf-8") as f:
          json.dump(todos, f, ensure_ascii=False, indent=2)

def show(todos):
      if not todos:
          print("暂无待办事项。")
          return
      for i, t in enumerate(todos, 1):
          status = "✓" if t["done"] else "○"
          print(f"{i}. {status} {t['text']}")

todos = load()

while True:
      print("\n--- 待办事项 ---")
      print("1. 查看  2. 添加  3. 标记完成  4. 删除  5. 退出")
      cmd = input("选一个数字： ")

      if cmd == "1":
          show(todos)
      elif cmd == "2":
          text = input("输入新事项： ")
          todos.append({"text": text, "done": False})
          save(todos)
          print("已添加。")
      elif cmd == "3":
          show(todos)
          n = int(input("标记第几个为完成？ "))
          if 1 <= n <= len(todos):
              todos[n-1]["done"] = True
              save(todos)
              print("已标记。")
      elif cmd == "4":
          show(todos)
          n = int(input("删除第几个？ "))
          if 1 <= n <= len(todos):
              del todos[n-1]
              save(todos)
              print("已删除。")
      elif cmd == "5":
          print("再见。")
          break
      else:
          print("输入 1-5。")