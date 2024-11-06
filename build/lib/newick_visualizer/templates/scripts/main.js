// 主函数：初始化并启动可视化
function initializeVisualization() {
    try {
        // 验证必要的数据
        if (!CONFIG || !groupData || !newickData) {
            throw new Error("Required data configurations are missing");
        }

        // 解析并重组树结构
        let parsedTree = parseNewick(newickData);
        parsedTree = reorganizeTree(parsedTree);

        // 创建树层级
        const root = d3.hierarchy(parsedTree);

        // 创建树布局
        const {treeLayout} = initializeTreeLayout();

        // 应用布局
        const data = treeLayout(root);

        // 创建可视化
        createTree(data);
        
        console.log("Tree visualization completed successfully");

    } catch (error) {
        console.error("Failed to initialize visualization:", error);
        // 显示错误信息
        d3.select("#tree-container")
            .append("div")
            .style("color", "red")
            .style("padding", "20px")
            .text(`Error: ${error.message}`);
    }
}

// 当页面加载完成后启动可视化
document.addEventListener('DOMContentLoaded', initializeVisualization);