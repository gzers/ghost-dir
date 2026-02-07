# coding: utf-8
"""智能扫描服务"""
import os
import re
from typing import List, Callable, Optional
from src.models.template import Template

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
            if os.path.exists(path):
                discovered.append(tpl)
                task['found'] = True
                continue

            # B. 注册表匹配 (模糊匹配名称)
            for reg_name, reg_loc in registry_paths.items():
                if tpl.name.lower() in reg_name.lower() and reg_loc and os.path.exists(reg_loc):
                    # 尝试拼接。有些注册表位置是根目录，需要补全子路径
                    # 比如 Steam 注册表是 D:\Steam，模板路径末尾是 steamapps
                    if tpl.id == "steam":
                        test_path = os.path.join(reg_loc, "steamapps")
                        if os.path.exists(test_path):
                            tpl.default_src = test_path
                            discovered.append(tpl)
                            task['found'] = True
                            break
                    
                    # 通用逻辑：如果是目录且存在，直接采纳
                    if os.path.exists(reg_loc):
                        tpl.default_src = reg_loc
                        discovered.append(tpl)
                        task['found'] = True
                        break

            if task['found']: continue

            # C. 深度探测逻辑：基于用户盘符探测最后两级特征路径
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
                        if os.path.exists(test_path):
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

    def import_templates(self, templates: List[Template]) -> int:
        """
        导入选中的模板
        将模板转换为 UserLink 对象并持久化到数据库中
        """
        if not self.link_service:
            print("ERROR: LinkService not configured for SmartScanner")
            return 0

        import uuid
        from src.models.link import UserLink, LinkStatus

        count = 0
        for tpl in templates:
            # 这里的 default_src 在扫描完成后可能是更新后的真实探测路径
            # default_target 默认为硬盘备份路径，如果为空，则使用一个合理的默认位置
            target = tpl.default_target or f"D:\\Ghost_Library\\{tpl.id}"
            
            # 创建 UserLink 对象
            link = UserLink(
                id=str(uuid.uuid4()).split('-')[0], # 生成短 ID
                name=tpl.name,
                source_path=tpl.default_src,
                target_path=target,
                category=tpl.category_id,
                status=LinkStatus.DISCONNECTED
            )
            
            # 写入数据库
            if self.link_service.add_link(link):
                count += 1
                
        return count
