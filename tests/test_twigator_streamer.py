import sys
sys.path.insert(1, ".")
sys.path.insert(2, "..")

import unittest
from unittest.mock import Mock, MagicMock

from twigator.streamer import MyStreamer, QueueReader, run_streamer

from tests import mytestrunner


class MyStreamerTestCase(unittest.TestCase):
    """
    Tests for twigator.streamer.MyStreamer
    """
    def setUp(self) -> None:
        self.streamer = MyStreamer('', '', '', '')

    def test_01_on_success_normal(self) -> None:
        self.streamer.queue = MagicMock()
        #self.streamer.queue.put_nowait =

    def test_02_on_success_limit(self) -> None:
        pass

    def test_03_on_error(self) -> None:
        pass

    def tearDown(self) -> None:
        pass


class QueueReaderTestCase(unittest.TestCase):
    """
    Tests for twigator.streamer.QueueReader
    """
    def setUp(self) -> None:
        pass

    def test_01_add_to_db(self) -> None:
        pass

    def test_02_process_chunk(self) -> None:
        pass

    def test_03_set_exit(self) -> None:
        pass

    def test_04_run(self) -> None:
        pass

    def tearDown(self) -> None:
        pass


class RunStreamerTestCase(unittest.TestCase):
    """
    Tests for twigator.streamer.run_streamer
    """
    def setUp(self) -> None:
        pass

    def test_01_dummy(self) -> None:
        pass

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    classes = [MyStreamerTestCase, QueueReaderTestCase, RunStreamerTestCase]
    mytestrunner(classes)
