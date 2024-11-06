from typing import Dict, Any
import json
from pathlib import Path

from .utils import (
    clean_newick_string,
    validate_newick_format,
    validate_groups_structure,
    process_colors,
    validate_file_path,
    load_json_file,
    save_to_file
)
from .template_manager import TemplateManager

class TreeGenerator:
    """系统发生树可视化生成器"""
    
    def __init__(self, config: Dict[str, Any]):
        """初始化生成器
        
        Args:
            config: 配置字典，包含所有可视化参数
        """
        self.config = config
        self.template_manager = TemplateManager()

    def generate(self) -> str:
        """生成树的可视化HTML
        
        Returns:
            str: 生成的HTML内容
        """
        try:
            print("Reading Newick file...")
            newick_data = self._load_newick_file()
            print(f"Newick data length: {len(newick_data)}")
            
            print("Reading groups file...")
            groups_data = self._load_groups_file()
            print(f"Groups data: {json.dumps(groups_data, indent=2)}")
            
            print("Processing data...")
            processed_newick = self._process_newick_data(newick_data)
            processed_groups = self._process_groups_data(groups_data)
            
            print("Preparing render config...")
            render_config = self._prepare_render_config()
            print(f"Render config: {json.dumps(render_config, indent=2)}")
            
            print("Generating HTML...")
            html_content = self._generate_html(
                processed_newick,
                processed_groups,
                render_config
            )
            
            return html_content
            
        except Exception as e:
            print(f"Error in generate(): {str(e)}")
            raise

    def _load_newick_file(self) -> str:
        """加载并验证Newick文件
        
        Returns:
            str: Newick数据字符串
        """
        file_path = validate_file_path(self.config['input_file'])
        with open(file_path, 'r', encoding='utf-8') as f:
            data = f.read().strip()
        validate_newick_format(data)
        return data

    def _load_groups_file(self) -> Dict[str, Any]:
        """加载并验证分组文件
        
        Returns:
            Dict: 分组数据字典
        """
        groups_data = load_json_file(self.config['groups_file'])
        validate_groups_structure(groups_data)
        return groups_data

    def _process_newick_data(self, newick_data: str) -> str:
        """处理Newick数据
        
        Args:
            newick_data: 原始Newick字符串
            
        Returns:
            str: 处理后的Newick字符串
        """
        return clean_newick_string(newick_data)

    def _process_groups_data(self, groups_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理分组数据
        
        Args:
            groups_data: 原始分组数据
            
        Returns:
            Dict: 处理后的分组数据
        """
        # 深拷贝以避免修改原始数据
        processed_data = json.loads(json.dumps(groups_data))
        
        # 处理颜色
        process_colors(processed_data)
        
        # 确保布局配置存在
        if 'layout' not in processed_data:
            processed_data['layout'] = {}
        
        # 设置默认布局配置
        layout = processed_data['layout']
        layout.setdefault('direction', 'right')
        layout.setdefault('evenDistribution', True)
        
        if 'groupOrder' not in layout:
            layout['groupOrder'] = list(processed_data['groups'].keys())
        
        return processed_data

    def _prepare_render_config(self) -> Dict[str, Any]:
        """准备渲染配置
        
        Returns:
            Dict: 渲染配置字典
        """
        return {
            'padding': self.config['padding'],
            'opacity': self.config['opacity'],
            'points': self.config['points'],
            'distance_threshold': self.config['distance_threshold'],
            'show_confidence': self.config['show_confidence'],
            'font_size': self.config['font_size'],
            'font_family': self.config['font_family'],
            'font_weight': self.config['font_weight'],
            'min_branch_length': self.config['min_branch_length'],
            'max_branch_length': self.config['max_branch_length'],
            'default_length': self.config['default_length'],
            'link_color': self.config['link_color'],
            'link_width': self.config['link_width'],
        }

    def _generate_html(
        self,
        newick_data: str,
        groups_data: Dict[str, Any],
        render_config: Dict[str, Any]
    ) -> str:
        """生成HTML内容
        
        Args:
            newick_data: 处理后的Newick数据
            groups_data: 处理后的分组数据
            render_config: 渲染配置
            
        Returns:
            str: 生成的HTML内容
        """
        return self.template_manager.render_tree(
            config=render_config,
            groups=groups_data,
            newick=newick_data
        )

    def _save_output(self, content: str) -> None:
        """保存输出文件
        
        Args:
            content: HTML内容
        """
        save_to_file(content, self.config['output_file'])

def create_tree_html(**kwargs) -> None:
    """创建树的可视化HTML
    
    Args:
        **kwargs: 配置参数
    """
    try:
        # 添加调试输出
        print("Starting tree generation with config:", json.dumps(kwargs, indent=2))
        
        generator = TreeGenerator(kwargs)
        
        # 获取生成的HTML内容
        html_content = generator.generate()
        
        # 输出生成的HTML内容的前100个字符（用于调试）
        print("Generated HTML preview:", html_content[:100])
        
        # 检查输出文件
        output_file = kwargs.get('output_file', 'tree_visualization.html')
        print(f"Writing to file: {output_file}")
        
        # 保存文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print("Tree generation completed successfully")
        
    except Exception as e:
        print(f"Error during tree generation: {str(e)}")
        raise

# 如果直接运行此文件
if __name__ == '__main__':
    from .cli import parse_args
    
    # 获取命令行参数并生成可视化
    args = parse_args()
    create_tree_html(**args._asdict())