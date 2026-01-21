"""
Build script for Ghost-Dir using PyInstaller
"""
import os
import sys
import subprocess

def build():
    """Build the executable"""
    # Get project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Paths
    main_script = os.path.join(project_root, 'run.py')
    icon_path = os.path.join(project_root, 'assets', 'icon.ico')
    src_dir = os.path.join(project_root, 'src')
    
    # Check if icon exists
    if not os.path.exists(icon_path):
        print(f"✗ Error: Icon file not found at {icon_path}")
        print("  Please run 'python scripts/convert_icon.py' first to create the ICO file.")
        return False
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--name=Ghost-Dir',
        '--windowed',  # No console window
        f'--icon={icon_path}',
        '--onefile',  # Single executable
        '--clean',
        '--uac-admin=false',  # Disable admin privilege requirement
        # Add source directory to path
        f'--paths={src_dir}',
        # Add data files
        '--add-data', f'{os.path.join(project_root, "assets")}{os.pathsep}assets',
        '--add-data', f'{os.path.join(project_root, "config")}{os.pathsep}config',
        # Hidden imports for PyQt-Fluent-Widgets
        '--hidden-import=qfluentwidgets',
        '--hidden-import=PyQt6',
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtWidgets',
        main_script
    ]
    
    print("Building Ghost-Dir executable...")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    # Run PyInstaller
    result = subprocess.run(cmd, cwd=project_root)
    
    if result.returncode == 0:
        print("\n✓ Build successful!")
        print(f"  Executable: {os.path.join(project_root, 'dist', 'Ghost-Dir.exe')}")
        return True
    else:
        print("\n✗ Build failed!")
        return False

if __name__ == '__main__':
    success = build()
    sys.exit(0 if success else 1)
