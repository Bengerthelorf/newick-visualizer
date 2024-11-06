// 主要的树渲染函数
function createTree(data) {
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

    // 画背景
    drawGroupBackgrounds(groupsLayer, data);
    
    // 画连接线
    drawLinks(linksLayer, data);
    
    // 画节点
    drawNodes(nodesLayer, data);
    
    // 画图例
    createLegend();
    
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
        const circle = d3.select(this).select("circle");
        const currentColor = circle.attr("fill");
        
        circle.transition()
            .duration(200)
            .attr("r", 6)
            .attr("fill", d3.color(currentColor).darker(0.2));
            
        d3.select(this).select(".node-label")
            .transition()
            .duration(200)
            .style("font-size", `${CONFIG.fontSize * 1.2}px`);  // hover时增大20%
    })
    .on("mouseout", function(event, d) {
        const circle = d3.select(this).select("circle");
        const currentColor = circle.attr("fill");
        
        circle.transition()
            .duration(200)
            .attr("r", 4)
            .attr("fill", currentColor);
            
        d3.select(this).select(".node-label")
            .transition()
            .duration(200)
            .style("font-size", `${CONFIG.fontSize}px`);  // 恢复原始大小
    });
}