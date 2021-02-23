from unittest import TestCase
from BuisnessLayer.ExternalSystemsAPIsManager.snopesManager import SnopesManager

class TestSnopesManager(TestCase):
    def setUp(self) -> None:
        self.snopes_manager = SnopesManager()


    def test_stop(self):
        self.snopes_manager.stop()

    def test_start(self):
        self.snopes_manager.start()
