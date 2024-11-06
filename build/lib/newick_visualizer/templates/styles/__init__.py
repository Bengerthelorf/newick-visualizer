"""CSS styles for the tree visualization"""

from pathlib import Path

def load_styles():
    """Load all CSS styles"""
    style_dir = Path(__file__).parent
    styles = []
    
    # 按顺序加载CSS文件
    css_files = ['main.css']
    
    for css_file in css_files:
        file_path = style_dir / css_file
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                styles.append(f.read())
    
    return '\n'.join(styles)

__all__ = ['load_styles']