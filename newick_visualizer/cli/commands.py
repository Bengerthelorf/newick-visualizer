import click
from pathlib import Path
from .. import __version__
from ..core.tree_generator import create_tree_html
from ..core.utils import validate_file_path

class FontWeightChoice(click.Choice):
    def get_metavar(self, param):
        return "WEIGHT"

CONTEXT_SETTINGS = {
    'help_option_names': ['-h', '--help'],
    'max_content_width': 100
}

@click.command(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__, prog_name="Newick Visualizer")
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('groups_file', type=click.Path(exists=True))
@click.option('--output', '-o', 
              default='tree_visualization.html',
              show_default=True,
              help='Output HTML file path.')
# 视觉相关选项
@click.option('--padding', 
              default=35,
              show_default=True,
              type=int, 
              help='Padding around nodes in pixels.')
@click.option('--opacity', 
              default=0.3,
              show_default=True,
              type=float,
              help='Opacity of group backgrounds (0-1).')
@click.option('--points', 
              default=12,
              show_default=True,
              type=click.IntRange(6, 24),
              help='Number of points to generate around each node for group background.')
@click.option('--distance-threshold', 
              default=1.2,
              show_default=True,
              type=float,
              help='Threshold for node connection distances.')
# 字体相关选项
@click.option('--font-size', 
              default=12,
              show_default=True,
              type=int,
              help='Font size for node labels in pixels.')
@click.option('--font-family',
              default='Arial, sans-serif',
              show_default=True,
              help='Font family for node labels.')
@click.option('--font-weight',
              default='normal',
              show_default=True,
              type=FontWeightChoice(
                  ['normal', 'bold', 'lighter', 
                   '100', '500', '900'],
                  case_sensitive=False
              ),
              help='Font weight for node labels. Choices: normal, bold, lighter, or 100-900.')
# 分支长度相关选项
@click.option('--min-branch-length',
              default=30.0,
              show_default=True,
              type=float,
              help='Minimum length for tree branches.')
@click.option('--max-branch-length',
              default=70.0,
              show_default=True,
              type=float,
              help='Maximum length for tree branches.')
@click.option('--default-length',
              default=40.0,
              show_default=True,
              type=float,
              help='Default length for branches without confidence values.')
# 连接线相关选项
@click.option('--link-color', 
              default='#999999', 
              help='Color of the connecting lines')
@click.option('--link-width', 
              default=1.5, 
              help='Width of the connecting lines')
# 可视化选项
@click.option('--show-confidence',
              is_flag=True,
              help='Show confidence values on the tree.')
def cli(input_file, groups_file, **kwargs):
    """Newick Tree Visualizer

    Create interactive visualizations from Newick format phylogenetic trees.

    Required Arguments:
    
        INPUT_FILE   Input Newick format file
        
        GROUPS_FILE  JSON file containing group definitions
    
    Example usage:

        newick-viz input.nwk groups.json -o output.html --font-size 14 --show-confidence

    For more information, visit: https://github.com/Bengerthelorf/newick-visualizer
    """
    try:
        click.echo(f"Processing {input_file}...")
        config = {
            'input_file': str(input_file),
            'groups_file': str(groups_file),
            **kwargs
        }
        
        create_tree_html(**config)
        click.echo(f"Successfully created visualization: {kwargs['output']}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

def main():
    """Main entry point for the CLI."""
    try:
        cli()
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        exit(1)

if __name__ == '__main__':
    main()