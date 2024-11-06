# Newick Tree Visualizer

A tool for creating interactive visualizations of phylogenetic trees in Newick format.

## Features

- Interactive visualization of phylogenetic trees
- Support for multiple layout directions (right, left, up, down)
- Configurable node and branch styling
- Custom grouping and coloring of nodes
- Draggable nodes for manual layout adjustments
- Automatic confidence value display
- Interactive hover effects
- Customizable connecting lines

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
    --link-color "#336699" \
    --link-width 2.0 \
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
- `--link-color`: Color of connecting lines [default: #999999]
- `--link-width`: Width of connecting lines in pixels [default: 1.5]

### Interactive Features

#### Node Dragging

- Click and drag any node to manually adjust its position
- Connected lines and group backgrounds will update automatically
- Visual feedback during dragging (node highlight and size change)
- Changes persist in the visualization

#### Hover Effects

- Nodes enlarge slightly on hover
- Labels become more prominent
- Smooth transitions for all visual changes

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

### Project Structure

```bash
.
├── _version.py
├── LICENSE
├── MANIFEST.in
├── newick_visualizer/
│   ├── __init__.py
│   ├── core/
│   │   ├── tree_generator.py
│   │   ├── template_manager.py
│   │   └── utils.py
│   └── templates/
│       ├── base.html
│       ├── scripts/
│       │   ├── tree.js
│       │   ├── layout.js
│       │   ├── groups.js
│       │   └── main.js
│       └── styles/
│           └── main.css
├── README.md
└── setup.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.