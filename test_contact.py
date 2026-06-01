import unittest
import sys
import os
from contact import Contact, BusinessContact, ContactBook

class TestContacts(unittest.TestCase):

    def test_create_contact(self):
        c = Contact("张三", "138", "z@mail.com")
        self.assertEqual(c.name, "张三")
        self.assertEqual(c.phone, "138")
        self.assertEqual(c.email, "z@mail.com")

    def test_create_business_contact(self):
        c = BusinessContact("李四", "139", "l@mail.com", "ACME", "经理")
        self.assertEqual(c.name, "李四")
        self.assertEqual(c.company, "ACME")
        self.assertEqual(c.title, "经理")

    def test_contact_to_dict(self):
        c = Contact("张三", "138", "z@mail.com")
        d = c.to_dict()
        self.assertEqual(d["name"], "张三")
        self.assertEqual(d["phone"], "138")

    def test_business_contact_to_dict(self):
        c = BusinessContact("李四", "139", "l@mail.com", "ACME", "经理")
        d = c.to_dict()
        self.assertEqual(d["type"], "business")
        self.assertEqual(d["company"], "ACME")

    def test_contact_str(self):
        c = Contact("张三", "138", "z@mail.com")
        s = str(c)
        self.assertIn("张三", s)
        self.assertIn("138", s)

    def test_contactbook_add_and_list(self):
        book = ContactBook()
        book.add(Contact("王五", "136", "w@mail.com"))
        self.assertEqual(len(book.contacts), 1)

    def test_contactbook_search(self):
        book = ContactBook()
        book.add(Contact("王五", "136", "w@mail.com"))
        book.add(Contact("赵六", "137", "z2@mail.com"))
        # 捕获标准输出以验证搜索逻辑不报错
        old_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        try:
            book.search("王")
        finally:
            sys.stdout.close()
            sys.stdout = old_stdout

    def test_contactbook_delete(self):
        book = ContactBook()
        book.add(Contact("王五", "136", "w@mail.com"))
        book.delete(1)
        self.assertEqual(len(book.contacts), 0)

    def test_contactbook_delete_invalid(self):
        book = ContactBook()
        book.add(Contact("王五", "136", "w@mail.com"))
        book.delete(5)  # 无效编号，不应抛出异常
        self.assertEqual(len(book.contacts), 1)


if __name__ == "__main__":
    runner = unittest.TextTestRunner(stream=sys.stdout)
    unittest.main(testRunner=runner)
