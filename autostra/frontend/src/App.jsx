import React, { useState, useRef, useCallback, useEffect } from 'react';
import { ReactFlowProvider, addEdge, useNodesState, useEdgesState, MarkerType } from 'reactflow';
import 'reactflow/dist/style.css';
import './index.css';
import { DEFAULT_NODES, NODE_TYPES } from './constants/flow';
import { PLATFORMS, getCommonItems } from './constants/platforms';
import {
  fetchStatsApi,
  listAccountsApi,
  listStrategiesApi,
  loadStrategyApi,
  saveStrategyApi,
  runStrategyApi
} from './services/autostraApi';
import { getNextNodeId } from './utils/nodeFactory';
import PlatformList from './components/sidebar/PlatformList';
import AccountList from './components/sidebar/AccountList';
import StrategyList from './components/sidebar/StrategyList';
import EditorSidebar from './components/sidebar/EditorSidebar';
import FlowCanvas from './components/editor/FlowCanvas';

const App = () => {
  const reactFlowWrapper = useRef(null);

  // --- 视图状态 ---
  const [viewMode, setViewMode] = useState('platforms'); // 'platforms' | 'accounts' | 'strategies' | 'editor'
  const [currentPlatform, setCurrentPlatform] = useState(null); // 当前选中的平台对象
  const [currentAccount, setCurrentAccount] = useState(null); // { id, name }
  const [currentStrategyName, setCurrentStrategyName] = useState(null); // 当前选中的策略文件名

  // --- 数据状态 ---
  const [stats, setStats] = useState({}); // { x: 5, youtube: 12 }
  const [accountList, setAccountList] = useState([]); // [{ id, name }]
  const [strategyList, setStrategyList] = useState([]); // ['strategy1', 'test2']

  // --- 画布状态 ---
  const [nodes, setNodes, onNodesChange] = useNodesState(DEFAULT_NODES);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedNode, setSelectedNode] = useState(null);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);
  const [logs, setLogs] = useState([]);
  const [resultImg, setResultImg] = useState(null);

  const [loading, setLoading] = useState(false); // 控制运行按钮状态
  const [saving] = useState(false);

  const fetchStats = async () => {
    try {
      const res = await fetchStatsApi();
      setStats(res.data);
    } catch {
      console.error('Failed to fetch stats');
    }
  };

  useEffect(() => { fetchStats(); }, []);

  const handlePlatformClick = async (platform) => {
    setCurrentPlatform(platform);
    setCurrentAccount(null);
    setCurrentStrategyName(null);
    setStrategyList([]);
    setViewMode('accounts');

    try {
      const res = await listAccountsApi(platform.id);
      const accounts = res.data.accounts || [];
      setAccountList(accounts);
    } catch (error) {
      console.error(error);
      setAccountList([]);
      alert(error?.message || '账号获取失败，请检查账号接口配置');
    }
  };

  const handleAccountClick = async (account) => {
    if (!currentPlatform) return;

    setCurrentAccount(account);
    setCurrentStrategyName(null);
    setViewMode('strategies');

    try {
      const res = await listStrategiesApi(currentPlatform.id, account.id);
      setStrategyList(res.data.strategies || []);
    } catch {
      setStrategyList([]);
    }
  };

  const handleStrategyClick = async (name) => {
    try {
      if (!currentAccount) {
        alert('请先选择账号');
        return;
      }

      const res = await loadStrategyApi(currentPlatform.id, currentAccount.id, name);
      let safeNodes = [];
      if (res.data && Array.isArray(res.data.nodes)) {
        safeNodes = res.data.nodes.map((node) => ({
          ...node,
          position: node.position || { x: 0, y: 0 },
          data: node.data || {},
          type: node.type || 'default'
        }));
      }

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

      let safeEdges = [];
      if (res.data && Array.isArray(res.data.edges)) {
        safeEdges = res.data.edges.map((edge, index) => ({
          ...edge,
          id: edge.id || `e_${edge.source}-${edge.target}_${index}`,
          markerEnd: { type: MarkerType.ArrowClosed }
        }));
      }

      setNodes(safeNodes);
      setEdges(safeEdges);

      setCurrentStrategyName(name);
      setViewMode('editor');
    } catch (e) {
      console.error(e);
      alert('加载失败: ' + e.message);
    }
  };

  const handleCreateNew = () => {
    const name = prompt('请输入新策略名称 (例如: 每日点赞):');
    if (!name) return;
    setCurrentStrategyName(name);
    setNodes([...DEFAULT_NODES]);
    setEdges([]);
    setViewMode('editor');
  };

  const handleSave = async (showTip = true) => {
    if (!currentPlatform) return;
    if (currentPlatform.id === 'common') return;
    if (!currentAccount) {
      if (showTip) alert('请先选择账号');
      return;
    }

    if (!currentStrategyName) {
      if (showTip) alert('请先新建或选择一个策略文件！');
      return;
    }

    const payload = {
      nodes,
      edges,
      cdp_url: ''
    };

    try {
      await saveStrategyApi(currentPlatform.id, currentAccount.id, currentStrategyName, payload);

      if (showTip) {
        alert(`✅ [${currentPlatform.name}/${currentAccount.name}] 策略 "${currentStrategyName}" 已保存！`);
      }
      fetchStats();
    } catch (e) {
      console.error(e);
      if (showTip) alert('❌ 保存失败，请检查后端');
    }
  };

  const handleRun = async () => {
    if (!currentPlatform) return;
    setLoading(true);
    setLogs([]);
    setResultImg(null);

    await handleSave(false);

    const payload = { nodes, edges, cdp_url: "http://127.0.0.1:9222" };

    try {
      const res = await runStrategyApi(payload);
      if (res.data.status === 'success') {
        setLogs(res.data.logs);
        setResultImg(res.data.screenshot);
        alert(`✅ [${currentPlatform.name}/${currentAccount?.name || '-'}] 执行完成！`);
      } else {
        alert('❌ 出错: ' + res.data.message);
      }
    } catch {
      alert('⚠️ 后端连接失败');
    } finally {
      setLoading(false);
    }
  };

  const onConnect = useCallback(
    (params) => setEdges((currentEdges) => addEdge({ ...params, markerEnd: { type: MarkerType.ArrowClosed } }, currentEdges)),
    [setEdges]
  );
  const onEdgeDoubleClick = useCallback((event, edge) => setEdges((eds) => eds.filter((e) => e.id !== edge.id)), [setEdges]);
  const onNodeClick = (event, node) => setSelectedNode(node);
  const onDragStart = (event, nodeType, label) => {
    event.dataTransfer.setData('application/reactflow', JSON.stringify({ nodeType, label }));
    event.dataTransfer.effectAllowed = 'move';
  };
  const onDragOver = useCallback((event) => { event.preventDefault(); event.dataTransfer.dropEffect = 'move'; }, []);

  const onDrop = useCallback((event) => {
    event.preventDefault();
    const dataStr = event.dataTransfer.getData('application/reactflow');
    if (!dataStr || !reactFlowInstance || !reactFlowWrapper.current) return;

    const { nodeType, label } = JSON.parse(dataStr);
    const bounds = reactFlowWrapper.current.getBoundingClientRect();
    const position = reactFlowInstance.project({
      x: event.clientX - bounds.left,
      y: event.clientY - bounds.top
    });
    setNodes((nds) => nds.concat({ id: getNextNodeId(), type: 'default', position, data: { label, nodeType } }));
  }, [reactFlowInstance, setNodes]);

  const updateNodeData = (field, value) => {
    if (!selectedNode) return;
    setNodes((nds) => nds.map((node) => {
      if (node.id === selectedNode.id) {
        const newData = { ...node.data, [field]: value };
        const baseLabel = (node.data?.label || '').split('\n')[0].split(':')[0] || node.data?.label || '';
        if (field === 'loop_count') newData.label = `🔄 循环 ${value} 次`;
        if (field === 'time') newData.label = `⏳ 等待 ${value} ms`;
        if (field === 'keyword') newData.label = `${baseLabel}: ${value}`;
        return { ...node, data: newData };
      }
      return node;
    }));
  };

  const handleBackToStrategies = async () => {
    if (!currentPlatform || !currentAccount) return;
    try {
      const res = await listStrategiesApi(currentPlatform.id, currentAccount.id);
      setStrategyList(res.data.strategies || []);
    } catch {
      setStrategyList([]);
    }
    setViewMode('strategies');
  };

  const handleDeleteSelectedNode = () => {
    if (!selectedNode) return;
    setNodes((currentNodes) => currentNodes.filter((node) => node.id !== selectedNode.id));
    setSelectedNode(null);
  };

  const renderSidebarContent = () => {
    if (viewMode === 'platforms') {
      return <PlatformList platforms={PLATFORMS} stats={stats} onPlatformClick={handlePlatformClick} />;
    }

    if (viewMode === 'accounts') {
      return (
        <AccountList
          currentPlatform={currentPlatform}
          accountList={accountList}
          onBack={() => setViewMode('platforms')}
          onAccountClick={handleAccountClick}
        />
      );
    }

    if (viewMode === 'strategies') {
      return (
        <StrategyList
          currentPlatform={currentPlatform}
          currentAccount={currentAccount?.name}
          strategyList={strategyList}
          onBack={() => setViewMode('accounts')}
          onStrategyClick={handleStrategyClick}
          onCreateNew={handleCreateNew}
        />
      );
    }

    if (viewMode === 'editor') {
      return (
        <EditorSidebar
          currentPlatform={currentPlatform}
          currentStrategyName={currentStrategyName}
          commonItems={getCommonItems()}
          logs={logs}
          resultImg={resultImg}
          onBack={handleBackToStrategies}
          onDragStart={onDragStart}
          onSave={handleSave}
          onRun={handleRun}
          loading={loading}
          saving={saving}
        />
      );
    }

    return null;
  };

  return (
    <div className="app-layout">
      <ReactFlowProvider>
        <aside style={{ width: 250, borderRight: '1px solid #ddd', background: '#fcfcfc' }}>
          {renderSidebarContent()}
        </aside>

        <div className="reactflow-wrapper" ref={reactFlowWrapper}>
          <FlowCanvas
            isEditorMode={viewMode === 'editor'}
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
            nodeTypes={NODE_TYPES}
            selectedNode={selectedNode}
            onUpdateNodeData={updateNodeData}
            onDeleteSelectedNode={handleDeleteSelectedNode}
          />
        </div>
      </ReactFlowProvider>
    </div>
  );
};

export default App;