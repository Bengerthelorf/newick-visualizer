// 初始化配置和映射
const layout = groupData.layout || {};
const useEvenDistribution = layout.evenDistribution !== false;
const treeDirection = layout.direction || 'right';
const groupOrder = layout.groupOrder || Object.keys(groupData.groups);

// 创建节点顺序映射
const nodeOrderMap = new Map();
const groupNodeMap = new Map();

// 初始化排序映射
groupOrder.forEach((groupName, groupIndex) => {
    const group = groupData.groups[groupName];
    if (!group || !group.order) return;
    
    group.order.forEach((nodeName, nodeIndex) => {
        nodeOrderMap.set(nodeName, {
            groupIndex: groupIndex,
            nodeIndex: nodeIndex,
            groupName: groupName
        });
    });
    
    // 保存组内节点顺序
    groupNodeMap.set(groupName, new Set(group.order));
});

// 获取一个节点的所有叶子节点
function getLeafNodes(node) {
    if (!node.children) {
        return [node];
    }
    return node.children.flatMap(getLeafNodes);
}

// 确定一组叶子节点主要属于哪个family
function getPrimaryFamily(leaves) {
    const familyCounts = new Map();
    
    leaves.forEach(leaf => {
        const order = nodeOrderMap.get(leaf.name);
        if (order) {
            const family = order.groupName;
            familyCounts.set(family, (familyCounts.get(family) || 0) + 1);
        }
    });
    
    // 返回出现次数最多的family
    return Array.from(familyCounts.entries())
        .sort((a, b) => b[1] - a[1])[0]?.[0] || null;
}

// 树结构的排序函数
function reorganizeTree(node) {
    if (!node) return node;
    if (!node.children) return node;
    
    // 递归处理子节点
    node.children = node.children.map(reorganizeTree);
    
    // 对于有多个子节点的情况，我们需要确定每个子树的"权重"
    node.children = node.children.sort((a, b) => {
        // 找到每个子树中所有的叶子节点
        const aLeaves = getLeafNodes(a);
        const bLeaves = getLeafNodes(b);
        
        // 计算每个子树的主要family（通过叶子节点判断）
        const aFamily = getPrimaryFamily(aLeaves);
        const bFamily = getPrimaryFamily(bLeaves);
        
        // 如果两个子树属于不同的family，按照groupOrder排序
        if (aFamily !== bFamily) {
            const aIndex = groupOrder.indexOf(aFamily);
            const bIndex = groupOrder.indexOf(bFamily);
            // 注意：这里返回负值让较小index的显示在上方
            return -(aIndex - bIndex);
        }
        
        return 0;
    });
    
    return node;
}

// Newick解析函数
function parseNewick(s) {
    const ancestors = [];
    let tree = {};
    let tokens = s.split(/\s*(;|\(|\)|,|:)\s*/);
    let subtree;
    
    for (let i = 0; i < tokens.length; i++) {
        const token = tokens[i];
        switch (token) {
            case '(':
                subtree = {};
                tree.children = [subtree];
                ancestors.push(tree);
                tree = subtree;
                break;
            case ',':
                subtree = {};
                ancestors[ancestors.length - 1].children.push(subtree);
                tree = subtree;
                break;
            case ')':
                tree = ancestors.pop();
                if (i + 1 < tokens.length && !isNaN(tokens[i + 1])) {
                    tree.confidence = parseFloat(tokens[i + 1]);
                }
                break;
            case ':':
                break;
            default:
                if (token !== ';') {
                    let x = tokens[i - 1];
                    if (x === ')' || x === '(' || x === ',') {
                        tree.name = token;
                    }
                }
                break;
        }
    }
    return tree;
}

// 坐标转换函数
function transformCoordinates(x, y) {
    switch (treeDirection) {
        case 'left':
            return [-y, x];
        case 'up':
            return [x, -y];
        case 'down':
            return [x, y];
        case 'right':
        default:
            return [y, x];
    }
}

// // 初始化树布局
function initializeTreeLayout() {
    const width = 1000;
    const height = 1000;
    const padding = 120;
    
    // 使用配置中的分支长度设置
    const branchLengthConfig = CONFIG.branchLength || {
        min: 30,
        max: 200,
        default: 100
    };

    console.log('Branch length config:', branchLengthConfig);  // 调试输出
    
    // 创建一个基于可信度的长度缩放函数
    const confidenceScale = d3.scaleLinear()
        .domain([0, 1])
        .range([branchLengthConfig.min, branchLengthConfig.max]);

    // 自定义树布局
    const treeLayout = d3.tree()
        .size([height - 2 * padding, width - 2 * padding])
        .separation((a, b) => {
            const aOrder = nodeOrderMap.get(a.data.name);
            const bOrder = nodeOrderMap.get(b.data.name);
            return aOrder && bOrder && aOrder.groupIndex === bOrder.groupIndex ? 1 : 2;
        });

    // 包装树布局以添加基于可信度的长度调整
    const wrappedLayout = function(root) {
        // 先应用原始布局
        const tree = treeLayout(root);
        
        // 调整每个节点的位置
        tree.each(node => {
            if (node.parent) {
                // 使用可信度值或默认长度
                const length = node.data.confidence !== undefined ?
                    confidenceScale(node.data.confidence) :
                    branchLengthConfig.default;
                
                // 根据树的方向调整位置
                if (treeDirection === 'right') {
                    node.y = node.parent.y + length;
                } else if (treeDirection === 'left') {
                    node.y = node.parent.y - length;
                } else if (treeDirection === 'down') {
                    node.x = node.parent.x + length;
                } else if (treeDirection === 'up') {
                    node.x = node.parent.x - length;
                }
            }
        });
        
        return tree;
    };

    return {width, height, padding, treeLayout: wrappedLayout};
}