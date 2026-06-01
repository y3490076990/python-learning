import re
def read_file(path):
      with open(path, "r", encoding="utf-8") as f:
          return f.read()
text = read_file("sample.txt")
words = re.findall(r"[a-zA-Z]+", text.lower())
total = len(words)
unique = len(set(words))
freq = {}
for w in words:
      if w in freq:
          freq[w] = freq[w] + 1
      else:
          freq[w] = 1
print(f"总词数: {total}")
print(f"不重复词数: {unique}")
print(f"最长词: {max(words, key=len)}")
print(f"最短词: {min(words, key=len)}")          
sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
print("\n出现最多的 10 个词:")
for word, count in sorted_words[:10]:
      print(f"  {word}: {count}次")