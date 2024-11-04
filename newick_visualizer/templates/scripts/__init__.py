"""JavaScript scripts for the tree visualization"""

from pathlib import Path

def load_scripts():
    """Load all JavaScript scripts"""
    script_dir = Path(__file__).parent
    scripts = []
    
    # 按顺序加载JS文件
    js_files = ['tree.js', 'layout.js', 'groups.js', 'main.js']
    
    for js_file in js_files:
        file_path = script_dir / js_file
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                scripts.append(f.read())
    
    return '\n'.join(scripts)

__all__ = ['load_scripts']