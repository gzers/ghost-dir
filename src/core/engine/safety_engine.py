"""
进程卫士
检测并处理文件占用问题
"""
import psutil
from typing import List, Tuple
from pathlib import Path


class SafetyEngine:
    """进程卫士引擎"""

    
    @staticmethod
    def scan_handles(path: str) -> List[Tuple[int, str]]:
        """
        扫描占用指定路径的进程
        
        Args:
            path: 要检查的路径
            
        Returns:
            进程列表 [(pid, process_name), ...]
        """
        processes = []
        target_path = Path(path).resolve()
        
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    # 检查进程打开的文件
                    for file in proc.open_files():
                        file_path = Path(file.path).resolve()
                        
                        # 检查是否是目标路径或其子路径
                        if file_path == target_path or target_path in file_path.parents:
                            processes.append((proc.info['pid'], proc.info['name']))
                            break
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
                    
        except Exception as e:
            print(f"扫描进程时出错: {e}")
        
        return processes
    
    @staticmethod
    def kill_process(pid: int) -> bool:
        """
        结束指定进程
        
        Args:
            pid: 进程 ID
            
        Returns:
            True 如果成功，否则 False
        """
        try:
            proc = psutil.Process(pid)
            proc.terminate()  # 先尝试优雅终止
            
            try:
                proc.wait(timeout=3)  # 等待 3 秒
            except psutil.TimeoutExpired:
                proc.kill()  # 强制结束
                
            return True
            
        except Exception as e:
            print(f"结束进程时出错: {e}")
            return False
    
    @staticmethod
    def kill_processes(processes: List[Tuple[int, str]]) -> int:
        """
        批量结束进程
        
        Args:
            processes: 进程列表 [(pid, name), ...]
            
        Returns:
            成功结束的进程数量
        """
        success_count = 0
        
        for pid, name in processes:
            if ProcessGuard.kill_process(pid):
                print(f"已结束进程: {name} (PID: {pid})")
                success_count += 1
            else:
                print(f"无法结束进程: {name} (PID: {pid})")
        
        return success_count
