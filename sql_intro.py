import sqlite3

  # 创建内存数据库（关掉就没了，先练习）
conn = sqlite3.connect(":memory:")
cur = conn.cursor()

  # 建表
cur.execute("""
  CREATE TABLE users (
      id INTEGER PRIMARY KEY,
      name TEXT NOT NULL,
      age INTEGER
  )
  """)

  # 插入数据
cur.execute("INSERT INTO users (name, age) VALUES ('张三', 25)")
cur.execute("INSERT INTO users (name, age) VALUES ('李四', 30)")
cur.execute("INSERT INTO users (name, age) VALUES ('王五', 22)")

  # 查询全部
print("=== 全部用户 ===")
for row in cur.execute("SELECT * FROM users"):
      print(row)

  # 条件查询
print("\n=== 年龄 > 23 ===")
for row in cur.execute("SELECT * FROM users WHERE age > 23"):
      print(row)

  # 更新
cur.execute("UPDATE users SET age = 26 WHERE name = '张三'")

  # 删除
cur.execute("DELETE FROM users WHERE name = '王五'")

  # 查看结果
print("\n=== 修改后 ===")
for row in cur.execute("SELECT * FROM users"):
      print(row)

  # 统计
print("\n=== 统计 ===")
row = cur.execute("SELECT COUNT(*), AVG(age) FROM users").fetchone()
print(f"总人数: {row[0]}, 平均年龄: {row[1]:.1f}")

conn.close()