# Newick Tree Visualizer

A tool for creating interactive visualizations of phylogenetic trees in Newick format.

## ✨ Features

- 🌳 Interactive visualization of phylogenetic trees
- 🎨 Configurable node and branch styling
- 🎯 Custom grouping and coloring of nodes
- 📐 Multiple layout directions (right, left, up, down)
- 🔄 Draggable nodes for manual layout adjustments
- 💾 Multiple export formats (HTML, PNG, JPG, PDF)
- ⚡️ Support for large-scale trees
- 🎯 Optional confidence values display

## 📦 Installation

### System Dependencies

Google Chrome is required:

```bash
# macOS
brew install --cask google-chrome

# Ubuntu
sudo apt-get update
sudo apt-get install google-chrome-stable

# CentOS
sudo yum install google-chrome-stable
```

### Python Package

```bash
pip install newick-visualizer
```

## 🚀 Quick Start

### Basic Usage

```bash
newick-viz input.nwk groups.json -o output.html
```

### Example with Options

```bash
newick-viz input.nwk groups.json \
    -o output.jpg \
    --padding 21 \
    --points 8 \
    --distance-threshold 1.5 \
    --min-branch-length 35 \
    --default-length 60 \
    --max-branch-length 80 \
    --opacity 0.6 \
    --font-size 13 \
    --font-weight bold \
    --link-width 3.0 \
    --link-color '#f7cc4f' \
    --render-delay 2000
```

### Export Formats

Supports multiple output formats:

```bash
# Interactive HTML
newick-viz input.nwk groups.json -o tree.html

# Static Images
newick-viz input.nwk groups.json -o tree.jpg
newick-viz input.nwk groups.json -o tree.png

# PDF Document
newick-viz input.nwk groups.json -o tree.pdf
```

## 🎮 Interactive Features

### 🖱️ Node Dragging

- Click and drag any node to manually adjust its position
- Connected lines and group backgrounds will update automatically
- Visual feedback during dragging (node highlight and size change)
- Changes persist in the visualization

### ↩️ Undo Function

- Undo button available in the top-left corner
- Reverts the last node movement
- Multiple levels of undo supported
- Visual feedback when undo is available/unavailable
- Keyboard shortcut support (⌃/⌘ + Z)

### ✨ Hover Effects

- Nodes enlarge slightly on hover
- Labels become more prominent
- Smooth transitions for all visual changes

## 🛠️ Configuration Options

### Basic Options

- `-o, --output`: Output file path [default: tree_visualization.html]
- `--render-delay`: Rendering delay in milliseconds [default: 2000]

### Visual Style

- `--padding`: Padding around nodes in pixels [default: 35]
- `--opacity`: Opacity of group backgrounds (0-1) [default: 0.3]
- `--points`: Number of points around each node [range: 6-24] [default: 12]
- `--distance-threshold`: Distance threshold for group backgrounds [default: 1.2]

### Font Settings

- `--font-size`: Font size in pixels [default: 12]
- `--font-family`: Font family [default: "Arial, sans-serif"]
- `--font-weight`: Font weight [default: "normal"]

### Branch Settings

- `--min-branch-length`: Minimum branch length [default: 30]
- `--max-branch-length`: Maximum branch length [default: 70]
- `--default-length`: Default length when no confidence value [default: 40]

### Connection Line Style

- `--link-color`: Color of connecting lines [default: "#999999"]
- `--link-width`: Width of connecting lines [default: 1.5]

### Other Settings

- `--show-confidence`: Show confidence values [flag]

## 📝 Input File Formats

### Newick File

Uses standard Newick format, for example:

```plaintext
((A:0.1,B:0.2)0.95:0.3,C:0.4);
```

### Groups Configuration File (JSON)

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

## 🔧 Development Installation

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

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

If you have any suggestions or feedback, please submit them on our [GitHub Issues page](https://github.com/Bengerthelorf/newick-visualizer/issues).


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [D3.js](https://d3js.org/) - Visualization library
- [Selenium](https://www.selenium.dev/) - Automated export generation
