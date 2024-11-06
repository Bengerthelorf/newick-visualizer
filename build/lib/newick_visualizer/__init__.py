"""Newick Tree Visualizer Package"""

from ._version import __version__
from .core.tree_generator import create_tree_html
from .core.template_manager import TemplateManager

__all__ = ['create_tree_html', 'TemplateManager', '__version__']