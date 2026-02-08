# coding: utf-8
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

    def get_detailed_occupancy(self, path: str) -> dict:
        """
        通过物理锁定测试和命令行参数分析，精准探测关联进程
        """
        if not os.path.exists(path):
            return {"hard": [], "soft": []}

        hard_locks = []
        soft_conflicts = []
        path_norm = os.path.normpath(path).lower()
        
        # 1. 硬检测：通过重命名探测物理锁定 (这是最准确的占用依据)
        try:
            parent = os.path.dirname(path)
            temp_name = os.path.join(parent, f".lock_check_{os.getpid()}")
            os.rename(path, temp_name)
            os.rename(temp_name, path)
        except OSError:
            hard_locks.append("文件系统流锁定 (侦测到物理读写占用)")

        # 2. 精准关联探测：反查哪个进程的启动参数里带了这个路径
        # 使用 PowerShell 替代 wmic（更好的兼容性）
        try:
            # PowerShell 命令：获取所有进程的命令行参数
            ps_cmd = 'powershell -Command "Get-Process | Where-Object {$_.Path} | Select-Object Name, Id, Path, CommandLine | ConvertTo-Json"'
            output = subprocess.check_output(ps_cmd, shell=True, text=True, timeout=5)
            
            import json
            processes = json.loads(output) if output.strip() else []
            if not isinstance(processes, list):
                processes = [processes]
            
            for proc in processes:
                try:
                    # 获取进程信息
                    proc_name = proc.get('Name', '')
                    proc_path = proc.get('Path', '').lower()
                    proc_cmdline = proc.get('CommandLine', '').lower()
                    proc_id = proc.get('Id', 0)
                    
                    # 跳过自身进程
                    if proc_id == os.getpid():
                        continue
                    
                    # 检查命令行或路径中是否包含目标路径
                    if path_norm in proc_cmdline or path_norm in proc_path:
                        soft_conflicts.append(f"{proc_name} (关联路径持有者)")
                except Exception:
                    continue
                    
        except subprocess.TimeoutExpired:
            self.logger.warning("进程扫描超时")
        except Exception as e:
            self.logger.debug(f"进程扫描失败（不影响主流程）: {e}")

        return {
            "hard": hard_locks,
            "soft": soft_conflicts
        }

    def get_locking_processes(self, path: str) -> list[str]:
        """兼容性包装方法"""
        res = self.get_detailed_occupancy(path)
        return list(set(res["hard"] + res["soft"]))

    def is_locked(self, path: str) -> bool:
        """检查路径是否被锁定"""
        res = self.get_detailed_occupancy(path)
        return len(res["hard"]) > 0
