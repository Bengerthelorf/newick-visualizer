import json
from pathlib import Path
from typing import Dict, Any

class TemplateManager:
    def __init__(self):
        # 使用包的根目录
        self.template_dir = Path(__file__).parent.parent / 'templates'
        
    def render_tree(self, config: Dict[str, Any], groups: Dict[str, Any], newick: str) -> str:
        """渲染完整的HTML"""
        try:
            # 读取基础模板
            with open(self.template_dir / 'base.html', 'r', encoding='utf-8') as f:
                template = f.read()
                
            # 读取所有JavaScript文件
            scripts_dir = self.template_dir / 'scripts'
            all_scripts = []
            for js_file in ['layout.js', 'tree.js', 'groups.js', 'main.js']:
                with open(scripts_dir / js_file, 'r', encoding='utf-8') as f:
                    all_scripts.append(f.read())
            script_content = '\n'.join(all_scripts)

            # 读取样式文件
            with open(self.template_dir / 'styles' / 'main.css', 'r', encoding='utf-8') as f:
                style_content = f.read()

            # 确保配置为字符串格式
            js_config = {
                "padding": config['padding'],
                "opacity": config['opacity'],
                "pointsPerNode": config['points'],
                "distanceThreshold": config['distance_threshold'],
                "showConfidence": bool(config['show_confidence']),
                "fontSize": config['font_size'],
                "fontFamily": config['font_family'],
                "fontWeight": config['font_weight'],
                "branchLength": {
                    "min": float(config['min_branch_length']),
                    "max": float(config['max_branch_length']),
                    "default": float(config['default_length'])
                },
                "linkColor": config['link_color'],
                "linkWidth": float(config['link_width'])
            }

            # 替换内容
            template = template.replace('STYLE_CONTENT', style_content)
            template = template.replace('CONFIG_CONTENT', json.dumps(js_config, indent=2))
            template = template.replace('GROUP_CONTENT', json.dumps(groups, indent=2))
            template = template.replace('NEWICK_CONTENT', f'`{newick}`')
            template = template.replace('SCRIPT_CONTENT', script_content)

            return template
            
        except Exception as e:
            import traceback
            print(f"Error details: {traceback.format_exc()}")
            raise ValueError(f"Failed to render template: {str(e)}")
            
    def get_template_dir(self) -> Path:
        """获取模板目录路径"""
        return self.template_dir