import json
import os

FILE = "contacts.json"

class Contact:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {"name": self.name, "phone": self.phone, "email": self.email}

    @classmethod
    def from_dict(cls, d):
        return cls(d["name"], d["phone"], d["email"])

    def __str__(self):
        return f"{self.name} | {self.phone} | {self.email}"


class BusinessContact(Contact):
    def __init__(self, name, phone, email, company, title):
        super().__init__(name, phone, email)
        self.company = company
        self.title = title

    def to_dict(self):
        d = super().to_dict()
        d["company"] = self.company
        d["title"] = self.title
        d["type"] = "business"
        return d

    def __str__(self):
        return f"{self.name} | {self.phone} | {self.email} | {self.title} @ {self.company}"


class ContactBook:
    def __init__(self):
        self.contacts = []

    def add(self, contact):
        self.contacts.append(contact)

    def list_all(self):
        if not self.contacts:
            print("暂无联系人。")
            return
        for i, c in enumerate(self.contacts, 1):
            print(f"{i}. {c}")

    def search(self, keyword):
        result = [c for c in self.contacts if keyword.lower() in c.name.lower()]
        if not result:
            print(f"找不到包含 '{keyword}' 的联系人。")
            return
        for i, c in enumerate(result, 1):
            print(f"{i}. {c}")

    def delete(self, index):
        if 1 <= index <= len(self.contacts):
            removed = self.contacts.pop(index - 1)
            print(f"已删除: {removed.name}")
        else:
            print("编号无效。")

    def save(self):
        data = [c.to_dict() for c in self.contacts]
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self):
        if os.path.exists(FILE):
            with open(FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for item in data:
                if item.get("type") == "business":
                    c = BusinessContact.from_dict(item)
                else:
                    c = Contact.from_dict(item)
                self.contacts.append(c)


book = ContactBook()
book.load()

while True:
    print("\n--- 联系人管理 ---")
    print("1. 查看全部  2. 搜索  3. 添加普通  4. 添加商务  5. 删除  6. 保存并退出")
    cmd = input("选一个数字: ")

    if cmd == "1":
        book.list_all()
    elif cmd == "2":
        kw = input("输入名字关键词: ")
        book.search(kw)
    elif cmd == "3":
        name = input("姓名: ")
        phone = input("电话: ")
        email = input("邮箱: ")
        book.add(Contact(name, phone, email))
        print("已添加。")
    elif cmd == "4":
        name = input("姓名: ")
        phone = input("电话: ")
        email = input("邮箱: ")
        company = input("公司: ")
        title = input("职位: ")
        book.add(BusinessContact(name, phone, email, company, title))
        print("已添加。")
    elif cmd == "5":
        book.list_all()
        n = int(input("删除第几个? "))
        book.delete(n)
    elif cmd == "6":
        book.save()
        print("已保存。再见。")
        break
    else:
        print("输入 1-6。")