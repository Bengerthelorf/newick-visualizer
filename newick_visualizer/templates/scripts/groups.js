// 绘制分组背景
function drawGroupBackgrounds(layer, data) {
    groupOrder.forEach(groupName => {
        const group = groupData.groups[groupName];
        if (!group) return;

        // 获取组内节点并按配置顺序排序
        const nodeSet = groupNodeMap.get(groupName);
        const groupNodes = data.descendants()
            .filter(d => nodeSet.has(d.data.name))
            .sort((a, b) => {
                const aOrder = nodeOrderMap.get(a.data.name);
                const bOrder = nodeOrderMap.get(b.data.name);
                return aOrder.nodeIndex - bOrder.nodeIndex;
            });

        if (groupNodes.length > 0) {
            const areaPoints = generateGroupArea(groupNodes);
            if (areaPoints) {
                const hull = d3.polygonHull(areaPoints.map(p => [p.x, p.y]));
                if (hull) {
                    const curve = d3.line().curve(d3.curveBasisClosed);
                    const pathData = curve(hull);

                    layer.append("path")
                        .attr("d", pathData)
                        .attr("fill", group.color)
                        .attr("class", "group-background")
                        .style("opacity", CONFIG.opacity);  // 使用配置的透明度
                }
            }
        }
    });
}

// 生成分组区域点
function generateGroupArea(groupNodes) {
    if (groupNodes.length < 2) return null;

    const padding = CONFIG.padding || 35;
    const pointsCount = CONFIG.pointsPerNode || 12;
    const distanceThreshold = CONFIG.distanceThreshold || 1.2;  // 使用距离阈值
    let points = [];

    for (let i = 0; i < groupNodes.length; i++) {
        const node = groupNodes[i];
        const [x, y] = transformCoordinates(node.x, node.y);
        
        // 基础环绕点
        for (let j = 0; j < pointsCount; j++) {
            const angle = (j / pointsCount) * 2 * Math.PI;
            // 使用 distanceThreshold 调整基础半径
            const baseRadius = padding * (i === 0 || i === groupNodes.length - 1 ? distanceThreshold : 1);
            points.push({
                x: x + Math.cos(angle) * baseRadius,
                y: y + Math.sin(angle) * baseRadius
            });
        }

        // 连接点
        if (i < groupNodes.length - 1) {
            const nextNode = groupNodes[i + 1];
            const [nextX, nextY] = transformCoordinates(nextNode.x, nextNode.y);
            
            // 计算两个节点之间的距离
            const distance = Math.sqrt(Math.pow(nextX - x, 2) + Math.pow(nextY - y, 2));
            // 根据距离和阈值调整连接点的数量和扰动
            const connectionPoints = Math.ceil(distance / (padding * distanceThreshold));
            const disturbance = padding * 0.2 * distanceThreshold;
            
            for (let t = 1; t < connectionPoints; t++) {
                const ratio = t / connectionPoints;
                points.push({
                    x: x * (1 - ratio) + nextX * ratio + (Math.random() - 0.5) * disturbance,
                    y: y * (1 - ratio) + nextY * ratio + (Math.random() - 0.5) * disturbance
                });
            }
        }
    }

    return points;
}

// 创建图例
function createLegend() {
    const legend = d3.select("#legend");
    groupOrder.forEach(groupName => {
        const group = groupData.groups[groupName];
        if (!group) return;
        
        const item = legend.append("div")
            .attr("class", "legend-item");
        
        item.append("div")
            .attr("class", "legend-color")
            .style("background-color", group.color);
        
        item.append("span")
            .text(groupName);
    });
}