"""
占用检查服务
用于探测目录或文件是否被其他进程锁定
"""
import os
import subprocess
import logging

class OccupancyService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # 预设的知名 IDE/程序进程名
        self.known_processes = {
            "Trae.exe": "Trae IDE",
            "Code.exe": "Visual Studio Code",
            "cursor.exe": "Cursor",
            "chrome.exe": "Google Chrome",
            "msedge.exe": "Microsoft Edge"
        }

    def get_locking_processes(self, path: str) -> list[str]:
        """
        获取锁定指定路径的进程列表 (模糊尝试)
        
        Args:
            path: 检查的路径
        Returns:
            list[str]: 发现的进程描述列表
        """
        if not os.path.exists(path):
            return []

        results = []
        
        # 1. 尝试通过重命名探测物理锁定 (Windows 下最有效)
        try:
            temp_name = path + ".lock_test"
            os.rename(path, temp_name)
            os.rename(temp_name, path) # 换回来
        except OSError:
            # 如果报错，说明被锁定
            results.append("系统检测到文件流被占用 (文件可能正在被读写)")

        # 2. 尝试匹配运行中的知名程序 (模糊匹配)
        # 获取当前运行的进程列表
        try:
            cmd = 'tasklist /NH /FO CSV'
            output = subprocess.check_output(cmd, shell=True, text=True)
            for proc_name, display_name in self.known_processes.items():
                if proc_name.lower() in output.lower():
                    # 这里是一个弱校验：只要程序开着，我们就认为可能有风险
                    # 特别是针对电子类 (Electron) 应用
                    results.append(f"{display_name} 正在运行")
        except:
            pass

        return list(set(results))

    def is_locked(self, path: str) -> bool:
        """检查路径是否被锁定"""
        return len(self.get_locking_processes(path)) > 0
