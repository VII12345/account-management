import React, { useState, useRef, useCallback, useEffect } from 'react';
import ReactFlow, {
  ReactFlowProvider,
  addEdge,
  useNodesState,
  useEdgesState,
  Controls,
  Background,
  MiniMap,
  Panel,
  MarkerType
} from 'reactflow';
import 'reactflow/dist/style.css';
import axios from 'axios';
import './index.css';

// 配置：平台定义
const PLATFORMS = [
  {
    id: 'x', name: 'X (Twitter)', icon: '𝕏', color: '#000000',
    items: [{ type: 'login_x', label: '🔑 登录账号' }, { type: 'like_x', label: '❤️ 随机点赞' }, { type: 'zhuan_x', label: '🔁 随机转发' }, { type: 'post_x', label: '📝 发布推文' }]
  },
  {
    id: 'youtube', name: 'YouTube', icon: '▶️', color: '#ff0000',
    items: [{ type: 'youtube_login', label: '🔑 打开网站' }, { type: 'youtube_search', label: '👀 搜索视频' }, { type: 'youtube_watch', label: '🔔 观看视频' }, { type: 'youtube_interact', label: '🔔 订阅频道' }, { type: 'youtube_like', label: '🔔 视频点赞' }]
  },
  {
    id: 'tiktok', name: 'TikTok', icon: '🎵', color: '#00f2ea',
    items: [{ type: 'swipe_tk', label: '👆 刷视频' }, { type: 'like_tk', label: '❤️ 双击点赞' }]
  },
  { id: 'instagram', name: 'Instagram', icon: '📷', color: '#E1306C', items: [] },
  { id: 'facebook', name: 'Facebook', icon: '📘', color: '#1877f2', items: [{ type: 'login_fb', label: '🔑 登录FB' }] },
  { id: 'threads', name: 'Threads', icon: '🌀', color: '#000000', items: [] },
  { id: 'tinder', name: 'Tinder', icon: '🔥', color: '#fe3c72', items: [] },
  {
    id: 'common', name: '公共动作', icon: '🧩', color: '#333',
    items: [{ type: 'loop_start', label: '🔄 循环开始' }, { type: 'wait', label: '⏳ 等待时间' }]
  }
];

// 默认初始节点
const DEFAULT_NODES = [{ id: '1', type: 'input', data: { label: 'Start' }, position: { x: 250, y: 50 } }];

let id = 100;
const getId = () => `node_${id++}`;
const nodeTypes = {};

const App = () => {
  const reactFlowWrapper = useRef(null);

  // --- 视图状态 ---
  const [viewMode, setViewMode] = useState('platforms'); // 'platforms' | 'strategies' | 'editor'
  const [currentPlatform, setCurrentPlatform] = useState(null); // 当前选中的平台对象
  const [currentStrategyName, setCurrentStrategyName] = useState(null); // 当前选中的策略文件名

  // --- 数据状态 ---
  const [stats, setStats] = useState({}); // { x: 5, youtube: 12 }
  const [strategyList, setStrategyList] = useState([]); // ['strategy1', 'test2']

  // --- 画布状态 ---
  const [nodes, setNodes, onNodesChange] = useNodesState(DEFAULT_NODES);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedNode, setSelectedNode] = useState(null);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);
  const [logs, setLogs] = useState([]);
  const [resultImg, setResultImg] = useState(null);

  const [loading, setLoading] = useState(false); // 控制运行按钮状态
  const [saving, setSaving] = useState(false);   // 控制保存按钮状态

  // ===========================
  // 1. 初始化：获取统计数据
  // ===========================
  const fetchStats = async () => {
    try {
      const res = await axios.get(`http://${window.location.hostname}:8000/stats`);
      setStats(res.data);
    } catch (e) { console.error("Failed to fetch stats"); }
  };

  useEffect(() => { fetchStats(); }, []);

  // ===========================
  // 2. 交互逻辑
  // ===========================

  // 点击平台 -> 进入策略列表
  const handlePlatformClick = async (platform) => {
    setCurrentPlatform(platform);
    setViewMode('strategies');
    try {
      const res = await axios.get(`http://${window.location.hostname}:8000/list/${platform.id}`);
      setStrategyList(res.data.strategies);
    } catch (e) { setStrategyList([]); }
  };

  // 点击某个策略 -> 加载并进入编辑器
  // 点击某个策略 -> 加载并进入编辑器
  // 点击某个策略 -> 加载并进入编辑器
  // 点击某个策略 -> 加载并进入编辑器
  const handleStrategyClick = async (name) => {
    try {
      const res = await axios.get(`http://${window.location.hostname}:8000/load/${currentPlatform.id}/${name}`);

      console.log("原始数据:", res.data); // 调试用

      // === 🛡️ 1. 清洗节点 (Nodes) ===
      let safeNodes = [];
      if (res.data && Array.isArray(res.data.nodes)) {
        safeNodes = res.data.nodes.map(node => ({
          ...node,
          // 修复坐标丢失导致重叠
          position: node.position || { x: 0, y: 0 },
          // 修复 data 丢失
          data: node.data || {},
          // 修复 type 丢失
          type: node.type || 'default'
        }));
      }

      // 🛡️ 保底逻辑：如果加载出来的节点里没有 Start，强行补一个
      // 防止后端报错 "未找到开始节点"
      const hasStart = safeNodes.some(n => n.data && n.data.nodeType === 'start');
      if (!hasStart) {
        safeNodes.push({
          id: '1',
          type: 'input',
          data: { label: `Start ${currentPlatform.name}`, nodeType: 'start' },
          position: { x: 250, y: 50 },
          style: { background: currentPlatform.color, color: '#fff', border: 'none', width: 80, borderRadius: '20px', fontWeight: 'bold' }
        });
      }

      // === 🛡️ 2. 清洗连线 (Edges) - 解决报错的关键！ ===
      let safeEdges = [];
      if (res.data && Array.isArray(res.data.edges)) {
        safeEdges = res.data.edges.map((edge, index) => ({
          ...edge,
          // ⚠️ 关键修复：如果 edge.id 是 null，React 就会报 "same key null" 错误
          // 这里我们生成一个唯一的 ID：e_源_目标_索引
          id: edge.id || `e_${edge.source}-${edge.target}_${index}`,
          markerEnd: { type: MarkerType.ArrowClosed }
        }));
      }
      // ===================================

      setNodes(safeNodes);
      setEdges(safeEdges);

      setCurrentStrategyName(name);
      setViewMode('editor');
    } catch (e) {
      console.error(e);
      alert('加载失败: ' + e.message);
    }
  };

  // 创建新策略
  const handleCreateNew = () => {
    const name = prompt("请输入新策略名称 (例如: 每日点赞):");
    if (!name) return;
    setCurrentStrategyName(name);
    setNodes(DEFAULT_NODES);
    setEdges([]);
    setViewMode('editor');
  };

  // 保存当前策略
  // ==============================================
  // 4. 保存功能
  // ==============================================
  const handleSave = async (showTip = true) => {
    // 修改 1: 使用 currentPlatform 判断
    if (!currentPlatform) return;
    if (currentPlatform.id === 'common') return; // 公共动作不需要保存

    if (!currentStrategyName) {
      if (showTip) alert("请先新建或选择一个策略文件！");
      return;
    }

    // 如果你定义了 saving 状态，取消注释下面这行
    // setSaving(true); 

    const payload = {
      nodes: nodes,
      edges: edges,
      cdp_url: ""
    };

    try {
      // 修改 2: URL 路径使用 currentPlatform.id
      await axios.post(`http://${window.location.hostname}:8000/save/${currentPlatform.id}/${currentStrategyName}`, payload);

      if (showTip) {
        // 修改 3: 提示语使用 currentPlatform.name
        alert(`✅ [${currentPlatform.name}] 策略 "${currentStrategyName}" 已保存！`);
      }

      // 刷新侧边栏的数字统计
      fetchStats();

    } catch (e) {
      console.error(e);
      if (showTip) alert('❌ 保存失败，请检查后端');
    } finally {
      // setSaving(false);
    }
  };

  // 运行
  const handleRun = async () => {
    setLoading(true);
    setLogs([]); setResultImg(null);

    // 1. 静默保存
    await handleSave(false);

    const payload = { nodes, edges, cdp_url: "http://127.0.0.1:9222" };

    try {
      const res = await axios.post(`http://${window.location.hostname}:8000/run`, payload);
      if (res.data.status === 'success') {
        setLogs(res.data.logs);
        setResultImg(res.data.screenshot);
        // 修改: 使用 currentPlatform.name
        alert(`✅ [${currentPlatform.name}] 执行完成！`);
      } else {
        alert('❌ 出错: ' + res.data.message);
      }
    } catch (e) {
      alert('⚠️ 后端连接失败');
    } finally {
      setLoading(false);
    }
  };

  // --- React Flow 基础 ---
  const onConnect = useCallback((params) => setEdges((eds) => addEdge({ ...params, markerEnd: { type: MarkerType.ArrowClosed } }, eds)), [setEdges]);
  const onEdgeDoubleClick = useCallback((event, edge) => setEdges((eds) => eds.filter((e) => e.id !== edge.id)), [setEdges]);
  const onNodeClick = (event, node) => setSelectedNode(node);
  const onDragStart = (event, nodeType, label) => { event.dataTransfer.setData('application/reactflow', JSON.stringify({ nodeType, label })); event.dataTransfer.effectAllowed = 'move'; };
  const onDragOver = useCallback((event) => { event.preventDefault(); event.dataTransfer.dropEffect = 'move'; }, []);
  const onDrop = useCallback((event) => {
    event.preventDefault();
    const dataStr = event.dataTransfer.getData('application/reactflow');
    if (!dataStr) return;
    const { nodeType, label } = JSON.parse(dataStr);
    const position = reactFlowInstance.project({ x: event.clientX - reactFlowWrapper.current.getBoundingClientRect().left, y: event.clientY - reactFlowWrapper.current.getBoundingClientRect().top });
    setNodes((nds) => nds.concat({ id: getId(), type: 'default', position, data: { label, nodeType } }));
  }, [reactFlowInstance, setNodes]);

  const updateNodeData = (field, value) => {
    if (!selectedNode) return;
    setNodes((nds) => nds.map((node) => {
      if (node.id === selectedNode.id) {
        const newData = { ...node.data, [field]: value };
        let label = node.data.label.split('\n')[0].split(':')[0];
        if (field === 'keyword') newData.label = `${label}: ${value}`;
        if (field === 'loop_count') newData.label = `🔄 循环 ${value} 次`;
        if (field === 'time') newData.label = `⏳ 等待 ${value} ms`;
        return { ...node, data: newData };
      }
      return node;
    }));
  };

  // ===========================
  // 渲染侧边栏内容 (根据 viewMode)
  // ===========================
  const renderSidebarContent = () => {
    // 1. 平台列表视图
    if (viewMode === 'platforms') {
      return (
        <div className="platform-list">
          <div style={{ padding: '15px', fontWeight: 'bold', fontSize: '16px' }}>📚 选择平台</div>
          {PLATFORMS.map(p => (
            <div key={p.id} className="platform-item" onClick={() => handlePlatformClick(p)}>
              <div className="platform-left">
                <span className="platform-icon" style={{ color: p.color }}>{p.icon}</span>
                <span>{p.name}</span>
              </div>
              <div className="badge-count">{stats[p.id] || 0}</div>
            </div>
          ))}
        </div>
      );
    }

    // 2. 策略列表视图
    if (viewMode === 'strategies') {
      return (
        <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
          <div className="sidebar-nav">
            <button className="back-btn" onClick={() => setViewMode('platforms')}>⬅️</button>
            <span style={{ fontWeight: 'bold' }}>{currentPlatform.name} 策略库</span>
          </div>
          <div style={{ flex: 1, overflowY: 'auto' }}>
            {strategyList.length === 0 && <div style={{ padding: 20, color: '#999', fontSize: 12 }}>暂无策略，请新建</div>}
            {strategyList.map(name => (
              <div key={name} className="strategy-item" onClick={() => handleStrategyClick(name)}>
                📄 {name}
              </div>
            ))}
          </div>
          <div style={{ padding: 10, borderTop: '1px solid #eee' }}>
            <button className="run-btn" onClick={handleCreateNew}>+ 新建策略</button>
          </div>
        </div>
      );
    }

    // 3. 编辑器视图 (模块库)
    if (viewMode === 'editor') {
      const commonItems = PLATFORMS.find(p => p.id === 'common').items;
      return (
        <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
          <div className="sidebar-nav">
            <button className="back-btn" onClick={() => {
              // 返回时重新获取列表
              axios.get(`http://${window.location.hostname}:8000/list/${currentPlatform.id}`).then(res => setStrategyList(res.data.strategies));
              setViewMode('strategies');
            }}>⬅️</button>
            <span style={{ fontWeight: 'bold', fontSize: 12, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              正在编辑: {currentStrategyName}
            </span>
          </div>

          <div style={{ flex: 1, overflowY: 'auto', padding: 10 }}>
            {/* 当前平台专属模块 */}
            <div style={{ marginBottom: 15 }}>
              <div style={{ fontSize: 12, color: '#999', marginBottom: 5 }}>专属动作</div>
              {currentPlatform.items.map(item => (
                <div key={item.type} className="dndnode" onDragStart={(e) => onDragStart(e, item.type, item.label)} draggable style={{ borderLeft: `3px solid ${currentPlatform.color}` }}>
                  {item.label}
                </div>
              ))}
            </div>

            {/* 公共动作 */}
            <div>
              <div style={{ fontSize: 12, color: '#999', marginBottom: 5 }}>公共动作</div>
              {commonItems.map(item => (
                <div key={item.type} className="dndnode" onDragStart={(e) => onDragStart(e, item.type, item.label)} draggable>
                  {item.label}
                </div>
              ))}
            </div>
          </div>

          <div style={{ padding: 10, borderTop: '1px solid #eee', display: 'flex', flexDirection: 'column', gap: 5 }}>
            <button className="run-btn" style={{ background: '#fff', color: '#333', border: '1px solid #ccc' }} onClick={handleSave}>💾 保存</button>
            <button className="run-btn" onClick={handleRun} style={{ background: currentPlatform.color }}>▶ 运行</button>
          </div>

          {/* 简易日志 */}
          {logs.length > 0 && <div style={{ height: 100, overflowY: 'auto', fontSize: 10, background: '#eee', padding: 5 }}>{logs.map((l, i) => <div key={i}>{l}</div>)}</div>}
          {resultImg && <img src={resultImg} style={{ width: '100%' }} />}
        </div>
      );
    }
  };

  return (
    <div className="app-layout">
      <ReactFlowProvider>
        <aside style={{ width: 250, borderRight: '1px solid #ddd', background: '#fcfcfc' }}>
          {renderSidebarContent()}
        </aside>

        <div className="reactflow-wrapper" ref={reactFlowWrapper}>
          {viewMode === 'editor' ? (
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onConnect={onConnect}
              onEdgeDoubleClick={onEdgeDoubleClick}
              onInit={setReactFlowInstance}
              onDrop={onDrop}
              onDragOver={onDragOver}
              onNodeClick={onNodeClick}
              nodeTypes={nodeTypes}  // <--- 加上这个，消除警告
              fitView
            >
              <Controls /><MiniMap /><Background variant="dots" gap={12} size={1} />
              {selectedNode && selectedNode.data.nodeType !== 'start' && (
                <Panel position="top-right" className="updatenode__controls">
                  {/* 简化的属性面板 */}
                  <h3>配置</h3>
                  {selectedNode.data.nodeType === 'loop_start' ? (
                    <input type="number" placeholder="循环次数" onChange={(e) => updateNodeData('loop_count', e.target.value)} />
                  ) : selectedNode.data.nodeType === 'wait' ? (
                    <input type="number" placeholder="等待毫秒" onChange={(e) => updateNodeData('time', e.target.value)} />
                  ) : (
                    <input placeholder="参数" onChange={(e) => updateNodeData('keyword', e.target.value)} />
                  )}
                  <button style={{ marginTop: 10, color: 'red' }} onClick={() => { setNodes((ns) => ns.filter(n => n.id !== selectedNode.id)); setSelectedNode(null) }}>删除</button>
                </Panel>
              )}
            </ReactFlow>
          ) : (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%', color: '#aaa', flexDirection: 'column' }}>
              <div style={{ fontSize: 40 }}>👋</div>
              <div>请在左侧选择一个策略开始编辑</div>
            </div>
          )}
        </div>
      </ReactFlowProvider>
    </div>
  );
};

export default App;