"""Newick Tree Visualizer Package"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from _version import __version__

from .core.tree_generator import create_tree_html
from .core.template_manager import TemplateManager

__all__ = ['create_tree_html', 'TemplateManager', '__version__']