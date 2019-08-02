import unittest
from main import text_numbers_to_tuple, cluster_runner, custom_joiner
from src.task import Task
from src.server import Server
from src.cluster import Cluster


class TestMain(unittest.TestCase):
    def test_main_text_numbers_to_tuple(self):
        file_text = '4\n2\n1\n3\n0\n1\n0\n1'
        result = text_numbers_to_tuple(file_text)
        expected = (4, 2, 1, 3, 0, 1, 0, 1)
        self.assertTupleEqual(result, expected)

    def test_main_cluster_runner(self):
        result = cluster_runner(Cluster(4, 2), [1, 3, 0, 1, 0, 1])
        list_expected = [
                [[4]],
                [[3, 4], [4, 4]],
                [[2, 3], [3, 3]],
                [[1, 2], [2, 2], [4]],
                [[1], [1, 1], [3]],
                [[2, 4]],
                [[1, 3]],
                [[2]],
                [[1]]
                ]
        self.assertEqual(15, result['cost'])
        self.assertListEqual(list_expected, result['logs'])

    def test_main_custom_joiner(self):
        inputs = (
            [
                [[2, 2]],
                [[1, 2], [2]],
                [[1], [2, 2]]
            ],
            15
        )
        expected = '2\n2,1\n1,2\n15'
        self.assertEqual(expected, custom_joiner(inputs[0], inputs[1]))


class TestTask(unittest.TestCase):
    def setUp(self):
        self.task = Task(2)
    
    def test_task_missing_ttask(self):
        """Test the start of missing_ttask var."""
        self.assertEqual(2, self.task.missing_ttask)
    
    def test_task_clock(self):
        """tests missing_ttask every clock()."""
        self.task.clock()
        self.assertEqual(1, self.task.missing_ttask)
        self.task.clock()
        self.assertEqual(0, self.task.missing_ttask)
    
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
    
    def test_server_add_task(self):
        self.assertEqual(0, len(self.server.task_list))
        self.server.add_task()
        self.assertEqual(1, len(self.server.task_list))
    
    def test_server_is_working(self):
        self.assertFalse(self.server.is_working())
        self.server.add_task()
        self.assertTrue(self.server.is_working())

    def test_server_task_umax_limit(self):
        """Tests the server UMAX limits."""
        for i in range(self.UMAX):
            self.server.add_task()
        self.assertRaises(Exception, self.server.add_task)

    def test_server_task_ttask_limit(self):
        """Tests the server TTASK limits."""
        with self.assertRaises(AssertionError):
            Server(11, 10)

    def test_server_task_finish(self):
        """Tests if server is finishing tasks."""
        self.server.add_task()
        for i in range(self.TTASK):
            self.server.clock()
        self.assertFalse(self.server.is_working())

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
        """Checks if server clock influences tasks."""
        self.server.add_task()
        self.server.clock()
        self.assertEqual(self.server.task_list[0].missing_ttask, 3)

    def test_server_clock_remove_tasks(self):
        self.server.add_task()
        self.server.clock()
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


class TestCluster(unittest.TestCase):
    def setUp(self):
        self.TTASK = 4
        self.UMAX = 2
        self.cluster = Cluster(self.TTASK, self.UMAX)

    def test_cluster_add_server(self):
        """Tests server creation in cluster."""
        self.cluster.add_server()
        self.assertEqual(1, len(self.cluster.servers_list))
        self.cluster.add_server(5)
        self.assertEqual(6, len(self.cluster.servers_list))

    def test_cluster_add_task(self):
        """Checks task and server health when creating tasks."""
        self.cluster.add_task(1)
        self.assertEqual(1, len(self.cluster.servers_list))
        self.assertEqual(1, len(self.cluster.servers_list[0].task_list))

        self.cluster.add_task(2)
        self.assertEqual(2, len(self.cluster.servers_list))
        self.assertEqual(2, len(self.cluster.servers_list[0].task_list))
        self.assertEqual(1, len(self.cluster.servers_list[1].task_list))

        self.cluster.add_task(2)
        self.assertEqual(3, len(self.cluster.servers_list))
        self.assertEqual(2, len(self.cluster.servers_list[0].task_list))
        self.assertEqual(2, len(self.cluster.servers_list[1].task_list))
        self.assertEqual(1, len(self.cluster.servers_list[2].task_list))

    def test_cluster_clock_reverberate(self):
        """Checks if cluster clock reverberates in tasks."""
        self.cluster.add_task()
        self.assertEqual(1, len(self.cluster.servers_list[0].task_list))
        self.cluster.clock()
        self.assertEqual(3, self.cluster.servers_list[0].task_list[0].missing_ttask)

    def test_cluster_clock_remove_server(self):
        self.cluster.add_task()
        for i in range(self.TTASK):
            self.cluster.clock()
        self.assertEqual(0, len(self.cluster.servers_list))

    def test_cluster_stats_like_pdf_example(self):
        """Tests cluster status like a PDF example."""
        self.cluster.add_task()
        self.assertListEqual([[4]], self.cluster.stats())
        self.cluster.clock()

        self.cluster.add_task(3)
        self.assertListEqual([[3, 4], [4, 4]], self.cluster.stats())
        self.cluster.clock()

        self.assertListEqual([[2, 3], [3, 3]], self.cluster.stats())
        self.cluster.clock()

        self.cluster.add_task(1)
        self.assertListEqual([[1, 2], [2, 2], [4]], self.cluster.stats())
        self.cluster.clock()

        self.assertListEqual([[1], [1, 1], [3]], self.cluster.stats())
        self.cluster.clock()

        self.cluster.add_task(1)
        self.assertListEqual([[2, 4]], self.cluster.stats())
        self.cluster.clock()

        self.assertListEqual([[1, 3]], self.cluster.stats())
        self.cluster.clock()

        self.assertListEqual([[2]], self.cluster.stats())
        self.cluster.clock()

        self.assertListEqual([[1]], self.cluster.stats())
        self.cluster.clock()

        self.assertListEqual([], self.cluster.stats())
