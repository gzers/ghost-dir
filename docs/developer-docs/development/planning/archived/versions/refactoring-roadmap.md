# Ghost-Dir QFluentWidgets Refactoring Roadmap

- 适用版本: `历史归档`
- 文档状态: `archived`
- 最后更新: `2026-02-10`

This plan outlines the steps to refactor the Ghost-Dir project to be 100% compliant with the official `QFluentWidgets` standards, eliminating "dirty code" and manual QSS hacks.

## Phase 1: 地基与入口 (Infrastructure)
**Objective:** Standardize application initialization and global theme management.

### Checklist
- [ ] **RHI Backend:** Retain `os.environ["QSG_RHI_BACKEND"] = "d3d12"` in `src/main.py` for Windows stability.
- [ ] **Theme Management:** Replace manual theme detection with `setTheme(Theme.AUTO)`.
- [ ] **Font Normalization:** Implement `setFontFamilies(['Segoe UI', 'Microsoft YaHei', 'PingFang SC'])` in `app.py`.
- [ ] **High DPI Scaling:** Ensure standard high DPI attributes are set.
- [ ] **App Info:** Standardize `setApplicationName` and `setApplicationVersion`.

### Key Files
- `src/main.py`
- `src/gui/app.py`

---

## Phase 2: 骨架与导航 (Shell & Navigation)
**Objective:** Leverage `FluentWindow`'s built-in capabilities to handle structure and effects.

### Checklist
- [ ] **Inheritance:** Ensure `MainWindow` inherits from `FluentWindow`.
- [ ] **Navigation:** Use `addSubInterface()` for all views, providing unique `objectName` for each.
- [ ] **Mica Effect:** Remove manual transparency QSS; use `FluentWindow`'s native Mica support.
- [ ] **Effect Sync:** Ensure `windowEffect.setMicaEffect` is handled during theme transitions if necessary.
- [ ] **Clean Layout:** Remove manual `apply_transparent_style` calls on navigation components.

### Key Files
- `src/gui/windows/main_window.py`

---

## Phase 3: 页面组件标准化 (Page & Components)
**Objective:** Replace all native Qt widgets with their Fluent counterparts.

### Checklist
- [ ] **Button Replacement:** 
    - `QPushButton` -> `PushButton` / `PrimaryPushButton` / `TransparentPushButton`
- [ ] **Label Replacement:** 
    - `QLabel` -> `TitleLabel` / `SubtitleLabel` / `BodyLabel` / `CaptionLabel`
- [ ] **Input Replacement:** 
    - `QLineEdit` -> `LineEdit` / `SearchLineEdit`
- [ ] **Icon Normalization:** 
    - Replace string paths with `FluentIcon` enum (e.g., `FluentIcon.HOME`).
    - Use `FluentIconBase.qicon()` for components only supporting `QIcon`.
- [ ] **Style Removal:** 
    - **CRITICAL:** Delete all manual `setStyleSheet` calls.
    - Use `setCustomStyleSheet(widget, lightQss, darkQss)` for minor tweaks only.

### Key Files
- `src/gui/views/*.py`
- `src/gui/views/*/widgets/*.py`

---

## Phase 4: 交互与反馈 (Interaction)
**Objective:** Modernize user feedback mechanisms.

### Checklist
- [ ] **Dialog Replacement:** 
    - `QMessageBox` -> `MessageDialog` (for blocking decisions).
    - `QMessageBox` tips -> `InfoBar` (for non-blocking feedback).
- [ ] **Progress Indicators:** 
    - Use `IndeterminateProgressBar` for background tasks or loading states.
- [ ] **Transition Effects:** 
    - Ensure smooth transitions between views using `FluentWindow`'s internal `StackedWidget`.

### Key Files
- Global logic across `src/gui/`

---

Master, shall we start with Phase 1?
