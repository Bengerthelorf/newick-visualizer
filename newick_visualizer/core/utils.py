import re
import os
import json
from pathlib import Path
from typing import Dict, Any, List, Union, Optional

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
    path = Path(file_path)
    
    if should_exist and not path.exists():
        raise ValueError(f"File does not exist: {file_path}")
        
    if not should_exist:
        # 检查父目录是否存在且可写
        parent = path.parent
        if not parent.exists():
            raise ValueError(f"Directory does not exist: {parent}")
        if not os.access(parent, os.W_OK):
            raise ValueError(f"Directory is not writable: {parent}")
    
    return str(path)

def get_file_extension(file_path: str) -> str:
    """获取文件扩展名
    
    Args:
        file_path: 文件路径
        
    Returns:
        str: 文件扩展名（小写）
    """
    return Path(file_path).suffix.lower()

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
    'get_file_extension',
    'ensure_directory_exists',
    'load_json_file',
    'save_to_file'
]