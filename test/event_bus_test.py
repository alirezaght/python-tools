import unittest

from patterns.event import Event
from patterns.event_bus import event_subscribe, EventBus, observer


class TestEvent(Event):
    pass


class TestEvent2(Event):
    pass


@observer
class MyClass:

    def __init__(self) -> None:
        super().__init__()
        self.value = 0
        self.value2 = 0

    @event_subscribe(TestEvent)
    @event_subscribe(TestEvent2)
    def increase(self, event: TestEvent):
        self.value += 1
        self.value2 += 1


test_value = 0


@event_subscribe(TestEvent, standalone=True)
def test():
    global test_value
    test_value += 1


class EventBusTest(unittest.TestCase):
    def test_event(self):
        global test_value
        instance = MyClass()
        instance2 = MyClass()
        EventBus.post(TestEvent())
        self.assertEqual(instance.value, 1)
        self.assertEqual(instance.value2, 1)
        self.assertEqual(instance2.value, 1)
        self.assertEqual(instance2.value2, 1)
        self.assertEqual(test_value, 1)
        EventBus.unsubscribe(instance, TestEvent)
        EventBus.post(TestEvent())
        self.assertEqual(instance.value, 1)
        self.assertEqual(instance2.value, 2)
        self.assertEqual(test_value, 2)
        EventBus.unsubscribe("")
        EventBus.post(TestEvent())
        self.assertEqual(instance.value, 1)
        self.assertEqual(instance2.value, 3)
        self.assertEqual(test_value, 2)
        EventBus.post(TestEvent2())
        self.assertEqual(instance.value, 2)
        self.assertEqual(instance2.value2, 4)


if __name__ == '__main__':
    unittest.main()
