// 历史记录管理
class History {
    constructor(initialData) {
        this.states = [this.deepCloneData(initialData)];
        this.currentIndex = 0;
        this.updateUndoButton();
    }

    // 深度克隆树数据
    deepCloneData(data) {
        return {
            x: data.x,
            y: data.y,
            children: data.children ? data.children.map(child => this.deepCloneData(child)) : null,
            data: { ...data.data },
            parent: null  // 不克隆父节点引用，避免循环引用
        };
    }

    // 保存新状态
    saveState(data) {
        // 移除当前状态之后的所有状态
        this.states.splice(this.currentIndex + 1);
        // 添加新状态
        this.states.push(this.deepCloneData(data));
        this.currentIndex++;
        this.updateUndoButton();
    }

    // 撤销到上一步
    undo() {
        if (this.canUndo()) {
            this.currentIndex--;
            this.updateUndoButton();
            return this.deepCloneData(this.states[this.currentIndex]);
        }
        return null;
    }

    // 检查是否可以撤销
    canUndo() {
        return this.currentIndex > 0;
    }

    // 更新撤销按钮状态
    updateUndoButton() {
        const undoButton = document.getElementById('undo-button');
        if (undoButton) {
            undoButton.disabled = !this.canUndo();
        }
    }
}

// 主要的树渲染函数
function createTree(data) {
    // 初始化历史记录
    const history = new History(data);
    
    const {width, height, padding, treeLayout} = initializeTreeLayout();
    
    // 根据方向调整 viewBox
    let viewBoxParams;
    switch (treeDirection) {
        case 'left':
        case 'right':
            viewBoxParams = [-padding, -padding, width, height];
            break;
        case 'up':
        case 'down':
            viewBoxParams = [-padding, -padding, width, height];
            break;
    }
    
    // 创建SVG容器
    const svg = d3.select("#tree-container")
        .append("svg")
        .attr("viewBox", viewBoxParams.join(" "))
        .style("width", "100%")
        .style("height", "100%");

    // 创建分组背景层
    const groupsLayer = svg.append("g").attr("class", "groups");
    
    // 创建连接线层
    const linksLayer = svg.append("g")
        .attr("fill", "none")
        .attr("stroke", CONFIG.linkColor || "#999")
        .attr("stroke-opacity", 0.4)
        .attr("stroke-width", CONFIG.linkWidth || 1.5);
        
    // 创建节点层
    const nodesLayer = svg.append("g");

    // 创建拖动行为
    const drag = d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);

    // 画背景
    drawGroupBackgrounds(groupsLayer, data);
    
    // 画连接线
    const links = drawLinks(linksLayer, data);
    
    // 画节点并应用拖动
    const nodes = drawNodes(nodesLayer, data);
    nodes.call(drag);
    
    // 画图例
    createLegend();
    
    // 设置撤销按钮事件
    d3.select('#undo-button').on('click', () => {
        const previousState = history.undo();
        if (previousState) {
            // 更新数据
            updateTreeFromState(previousState);
        }
    });

    // 更新整个树的状态
    function updateTreeFromState(state) {
        // 递归更新所有节点的位置
        function updateNodePositions(node, stateNode) {
            node.x = stateNode.x;
            node.y = stateNode.y;
            if (node.children && stateNode.children) {
                node.children.forEach((child, i) => {
                    updateNodePositions(child, stateNode.children[i]);
                });
            }
        }

        updateNodePositions(data, state);

        // 更新视图
        nodes.attr("transform", d => {
            const [x, y] = transformCoordinates(d.x, d.y);
            return `translate(${x},${y})`;
        });

        // 更新连接线
        updateLinks();
        
        // 更新分组背景
        updateGroupBackgrounds();
    }
    
    // 拖动开始函数
    function dragstarted(event, d) {
        d3.select(this).classed("dragging", true);
        event.sourceEvent.stopPropagation();
    }

    // 拖动中函数
    function dragged(event, d) {
        const [x, y] = d3.pointer(event, svg.node());
        
        if (treeDirection === 'right' || treeDirection === 'left') {
            d.x = y;
            d.y = x - padding;
        } else {
            d.x = x;
            d.y = y - padding;
        }
        
        d3.select(this)
            .attr("transform", `translate(${x},${y})`);

        updateLinks();
        updateGroupBackgrounds();
    }

    // 拖动结束函数
    function dragended(event, d) {
        d3.select(this).classed("dragging", false);
        // 保存当前状态到历史记录
        history.saveState(data);
    }

    // 更新连接线的函数
    function updateLinks() {
        linksLayer.selectAll("path")
            .attr("d", d => {
                const source = transformCoordinates(d.source.x, d.source.y);
                const target = transformCoordinates(d.target.x, d.target.y);
                
                if (treeDirection === 'up' || treeDirection === 'down') {
                    const midY = (source[1] + target[1]) / 2;
                    return `M${source[0]},${source[1]}
                            C${source[0]},${midY}
                             ${target[0]},${midY}
                             ${target[0]},${target[1]}`;
                } else {
                    const midX = (source[0] + target[0]) / 2;
                    return `M${source[0]},${source[1]}
                            C${midX},${source[1]}
                             ${midX},${target[1]}
                             ${target[0]},${target[1]}`;
                }
            });
    }

    // 更新分组背景的函数
    function updateGroupBackgrounds() {
        groupsLayer.selectAll("path.group-background").remove();
        drawGroupBackgrounds(groupsLayer, data);
    }

    return svg.node();
}

// // 绘制连接线
function drawLinks(layer, data) {
    layer.selectAll("path")
        .data(data.links())
        .join("path")
        .attr("d", d => {
            const source = transformCoordinates(d.source.x, d.source.y);
            const target = transformCoordinates(d.target.x, d.target.y);
            
            // 根据方向使用不同的曲线绘制方式
            if (treeDirection === 'up' || treeDirection === 'down') {
                const midY = (source[1] + target[1]) / 2;
                return `M${source[0]},${source[1]}
                        C${source[0]},${midY}
                         ${target[0]},${midY}
                         ${target[0]},${target[1]}`;
            } else {
                const midX = (source[0] + target[0]) / 2;
                return `M${source[0]},${source[1]}
                        C${midX},${source[1]}
                         ${midX},${target[1]}
                         ${target[0]},${target[1]}`;
            }
        });
}

// 检查一个节点名称是否是可信度值（数字）
function isConfidenceValue(name) {
    return !isNaN(parseFloat(name)) && isFinite(name);
}

// 绘制节点
function drawNodes(layer, data) {
    // 创建节点组
    const node = layer
        .selectAll("g")
        .data(data.descendants())
        .join("g")
        .attr("transform", d => {
            const [x, y] = transformCoordinates(d.x, d.y);
            return `translate(${x},${y})`;
        });

    // 添加节点圆圈
    node.append("circle")
        .attr("fill", d => {
            const order = nodeOrderMap.get(d.data.name);
            if (order) {
                return groupData.groups[order.groupName].color;
            }
            return "#999";
        })
        .attr("r", 4);

    // 添加节点标签
    node.append("text")
        .attr("class", d => `node-label direction-${treeDirection}`)
        .style("font-family", CONFIG.fontFamily)
        .style("font-size", `${CONFIG.fontSize}px`)
        .style("font-weight", d => CONFIG.fontWeight)
        // .style("font-weight", d => {
        //     const order = nodeOrderMap.get(d.data.name);
        //     // 如果是分组中的节点，使用配置的font-weight，否则使用normal
        //     return order ? CONFIG.fontWeight : "normal";
        // })
        .text(d => {
            // 如果节点名称是数字（可信度值）
            if (isConfidenceValue(d.data.name)) {
                // 只在showConfidence为true时显示
                return CONFIG.showConfidence ? `(${parseFloat(d.data.name).toFixed(3)})` : "";
            }
            
            // 如果是普通节点
            let label = d.data.name;
            if (CONFIG.showConfidence && d.data.confidence !== undefined) {
                return `${label} (${d.data.confidence.toFixed(3)})`;
            }
            return label;
        })
        .attr("x", d => {
            switch (treeDirection) {
                case 'right': return 8;
                case 'left': return -8;
                default: return 0;
            }
        })
        .attr("y", d => {
            switch (treeDirection) {
                case 'down': return 15;
                case 'up': return -15;
                default: return 0;
            }
        })
        // .style("font-weight", d => {
        //     const order = nodeOrderMap.get(d.data.name);
        //     return order ? "bold" : "normal";
        // })
        // 根据标签是否为空来控制可见性
        .style("display", d => {
            if (!CONFIG.showConfidence && isConfidenceValue(d.data.name)) {
                return "none";
            }
            return null;
        });

    // 添加交互效果
    addNodeInteractions(node);

    return node;
}

// 添加节点交互效果
function addNodeInteractions(node) {
    node.on("mouseover", function(event, d) {
        // 如果节点正在被拖动，不执行hover效果
        if (!d3.select(this).classed("dragging")) {
            const circle = d3.select(this).select("circle");
            const currentColor = circle.attr("fill");
            
            circle.transition()
                .duration(200)
                .attr("r", 6)
                .attr("fill", d3.color(currentColor).darker(0.2));
                
            d3.select(this).select(".node-label")
                .transition()
                .duration(200)
                .style("font-size", `${CONFIG.fontSize * 1.2}px`);
        }
    })
    .on("mouseout", function(event, d) {
        // 如果节点正在被拖动，不执行hover效果
        if (!d3.select(this).classed("dragging")) {
            const circle = d3.select(this).select("circle");
            const currentColor = circle.attr("fill");
            
            circle.transition()
                .duration(200)
                .attr("r", 4)
                .attr("fill", currentColor);
                
            d3.select(this).select(".node-label")
                .transition()
                .duration(200)
                .style("font-size", `${CONFIG.fontSize}px`);
        }
    });
    
    // 注意：不需要在这里添加拖动事件，因为已经在createTree中通过.call(drag)添加了
}