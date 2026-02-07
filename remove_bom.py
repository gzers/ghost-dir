import os

def remove_bom(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
    
    if content.startswith(b'\xef\xbb\xbf'):
        print(f"检测并移除 BOM: {file_path}")
        with open(file_path, 'wb') as f:
            f.write(content[3:])
        return True
    return False

src_dir = r"d:\Users\15119\WorkSpace\Code\tool\ghost-dir\src"

count = 0
for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            if remove_bom(path):
                count += 1

print(f"\n清理完成，共处理了 {count} 个带 BOM 的文件。")
