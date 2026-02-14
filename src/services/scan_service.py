# coding: utf-8
"""智能扫描服务"""
import os
import re
from typing import List, Callable, Optional
from src.models.template import Template
from src.drivers.fs import get_real_path

class SmartScanner:
    """智能扫描引擎"""
    
    def __init__(self, templates: List[Template], link_service=None):
        self.templates = templates
        self.link_service = link_service
        self.progress_callback: Optional[Callable[[str], None]] = None

    def set_progress_callback(self, callback: Callable[[str], None]):
        """设置扫描进度回调"""
        self.progress_callback = callback

    def scan(self) -> List[Template]:
        """
        全量扫描本机应用
        使用三级探测机制：
        1. 默认路径检查
        2. 注册表安装信息探测
        3. 磁盘关键词深度匹配
        """
        discovered = []
        
        # 0. 预加载已导入的链接，用于扫描去重
        existing_srcs = set()
        if self.link_service:
            for l in self.link_service.get_all_links():
                # 统一标准化路径，处理大小写、反斜杠方向以及环境变量
                norm_src = os.path.normpath(os.path.expandvars(l.source_path)).lower()
                existing_srcs.add(norm_src)
        
        import winreg # 仅在 Windows 下执行
        
        # 1. 预解析环境变量后的模板
        template_tasks = []
        for t in self.templates:
            expanded = os.path.expandvars(t.default_src)
            template_tasks.append({'tpl': t, 'path': expanded, 'found': False})

        # 2. 获取注册表中的安装信息（用于辅助定位）
        # 格式: { "DisplayName": "InstallLocation" }
        registry_paths = self._get_registry_installations()

        # 3. 扫描逻辑
        for task in template_tasks:
            tpl = task['tpl']
            path = task['path']

            if self.progress_callback:
                self.progress_callback(f"正在分析: {tpl.name}")

            # A. 检查默认路径
            norm_path = os.path.normpath(path).lower()
            if os.path.exists(path) and norm_path not in existing_srcs:
                discovered.append(tpl)
                task['found'] = True
                continue

            # B. 注册表匹配 (模糊匹配名称)
            for reg_name, reg_loc in registry_paths.items():
                if tpl.name.lower() in reg_name.lower() and reg_loc and os.path.exists(reg_loc):
                    # 尝试拼接
                    target_path = reg_loc
                    if tpl.id == "steam":
                        target_path = os.path.join(reg_loc, "steamapps")
                    
                    norm_reg_path = os.path.normpath(target_path).lower()
                    if os.path.exists(target_path) and norm_reg_path not in existing_srcs:
                        tpl.default_src = target_path
                        discovered.append(tpl)
                        task['found'] = True
                        break

            if task['found']: continue

            # C. 深度探测逻辑
            path_parts = path.replace("\\", "/").rstrip("/").split("/")
            if len(path_parts) >= 2:
                feature = os.path.join(path_parts[-2], path_parts[-1])
                # 获取系统所有逻辑盘
                drives = [f"{d}:\\" for d in "CDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]
                
                # 常见软件安装根目录
                common_roots = ["", "Games", "Software", "Program Files", "Program Files (x86)"]
                
                for drive in drives:
                    for sub in common_roots:
                        test_path = os.path.join(drive, sub, feature)
                        norm_test_path = os.path.normpath(test_path).lower()
                        if os.path.exists(test_path) and norm_test_path not in existing_srcs:
                            tpl.default_src = test_path
                            discovered.append(tpl)
                            task['found'] = True
                            break
                    if task['found']: break

        return discovered

    def _get_registry_installations(self) -> dict:
        """从注册表获取已安装程序的列表"""
        results = {}
        import winreg
        keys = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall")
        ]
        
        for root_key, sub_key in keys:
            try:
                with winreg.OpenKey(root_key, sub_key) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, name) as sub:
                                display_name = winreg.QueryValueEx(sub, "DisplayName")[0]
                                install_loc = winreg.QueryValueEx(sub, "InstallLocation")[0]
                                if display_name and install_loc:
                                    results[display_name] = install_loc
                        except: continue
            except: continue
        return results

    def _get_real_link_target(self, path: str) -> Optional[str]:
        """[底层核心] 探测路径是否为链接，并返回其实际物理指向"""
        if not os.path.exists(path):
            return None
        resolved = get_real_path(path)
        if not resolved:
            return None
        # 解析结果与原始路径相同说明不是链接，返回 None
        norm_original = os.path.normpath(path)
        if os.path.normcase(resolved) == os.path.normcase(norm_original):
            return None
        return resolved

    def import_templates(self, templates: List[Template]) -> int:
        """
        [深度重构] 导入模板
        1. 动态自适应：识别本地已存在链接的真实指向
        2. 即时状态同步：导入成功后立即触发物理校验
        """
        if not self.link_service:
            print("ERROR: LinkService not configured for SmartScanner")
            return 0

        import uuid
        from src.models.link import UserLink, LinkStatus

        count = 0
        for tpl in templates:
            src = tpl.default_src
            
            # 核心改进：实测优先原则
            # 检查当前扫描到的源路径是否已经是一个链接
            real_target = self._get_real_link_target(src)
            
            if real_target:
                # [关键逻辑] 如果已建立链接，则以其实测指向作为导入的 target_path
                target = real_target
                initial_status = LinkStatus.CONNECTED # 初步标记为连接，后续会由 service 进行物理确认
            else:
                # 否则使用模板默认或库路径
                target = tpl.default_target or f"D:\\Ghost_Library\\{tpl.id}"
                initial_status = LinkStatus.DISCONNECTED

            # 创建 UserLink 对象
            link = UserLink(
                id=str(uuid.uuid4()).split('-')[0],
                name=tpl.name,
                source_path=src,
                target_path=target,
                category=tpl.category_id,
                status=initial_status
            )
            
            # 写入数据库
            if self.link_service.add_link(link):
                # [体验加固] 导入后立即触发一次物理状态确认，确保 UI 状态即刻更新
                self.link_service.refresh_link_status(link.id)
                count += 1
                
        return count
