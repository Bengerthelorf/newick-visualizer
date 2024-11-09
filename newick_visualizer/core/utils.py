import re
import os
import json
from pathlib import Path
from typing import Dict, Any, List, Union, Optional
import base64
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def clean_newick_string(newick_str: str) -> str:
    """清理 Newick 字符串，移除不必要的空白字符
    
    Args:
        newick_str: Newick 格式的字符串
        
    Returns:
        str: 清理后的 Newick 字符串
    """
    # 保留括号、逗号、冒号、分号之间的空格，但移除其他多余的空白字符
    return re.sub(r'\s+', '', newick_str.strip())

def validate_newick_format(newick_str: str) -> bool:
    """验证 Newick 格式是否正确
    
    Args:
        newick_str: 要验证的 Newick 字符串
        
    Returns:
        bool: 格式是否有效
        
    Raises:
        ValueError: 如果格式无效，返回具体错误信息
    """
    # 基本格式检查
    if not newick_str.strip().endswith(';'):
        raise ValueError("Newick string must end with semicolon")
        
    # 括号匹配检查
    stack = []
    for char in newick_str:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                raise ValueError("Unmatched parentheses in Newick string")
            stack.pop()
            
    if stack:
        raise ValueError("Unclosed parentheses in Newick string")
    
    return True

def validate_groups_structure(groups_data: dict) -> bool:
    """验证组数据的JSON结构
    
    Args:
        groups_data: 包含组信息的字典
        
    Returns:
        bool: 验证是否通过
        
    Raises:
        ValueError: 如果数据结构无效
    """
    if not isinstance(groups_data, dict):
        raise ValueError("Groups data must be a dictionary")
        
    if 'groups' not in groups_data:
        raise ValueError("Missing 'groups' key in data")
        
    if not isinstance(groups_data['groups'], dict):
        raise ValueError("'groups' must be a dictionary")

    # 验证布局配置
    if 'layout' in groups_data:
        if not isinstance(groups_data['layout'], dict):
            raise ValueError("'layout' must be a dictionary")
            
        layout = groups_data['layout']
        if 'direction' in layout and layout['direction'] not in ['right', 'left', 'up', 'down']:
            raise ValueError("'direction' must be one of: right, left, up, down")
            
        if 'groupOrder' in layout and not isinstance(layout['groupOrder'], list):
            raise ValueError("'groupOrder' must be a list")
            
        if 'evenDistribution' in layout and not isinstance(layout['evenDistribution'], bool):
            raise ValueError("'evenDistribution' must be a boolean")
    
    # 验证每个组的结构
    for group_name, group in groups_data['groups'].items():
        if not isinstance(group, dict):
            raise ValueError(f"Group '{group_name}' must be a dictionary")
            
        if 'color' not in group:
            raise ValueError(f"Missing 'color' in group '{group_name}'")
            
        if 'members' not in group:
            raise ValueError(f"Missing 'members' in group '{group_name}'")
            
        if not isinstance(group['members'], list):
            raise ValueError(f"'members' in group '{group_name}' must be a list")
        
        # 验证成员排序（如果存在）
        if 'order' in group:
            if not isinstance(group['order'], list):
                raise ValueError(f"'order' in group '{group_name}' must be a list")
            
            # 确保所有成员都在排序列表中
            members_set = set(group['members'])
            order_set = set(group['order'])
            
            if not order_set.issubset(members_set):
                raise ValueError(f"'order' in group '{group_name}' contains invalid members")
            
            if len(order_set) != len(group['members']):
                raise ValueError(f"'order' in group '{group_name}' must contain all members")
    
    return True

def process_colors(groups_data: Dict[str, Any]) -> None:
    """处理和加深颜色
    
    Args:
        groups_data: 包含组信息的字典
    """
    def darken_color(color: str, amount: int = 40) -> str:
        """使颜色更深
        
        Args:
            color: 十六进制颜色字符串 (e.g., '#RRGGBB')
            amount: 减少的亮度值
        """
        if not color.startswith('#'):
            return color
            
        r = max(0, int(color[1:3], 16) - amount)
        g = max(0, int(color[3:5], 16) - amount)
        b = max(0, int(color[5:7], 16) - amount)
        return f'#{r:02x}{g:02x}{b:02x}'

    # 处理每个组的颜色
    for group in groups_data['groups'].values():
        group['color'] = darken_color(group['color'])

def validate_file_path(file_path: str, should_exist: bool = True) -> str:
    """验证文件路径
    
    Args:
        file_path: 要验证的文件路径
        should_exist: 是否应该已经存在
        
    Returns:
        str: 验证后的文件路径
        
    Raises:
        ValueError: 如果路径无效
    """
    try:
        # 规范化路径，处理跨平台差异
        path = Path(file_path).resolve()
        
        if should_exist and not path.exists():
            raise ValueError(f"File does not exist: {path}")
            
        if not should_exist:
            # 检查父目录是否存在且可写
            parent = path.parent
            if not parent.exists():
                raise ValueError(f"Directory does not exist: {parent}")
            if not os.access(str(parent), os.W_OK):  # 使用 str() 确保 Windows 兼容性
                raise ValueError(f"Directory is not writable: {parent}")
        
        return str(path)  # 返回规范化的路径字符串
        
    except Exception as e:
        # 提供更详细的错误信息
        raise ValueError(f"Invalid file path '{file_path}': {str(e)}")

def ensure_directory_exists(directory: Union[str, Path]) -> None:
    """确保目录存在，如果不存在则创建
    
    Args:
        directory: 目录路径
    """
    Path(directory).mkdir(parents=True, exist_ok=True)

def load_json_file(file_path: str) -> Dict[str, Any]:
    """加载并验证JSON文件
    
    Args:
        file_path: JSON文件路径
        
    Returns:
        Dict: 加载的JSON数据
        
    Raises:
        ValueError: 如果文件不存在或JSON格式无效
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in {file_path}: {str(e)}")

def get_file_type(file_path: str) -> str:
    """根据文件扩展名确定输出类型
    
    Args:
        file_path: 文件路径
        
    Returns:
        str: 文件类型 ('html', 'png', 'jpg', 'pdf')
    """
    ext = Path(file_path).suffix.lower()
    if ext in ['.jpg', '.jpeg']:
        return 'jpg'
    elif ext in ['.png']:
        return 'png'
    elif ext in ['.pdf']:
        return 'pdf'
    else:
        return 'html'

def export_visualization(html_content: str, output_path: str, output_type: str = None, render_delay: int = 2000) -> None:
    """导出可视化结果为不同格式
    
    Args:
        html_content: HTML内容
        output_path: 输出文件路径
        output_type: 输出类型 ('html', 'png', 'jpg', 'pdf')
        render_delay: 渲染延迟（毫秒）
    """
    if output_type is None:
        output_type = get_file_type(output_path)

    # HTML格式直接输出，不需要修改内容和等待渲染
    if output_type == 'html':
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Successfully created HTML: {output_path}")
        return

    # 对于其他格式，创建临时HTML文件用于转换
    temp_html = f"temp_{int(time.time())}.html"
    try:
        with open(temp_html, "w", encoding="utf-8") as f:
            # 隐藏 controls-container
            cleaned_content = html_content.replace(
                '<div id="controls-container">', 
                '<div id="controls-container" style="display: none;">')
            f.write(cleaned_content)

            # 使用Chrome headless模式进行转换
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--window-size=1920,1080')

            driver = webdriver.Chrome(options=chrome_options)
            try:
                # 加载HTML
                driver.get(f'file://{os.path.abspath(temp_html)}')
                
                # 等待渲染完成
                print(f"Waiting {render_delay}ms for rendering...")
                time.sleep(render_delay / 1000)  # 转换为秒
                
                if output_type in ['png', 'jpg']:
                    # 等待树容器出现并可见
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located(("id", "tree-container"))
                    )
                    
                    # 截图
                    driver.save_screenshot(output_path)
                    print(f"Successfully created image: {output_path}")
                    
                elif output_type == 'pdf':
                    # PDF打印设置
                    print_options = {
                        'landscape': True,
                        'paperWidth': 11.7,  # A4宽度（英寸）
                        'paperHeight': 8.3,  # A4高度（英寸）
                        'marginTop': 0,
                        'marginBottom': 0,
                        'marginLeft': 0,
                        'marginRight': 0,
                        'printBackground': True
                    }
                    
                    # 生成PDF
                    result = driver.execute_cdp_cmd('Page.printToPDF', print_options)
                    with open(output_path, 'wb') as f:
                        f.write(base64.b64decode(result['data']))
                    print(f"Successfully created PDF: {output_path}")
                    
            finally:
                driver.quit()
                
    finally:
        # 清理临时文件
        if os.path.exists(temp_html):
            os.remove(temp_html)

def save_to_file(content: str, file_path: str, mode: str = 'w') -> None:
    """保存内容到文件
    
    Args:
        content: 要保存的内容
        file_path: 目标文件路径
        mode: 文件打开模式
    """
    with open(file_path, mode, encoding='utf-8') as f:
        f.write(content)

# 导出所有工具函数
__all__ = [
    'clean_newick_string',
    'validate_newick_format',
    'validate_groups_structure',
    'process_colors',
    'validate_file_path',
    'ensure_directory_exists',
    'load_json_file',
    'save_to_file',
    'get_file_type',
    'export_visualization'
]