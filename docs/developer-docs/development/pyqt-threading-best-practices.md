# PyQt/PySide 多线程开发最佳实践

- 适用版本: `>=1.0.0`
- 文档状态: `active`
- 最后更新: `2026-02-10`

## 概述

本文档总结了在 Ghost-Dir 项目中使用 PyQt/PySide 进行多线程开发时遇到的问题和最佳实践，旨在避免常见的线程安全陷阱。

## 核心原则

### 1. 避免在工作线程中访问 QObject 实例属性

**问题**：在 `ThreadPoolExecutor` 或 `QThread` 中直接访问 `QObject` 的实例属性（如 `self.is_aborted`）可能导致死锁或不可预测的行为。

**原因**：PyQt/PySide 的元对象系统（Meta-Object System）在多线程环境中访问属性时可能涉及 GIL 竞争或内部锁机制。

**错误示例**：
```python
class ServiceWorker(QObject):
    def __init__(self):
        super().__init__()
        self.is_aborted = False
    
    def detect_status(self, link_ids):
        def _get_status(lid):
            # ❌ 错误：在线程池中访问 self.is_aborted
            if self.is_aborted:
                return None
            # ❌ 错误：在线程池中调用实例方法
            return self._check_single_link(lid)
        
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(_get_status, lid) for lid in link_ids]
```

**正确示例**：
```python
class ServiceWorker(QObject):
    def __init__(self):
        super().__init__()
        self.is_aborted = False
    
    def detect_status(self, link_ids):
        # ✅ 正确：缓存到本地变量
        aborted = self.is_aborted
        
        def _get_status(lid):
            # ✅ 正确：使用本地变量
            if aborted:
                return None
            # ✅ 正确：调用静态方法
            return ServiceWorker._check_single_link(lid)
        
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(_get_status, lid) for lid in link_ids]
    
    @staticmethod
    def _check_single_link(lid):
        # 纯函数，不依赖实例状态
        pass
```

### 2. 重置状态标志

**问题**：状态标志（如 `is_aborted`）在操作完成后未重置，导致后续操作立即失败。

**错误示例**：
```python
def detect_status(self, link_ids):
    # ❌ 错误：未重置 is_aborted
    aborted = self.is_aborted  # 如果上次操作设置为 True，这次也会是 True
    
    with ThreadPoolExecutor() as executor:
        for future in as_completed(futures):
            if aborted:  # 立即退出！
                break
```

**正确示例**：
```python
def detect_status(self, link_ids):
    # ✅ 正确：每次操作开始时重置状态
    self.is_aborted = False
    aborted = self.is_aborted
    
    with ThreadPoolExecutor() as executor:
        for future in as_completed(futures):
            if aborted:
                break
```

### 3. 将实例方法改为静态方法

**问题**：在多线程环境中调用实例方法会隐式访问 `self`，可能导致线程安全问题。

**解决方案**：
- 将不依赖实例状态的方法改为 `@staticmethod`
- 如果需要访问实例数据，通过参数显式传递

**示例**：
```python
class ServiceWorker(QObject):
    # ❌ 错误：实例方法
    def _check_single_link(self, link):
        return link.status
    
    # ✅ 正确：静态方法
    @staticmethod
    def _check_single_link(link):
        return link.status
```

### 4. 使用本地变量缓存共享数据

**原则**：在启动线程池之前，将所有需要的共享数据缓存到本地变量中。

**示例**：
```python
def detect_status(self, link_ids, dao):
    # ✅ 缓存所有需要的数据
    self.is_aborted = False
    aborted = self.is_aborted
    all_links = dao.get_all()
    link_map = {l.id: l for l in all_links}
    
    def _get_status(lid):
        # 只使用本地变量和参数
        if aborted:
            return None
        link = link_map.get(lid)
        return ServiceWorker._check_single_link(link)
    
    with ThreadPoolExecutor() as executor:
        # ...
```

## 调试技巧

### 1. 添加详细日志

在多线程代码中添加详细的调试日志，帮助追踪执行流程：

```python
def _get_status(lid):
    print(f"[DEBUG] _get_status called for {lid}")
    print(f"[DEBUG] Checking aborted flag")
    if aborted:
        print(f"[DEBUG] Aborted, returning None")
        return None
    print(f"[DEBUG] Processing {lid}")
    result = process(lid)
    print(f"[DEBUG] Returning result: {result}")
    return result
```

### 2. 捕获并记录异常

在 `as_completed` 循环中捕获异常，避免静默失败：

```python
for future in as_completed(futures):
    try:
        result = future.result()
        process(result)
    except Exception as e:
        print(f"[ERROR] Task failed: {e}")
        import traceback
        traceback.print_exc()
```

### 3. 检查线程池任务完成情况

确认所有提交的任务都被处理：

```python
print(f"[DEBUG] Submitted {len(futures)} tasks")
processed = 0
for future in as_completed(futures):
    processed += 1
    # ...
print(f"[DEBUG] Processed {processed}/{len(futures)} tasks")
```

## 常见陷阱

### 陷阱 1：闭包捕获可变对象

```python
# ❌ 错误
results = []
for item in items:
    executor.submit(lambda: results.append(process(item)))  # 竞态条件！

# ✅ 正确
def process_and_store(item, results_dict, item_id):
    results_dict[item_id] = process(item)

results = {}
for i, item in enumerate(items):
    executor.submit(process_and_store, item, results, i)
```

### 陷阱 2：在主循环中访问实例属性

```python
# ❌ 错误
for future in as_completed(futures):
    if self.is_aborted:  # 可能导致问题
        break

# ✅ 正确
aborted = self.is_aborted
for future in as_completed(futures):
    if aborted:
        break
```

### 陷阱 3：忘记重置状态

```python
# ❌ 错误
def start_operation(self):
    # self.is_running 可能已经是 True
    if self.is_running:
        return
    # ...

# ✅ 正确
def start_operation(self):
    self.is_running = False  # 显式重置
    if self.is_running:
        return
    self.is_running = True
    # ...
```

## 检查清单

在编写 PyQt 多线程代码时，请检查以下项目：

- [ ] 工作线程中不访问 `self` 的任何属性
- [ ] 实例方法改为静态方法或通过参数传递数据
- [ ] 在操作开始时重置所有状态标志
- [ ] 共享数据缓存到本地变量
- [ ] 添加详细的调试日志
- [ ] 异常处理覆盖所有线程池任务
- [ ] 验证所有任务都被正确处理

## 参考案例

本文档基于 Ghost-Dir 项目中 `ServiceWorker.detect_status` 方法的调试经验总结。详见：
- 文件：`src/services/link_service.py`
- 提交：修复状态检测线程安全问题
- 问题：线程池卡死、状态标志未重置

## 相关资源

- [Qt 文档：线程基础](https://doc.qt.io/qt-6/thread-basics.html)
- [Python concurrent.futures 文档](https://docs.python.org/3/library/concurrent.futures.html)
- [PyQt 线程安全指南](https://www.riverbankcomputing.com/static/Docs/PyQt6/signals_slots.html#thread-safety)
