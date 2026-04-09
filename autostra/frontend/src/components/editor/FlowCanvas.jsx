/**
 * 文件注释：autostra/frontend/src/components/editor/FlowCanvas.jsx
 *
 * 职责：封装当前模块的初始化、常量、工具函数或组件逻辑。
 * 边界：仅承担本模块职责，不在此处定义跨模块业务规则。
 */

import ReactFlow, { Background, Controls, MiniMap, Panel } from 'reactflow';

const FlowCanvas = ({
  isEditorMode,
  nodes,
  edges,
  onNodesChange,
  onEdgesChange,
  onConnect,
  onEdgeDoubleClick,
  onInit,
  onDrop,
  onDragOver,
  onNodeClick,
  nodeTypes,
  selectedNode,
  onUpdateNodeData,
  onDeleteSelectedNode
}) => {
  if (!isEditorMode) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%', color: '#aaa', flexDirection: 'column' }}>
        <div style={{ fontSize: 40 }}>👋</div>
        <div>请在左侧选择一个策略开始编辑</div>
      </div>
    );
  }

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      onConnect={onConnect}
      onEdgeDoubleClick={onEdgeDoubleClick}
      onInit={onInit}
      onDrop={onDrop}
      onDragOver={onDragOver}
      onNodeClick={onNodeClick}
      nodeTypes={nodeTypes}
      fitView
    >
      <Controls />
      <MiniMap />
      <Background variant="dots" gap={12} size={1} />
      {selectedNode && selectedNode.data?.nodeType !== 'start' && (
        <Panel position="top-right" className="updatenode__controls">
          <h3>配置</h3>
          {selectedNode.data?.nodeType === 'loop_start' ? (
            <input type="number" placeholder="循环次数" onChange={(event) => onUpdateNodeData('loop_count', event.target.value)} />
          ) : selectedNode.data?.nodeType === 'wait' ? (
            <input type="number" placeholder="等待毫秒" onChange={(event) => onUpdateNodeData('time', event.target.value)} />
          ) : (
            <input placeholder="参数" onChange={(event) => onUpdateNodeData('keyword', event.target.value)} />
          )}
          <button style={{ marginTop: 10, color: 'red' }} onClick={onDeleteSelectedNode}>删除</button>
        </Panel>
      )}
    </ReactFlow>
  );
};

export default FlowCanvas;