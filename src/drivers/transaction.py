# coding: utf-8
"""事务管理驱动"""
import os
import json
from pathlib import Path
from src.common.config import DATA_DIR


LOCK_FILE = DATA_DIR / ".ghost.lock"


def check_crash_recovery() -> bool:
    """检查是否需要崩溃恢复"""
    return LOCK_FILE.exists()


def recover_from_crash():
    """从崩溃中恢复"""
    if LOCK_FILE.exists():
        try:
            with open(LOCK_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 这里可以添加恢复逻辑
            # 例如回滚未完成的操作
            
            LOCK_FILE.unlink()
        except Exception:
            pass


def start_transaction():
    """开始事务"""
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOCK_FILE, 'w', encoding='utf-8') as f:
        json.dump({'status': 'in_progress'}, f)


def commit_transaction():
    """提交事务"""
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()


def rollback_transaction():
    """回滚事务"""
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()
