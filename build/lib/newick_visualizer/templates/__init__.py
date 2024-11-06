"""Template management for tree visualization"""

from pathlib import Path

def load_styles() -> str:
    """Load all CSS styles"""
    style_dir = Path(__file__).parent / 'styles'
    styles = []
    
    # 按顺序加载CSS文件
    css_files = ['main.css']
    
    for css_file in css_files:
        file_path = style_dir / css_file
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                styles.append(f.read())
    
    return '\n'.join(styles)

def load_scripts() -> str:
    """Load all JavaScript scripts"""
    script_dir = Path(__file__).parent / 'scripts'
    scripts = []
    
    # 按顺序加载JS文件
    js_files = ['tree.js', 'layout.js', 'groups.js', 'main.js']
    
    for js_file in js_files:
        file_path = script_dir / js_file
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                scripts.append(f.read())
    
    return '\n'.join(scripts)

def get_base_template() -> str:
    """Get the base HTML template"""
    template_path = Path(__file__).parent / 'base.html'
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

__all__ = ['get_base_template', 'load_styles', 'load_scripts']