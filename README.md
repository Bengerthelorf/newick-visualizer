# Newick Tree Visualizer

A tool for creating interactive visualizations of phylogenetic trees in Newick format.

## Installation

You can install newick-visualizer using pip:

```bash
pip install newick-visualizer
```

## Usage

Basic usage:

```bash
newick-viz input.nwk groups.json
```

With options:

```bash
newick-viz input.nwk groups.json \
    --output output.html \
    --font-size 14 \
    --show-confidence
```

### Options

- `-o, --output`: Output HTML file path [default: tree_visualization.html]
- `--padding`: Padding around nodes in pixels [default: 35]
- `--opacity`: Opacity of group backgrounds (0-1) [default: 0.3]
- `--points`: Number of points around each node [6-24] [default: 12]
- `--font-size`: Font size in pixels [default: 12]
- `--font-family`: Font family for labels [default: Arial, sans-serif]
- `--font-weight`: Font weight [default: normal]
- `--show-confidence`: Show confidence values

For a complete list of options:

```bash
newick-viz --help
```

## Input Files

### Newick File

The input Newick file should be in standard Newick format. Example:

```plaintext
((A:0.1,B:0.2)0.95:0.3,C:0.4);
```

### Groups JSON File

The groups configuration file should be in JSON format. Example:

```json
{
  "layout": {
    "direction": "right",
    "groupOrder": ["Group1", "Group2"]
  },
  "groups": {
    "Group1": {
      "color": "#ffcdd2",
      "members": ["A", "B"],
      "order": ["B", "A"]
    },
    "Group2": {
      "color": "#c8e6c9",
      "members": ["C"],
      "order": ["C"]
    }
  }
}
```

## Development

For development installation:

```bash
git clone https://github.com/Bengerthelorf/newick-visualizer.git
cd newick-visualizer
pip install -e .
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.