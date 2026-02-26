# coding: utf-8
"""
USN Journal 驱动 - 通过 NTFS MFT 枚举快速发现磁盘上所有 Reparse Point（Junction/Symlink）
仅适用于 Windows NTFS 卷，需要管理员权限。
"""
import os
import ctypes
import ctypes.wintypes as wintypes
import struct
from typing import List, Dict, Optional, Tuple

# ===== Windows API 常量 =====
GENERIC_READ = 0x80000000
FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002
OPEN_EXISTING = 3
FSCTL_ENUM_USN_DATA = 0x000900B3
FILE_ATTRIBUTE_REPARSE_POINT = 0x0400
FILE_ATTRIBUTE_DIRECTORY = 0x0010
FILE_ATTRIBUTE_HIDDEN = 0x0002
FILE_ATTRIBUTE_SYSTEM = 0x0004

# USN_RECORD_V2 头部固定字段大小（到 FileName 之前）
USN_RECORD_HEADER_SIZE = 60

# ===== 声明 Windows API 函数签名（关键：确保 64 位兼容） =====
kernel32 = ctypes.windll.kernel32

# CreateFileW 返回 HANDLE（指针类型），必须声明为 c_void_p
kernel32.CreateFileW.restype = ctypes.c_void_p
kernel32.CreateFileW.argtypes = [
    ctypes.c_wchar_p,  # lpFileName
    wintypes.DWORD,    # dwDesiredAccess
    wintypes.DWORD,    # dwShareMode
    ctypes.c_void_p,   # lpSecurityAttributes
    wintypes.DWORD,    # dwCreationDisposition
    wintypes.DWORD,    # dwFlagsAndAttributes
    ctypes.c_void_p,   # hTemplateFile
]

# DeviceIoControl 的 hDevice 也是 HANDLE
kernel32.DeviceIoControl.restype = wintypes.BOOL
kernel32.DeviceIoControl.argtypes = [
    ctypes.c_void_p,        # hDevice
    wintypes.DWORD,         # dwIoControlCode
    ctypes.c_void_p,        # lpInBuffer
    wintypes.DWORD,         # nInBufferSize
    ctypes.c_void_p,        # lpOutBuffer
    wintypes.DWORD,         # nOutBufferSize
    ctypes.POINTER(wintypes.DWORD),  # lpBytesReturned
    ctypes.c_void_p,        # lpOverlapped
]

kernel32.CloseHandle.restype = wintypes.BOOL
kernel32.CloseHandle.argtypes = [ctypes.c_void_p]

# INVALID_HANDLE_VALUE 在 64 位下为 0xFFFFFFFFFFFFFFFF
INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value


def _open_volume(drive_letter: str) -> Optional[int]:
    """打开卷句柄（需要管理员权限）"""
    volume_path = f"\\\\.\\{drive_letter}:"
    handle = kernel32.CreateFileW(
        volume_path,
        GENERIC_READ,
        FILE_SHARE_READ | FILE_SHARE_WRITE,
        None,
        OPEN_EXISTING,
        0,
        None,
    )
    if handle is None or handle == INVALID_HANDLE_VALUE:
        return None
    return handle


def _close_handle(handle: int):
    """关闭句柄"""
    kernel32.CloseHandle(handle)


def scan_reparse_points(drive_letter: str) -> List[Dict]:
    """
    通过 USN Journal 枚举 MFT，扫描指定卷上所有 Reparse Point 目录

    Args:
        drive_letter: 盘符，如 'C'

    Returns:
        [{"path": "C:\\Games\\SomeGame", "name": "SomeGame"}, ...]
        权限不足或发生错误时返回空列表
    """
    handle = _open_volume(drive_letter)
    if handle is None:
        return []

    try:
        # {FileReferenceNumber(低48位): (ParentRef, FileName, Attributes)}
        mft_records: Dict[int, Tuple[int, str, int]] = {}
        reparse_refs: List[int] = []

        # 64KB 缓冲区，提升单次 IO 效率
        buf_size = 65536
        buf = ctypes.create_string_buffer(buf_size)
        bytes_returned = wintypes.DWORD(0)

        # MFT_ENUM_DATA_V0: StartFileReferenceNumber(Q) + LowUsn(q) + HighUsn(Q)
        mft_enum_data = struct.pack('<QqQ', 0, 0, 0x7FFFFFFFFFFFFFFF)
        mft_enum_buf = ctypes.create_string_buffer(mft_enum_data)

        while True:
            result = kernel32.DeviceIoControl(
                handle,
                FSCTL_ENUM_USN_DATA,
                mft_enum_buf,
                len(mft_enum_buf),
                buf,
                buf_size,
                ctypes.byref(bytes_returned),
                None,
            )

            if not result:
                break

            returned = bytes_returned.value
            if returned <= 8:
                break

            # 前 8 字节是下一次枚举的 StartFileReferenceNumber
            next_start = struct.unpack_from('<Q', buf.raw, 0)[0]
            offset = 8

            while offset < returned:
                if offset + USN_RECORD_HEADER_SIZE > returned:
                    break

                # 解析 USN_RECORD_V2 头部字段
                (
                    record_length,
                    major_version,
                    minor_version,
                    file_ref,
                    parent_ref,
                    usn,
                    timestamp,
                    reason,
                    source_info,
                    security_id,
                    file_attributes,
                    file_name_length,
                    file_name_offset,
                ) = struct.unpack_from('<IHHQQQQIIIIHH', buf.raw, offset)

                if record_length == 0:
                    break

                # 提取文件名（UTF-16LE 编码）
                name_start = offset + file_name_offset
                name_end = name_start + file_name_length
                if name_end <= returned:
                    try:
                        file_name = buf.raw[name_start:name_end].decode('utf-16-le')
                    except UnicodeDecodeError:
                        file_name = ""

                    # 用低 48 位作为键（高 16 位是序列号，会变化）
                    ref_key = file_ref & 0x0000FFFFFFFFFFFF
                    parent_key = parent_ref & 0x0000FFFFFFFFFFFF

                    mft_records[ref_key] = (parent_key, file_name, file_attributes)

                    # 筛选：目录 + Reparse Point = Junction 或 Directory Symlink
                    # 排除 HIDDEN+SYSTEM 的系统兼容链接（如 Content.IE5、All Users 等）
                    is_reparse_dir = (file_attributes & FILE_ATTRIBUTE_DIRECTORY) and \
                                     (file_attributes & FILE_ATTRIBUTE_REPARSE_POINT)
                    is_system_compat = (file_attributes & FILE_ATTRIBUTE_HIDDEN) and \
                                       (file_attributes & FILE_ATTRIBUTE_SYSTEM)
                    if is_reparse_dir and not is_system_compat:
                        reparse_refs.append(ref_key)

                offset += record_length

            # 更新起始位置，继续枚举
            mft_enum_buf = ctypes.create_string_buffer(
                struct.pack('<QqQ', next_start, 0, 0x7FFFFFFFFFFFFFFF)
            )

        # 重建完整路径
        results = []
        drive_root = f"{drive_letter}:\\"

        for ref in reparse_refs:
            path = _build_path(ref, mft_records, drive_root)
            if path:
                name = os.path.basename(path)
                results.append({"path": path, "name": name})

        return results

    except Exception as e:
        print(f"[USN] 扫描 {drive_letter}: 卷时发生异常: {e}")
        return []
    finally:
        _close_handle(handle)


def _build_path(ref: int, mft_records: Dict, drive_root: str, max_depth: int = 64) -> Optional[str]:
    """通过 ParentFileReferenceNumber 链反向拼接完整路径"""
    parts = []
    current = ref
    visited = set()

    for _ in range(max_depth):
        if current in visited:
            break
        visited.add(current)

        record = mft_records.get(current)
        if record is None:
            break

        parent_ref, name, _ = record

        # MFT 条目 5 是卷根目录（不加入路径）
        if current == 5:
            break

        if name in ('.', '..', ''):
            break

        parts.append(name)
        current = parent_ref

    if not parts:
        return None

    parts.reverse()
    return os.path.join(drive_root, *parts)


def is_usn_available(drive_letter: str = 'C') -> bool:
    """检测 USN Journal 是否可用（管理员权限能否打开卷句柄）"""
    handle = _open_volume(drive_letter)
    if handle is None:
        return False
    _close_handle(handle)
    return True
