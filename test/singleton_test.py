import unittest

from patterns.prototype import Prototype, prototype
from patterns.singleton import Singleton, singleton


class SingletonClass(metaclass=Singleton):
    pass


class PrototypeClass(metaclass=Prototype):
    pass


@prototype
class ProtoDecorator:
    pass


@singleton
class SingleDecorator:
    pass


class ComponentTest(unittest.TestCase):
    def test_singleton(self):
        class1 = SingletonClass()
        class2 = SingletonClass()
        class3 = SingleDecorator()
        class4 = SingleDecorator()
        self.assertEqual(class1, class2)
        self.assertEqual(class3, class4)


    def test_prototype(self):
        class1 = PrototypeClass()
        class2 = PrototypeClass()
        class3 = ProtoDecorator()
        class4 = ProtoDecorator()
        self.assertEqual(class1 == class2, False)
        self.assertEqual(class3 == class4, False)



if __name__ == '__main__':
    unittest.main()
