import unittest

from patterns.autowired import autowired
from patterns.singleton import Singleton, singleton


@singleton
class Class1:
    def me(self):
        return "class1"


@autowired
class Class2:
    c: Class1

    def me(self):
        return f"class2, {self.c.me()}"


@singleton
class Class3(Class2):
    def me(self):
        return "class3"


@autowired
class Class4:
    c: Class2

    def me(self):
        return f"class4, {self.c.me()}"


class AutowiredTest(unittest.TestCase):
    def test_autowired(self):
        class1 = Class1()
        class2 = Class2()
        class3 = Class3()
        class4 = Class4()
        self.assertEqual(type(class4.c), type(Class3()))
        self.assertEqual(class4.c is not None, True)
        self.assertEqual(class1.me(), "class1")
        self.assertEqual(class2.me(), "class2, class1")
        self.assertEqual(class4.me(), "class4, class3")


if __name__ == '__main__':
    unittest.main()
