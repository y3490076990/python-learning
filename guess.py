import random

number = random.randint(1, 100)
guess = 0
count = 0 
print("我想了一个 1 到 100 之间的数字。")

while guess != number:
      guess = int(input("你猜是多少？ "))
      count = count + 1
      if guess > number:
          print("高了。")
      elif guess < number:
          print("低了。")






print(f"猜对了！你一共猜了 {count} 次。")