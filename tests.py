# python -m unittest
import unittest
import main
from task import Task
from server import Server


class TestTextNumbersToTuple(unittest.TestCase):
    def setUp(self):
        self.file_text = '4\n2\n1\n3\n0\n1\n0\n1'
    
    def test(self):
        result = main.text_numbers_to_tuple(self.file_text)
        expected = (4, 2, 1, 3, 0, 1, 0, 1)
        self.assertTupleEqual(result, expected)


class TestTask(unittest.TestCase):
    def setUp(self):
        self.task = Task(2)
    
    def test_task_missing_ttask(self):
        self.assertEqual(2, self.task.missing_ttask)
    
    def test_task_clock(self):
        self.task.clock()
        self.assertEqual(1, self.task.missing_ttask)
        self.task.clock()
        self.assertEqual(0, self.task.missing_ttask)
        self.assertRaises(AssertionError, self.task.clock)
    
    def test_task_alive(self):
        self.task.clock()
        self.assertTrue(self.task.is_alive())
        self.task.clock()
        self.assertFalse(self.task.is_alive())


class TestServer(unittest.TestCase):
    def setUp(self):
        self.TTASK = 5
        self.UMAX = 8
        self.server = Server(self.TTASK, self.UMAX)
    
    def test_server_attributes(self):
        self.assertEqual(self.server.ttask, self.TTASK)
        self.assertEqual(self.server.umax, self.UMAX)
    
    def test_server_task(self):
        self.assertEqual(0, len(self.server.task_list))
        self.server.add_task()
        self.assertEqual(1, len(self.server.task_list))
        self.assertIsInstance(self.server.task_list, list)
        self.assertIsInstance(self.server.task_list[0], Task)
    
    def test_server_is_working(self):
        self.assertFalse(self.server.is_working())
        self.server.add_task()
        self.assertTrue(self.server.is_working())
    
    def test_server_task_limit(self):
        for i in range(self.UMAX):
            self.server.add_task()
        self.assertRaises(Exception, self.server.add_task)

    def test_server_task_finish(self):
        self.server.add_task()
        self.assertTrue(self.server.is_working())
        for i in range(self.TTASK):
            self.server.clock()
        self.assertFalse(self.server.is_working())
    
    def test_server_ttask_limits(self):
        with self.assertRaises(AssertionError):
             Server(11, 10)
        
    def test_server_umax_limits(self):
        with self.assertRaises(AssertionError):
             Server(10, 11)

    def test_server_have_slots(self):
        self.assertEqual(self.UMAX, self.server.available_slots())
        for i in range(self.UMAX):
            self.server.add_task()
        self.assertEqual(0, self.server.available_slots())


class TestServerClock(unittest.TestCase):
    def setUp(self):
        self.TTASK = 4
        self.UMAX = 2
        self.server = Server(self.TTASK, self.UMAX)
    
    def test_server_clock(self):
        self.server.add_task()
        self.server.clock()
        self.assertEqual(self.server.task_list[0].missing_ttask, 3)
        
        self.server.add_task()
        self.server.clock()
        self.assertEqual(self.server.task_list[0].missing_ttask, 2)
        self.assertEqual(self.server.task_list[1].missing_ttask, 3)
        
        self.server.clock()
        self.assertEqual(self.server.task_list[0].missing_ttask, 1)
        self.assertEqual(self.server.task_list[1].missing_ttask, 2)
        
        self.server.clock()
        self.assertEqual(self.server.task_list[0].missing_ttask, 1)
        
        self.server.add_task()
        self.server.clock()
        self.assertEqual(self.server.task_list[0].missing_ttask, 3)
