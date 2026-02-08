import os
import sys
import shutil
import unittest

# 修复导入路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PySide6.QtWidgets import QApplication
from src.services.migration_service import MigrationService

class TestMigrationService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 创建一个 QApplication 实例，因为 MigrationService 使用了 QThread/QObject
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.test_dir = os.path.abspath("test_migration_data")
        self.src_dir = os.path.join(self.test_dir, "src")
        self.dst_dir = os.path.join(self.test_dir, "dst")
        
        # 创建测试数据
        os.makedirs(self.src_dir, exist_ok=True)
        with open(os.path.join(self.src_dir, "file1.txt"), "w") as f:
            f.write("hello" * 1000)
        
        os.makedirs(os.path.join(self.src_dir, "subdir"), exist_ok=True)
        with open(os.path.join(self.src_dir, "subdir", "file2.txt"), "w") as f:
            f.write("world" * 2000)

        self.service = MigrationService()

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_calculate_size(self):
        from src.services.migration_service import MigrationWorker
        worker = MigrationWorker(self.src_dir, self.dst_dir)
        size = worker.calculate_total_size(self.src_dir)
        # file1: 5000 bytes, file2: 10000 bytes
        self.assertEqual(size, 15000)

    def test_migration_copy(self):
        finished_success = False
        def on_finished(success, msg):
            nonlocal finished_success
            finished_success = success
            self.app.quit()

        self.service.migrate_async(self.src_dir, self.dst_dir, mode="copy", on_finished=on_finished)
        self.app.exec()

        self.assertTrue(finished_success)
        self.assertTrue(os.path.exists(os.path.join(self.dst_dir, "file1.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.dst_dir, "subdir", "file2.txt")))
        self.assertTrue(os.path.exists(self.src_dir)) # Copy 模式源应存在

    def test_migration_move(self):
        finished_success = False
        def on_finished(success, msg):
            nonlocal finished_success
            finished_success = success
            self.app.quit()

        self.service.migrate_async(self.src_dir, self.dst_dir, mode="move", on_finished=on_finished)
        self.app.exec()

        self.assertTrue(finished_success)
        self.assertTrue(os.path.exists(self.dst_dir))
        self.assertFalse(os.path.exists(self.src_dir)) # Move 模式源应被删除

if __name__ == "__main__":
    unittest.main()
