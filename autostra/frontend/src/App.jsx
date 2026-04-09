/**
 * 文件注释：autostra/frontend/src/App.jsx
 *
 * 职责：封装当前模块的初始化、常量、工具函数或组件逻辑。
 * 边界：仅承担本模块职责，不在此处定义跨模块业务规则。
 */

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
  deleteStrategyApi,
  deletePublicStrategyApi,
  savePublicStrategyApi,
  listPublicStrategiesApi,
  getPublicStrategyTargetsApi,
  updatePublicStrategyTargetsApi,
  runStrategyApi
} from './services/autostraApi';
import { getNextNodeId } from './utils/nodeFactory';
import PlatformList from './components/sidebar/PlatformList';
import AccountList from './components/sidebar/AccountList';
import StrategyList from './components/sidebar/StrategyList';
import EditorSidebar from './components/sidebar/EditorSidebar';
import FlowCanvas from './components/editor/FlowCanvas';

const PUBLIC_STRATEGY_ACCOUNT = { id: '__public__', name: '公共策略' };
const PUBLIC_TEMPLATE_ACCOUNT = { id: '__public__', name: '公共策略模板' };
const DEFAULT_CDP_URL = 'http://127.0.0.1:9222';

const App = () => {
  const reactFlowWrapper = useRef(null);

  // --- 视图状态 ---
  const [viewMode, setViewMode] = useState('platforms'); // 'platforms' | 'accounts' | 'strategies' | 'editor'
  const [currentPlatform, setCurrentPlatform] = useState(null); // 当前选中的平台对象
  const [currentAccount, setCurrentAccount] = useState(null); // { id, name }
  const [selectedStrategyAccountIds, setSelectedStrategyAccountIds] = useState([]); // 公共策略模式下勾选账号
  const [currentStrategyName, setCurrentStrategyName] = useState(null); // 当前选中的策略文件名

  // --- 数据状态 ---
  const [stats, setStats] = useState({}); // { x: 5, youtube: 12 }
  const [accountList, setAccountList] = useState([]); // [{ id, name, account_ip, account_port }]
  const [strategyList, setStrategyList] = useState([]); // ['strategy1', 'test2']
  const [publicStrategyTargetsMap, setPublicStrategyTargetsMap] = useState({}); // { strategyName: ['a1', 'a2'] }

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

  const isPublicStrategyMode = currentAccount?.id === PUBLIC_STRATEGY_ACCOUNT.id;
  const effectiveAccount = isPublicStrategyMode ? PUBLIC_TEMPLATE_ACCOUNT : currentAccount;
  const selectedTargetAccounts = accountList.filter((account) => selectedStrategyAccountIds.includes(account.id));

  const buildCdpUrlByAccount = (account) => {
    if (!account) return DEFAULT_CDP_URL;
    const host = account.account_ip;
    const port = account.account_port;
    if (!host || !port) return DEFAULT_CDP_URL;
    return `http://${host}:${port}`;
  };

  const currentExecutionAccount = isPublicStrategyMode
    ? selectedTargetAccounts[0]
    : accountList.find((item) => item.id === effectiveAccount?.id);
  const currentCdpUrl = buildCdpUrlByAccount(currentExecutionAccount);

  const fetchStrategiesForAccount = async (account) => {
    if (!currentPlatform || !account?.id) {
      setStrategyList([]);
      return;
    }

    try {
      const res = await listStrategiesApi(currentPlatform.id, account.id);
      setStrategyList(res.data.strategies || []);
    } catch {
      setStrategyList([]);
    }
  };

  const handlePlatformClick = async (platform) => {
    setCurrentPlatform(platform);
    setCurrentAccount(null);
    setSelectedStrategyAccountIds([]);
    setCurrentStrategyName(null);
    setStrategyList([]);
    setPublicStrategyTargetsMap({});
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
    setSelectedStrategyAccountIds([account.id]);
    setCurrentStrategyName(null);
    setPublicStrategyTargetsMap({});
    setViewMode('strategies');

    await fetchStrategiesForAccount(account);
  };

  const handlePublicStrategyClick = async () => {
    if (!currentPlatform) return;

    setCurrentAccount(PUBLIC_STRATEGY_ACCOUNT);
    setCurrentStrategyName(null);
    setViewMode('strategies');

    setSelectedStrategyAccountIds(accountList.map((account) => account.id));

    // 加载公共策略列表
    try {
      const res = await listPublicStrategiesApi(currentPlatform.id);
      const strategies = res.data.strategies || [];
      setStrategyList(strategies);

      const targetPairs = await Promise.all(
        strategies.map(async (strategyName) => {
          try {
            const targetRes = await getPublicStrategyTargetsApi(currentPlatform.id, strategyName);
            return [strategyName, targetRes.data.targets || []];
          } catch {
            return [strategyName, []];
          }
        })
      );
      setPublicStrategyTargetsMap(Object.fromEntries(targetPairs));
    } catch {
      setStrategyList([]);
      setPublicStrategyTargetsMap({});
    }
  };

  const handleToggleStrategyAccount = (accountId) => {
    setSelectedStrategyAccountIds((prev) => {
      if (prev.includes(accountId)) {
        return prev.filter((id) => id !== accountId);
      }
      return [...prev, accountId];
    });
  };

  const handleStrategyClick = async (name) => {
    try {
      if (!currentAccount) {
        alert('请先选择账号');
        return;
      }

      // 如果是公共策略模式，从 __public__ 账号加载
      const loadAccountId = isPublicStrategyMode ? '__public__' : effectiveAccount.id;

      if (isPublicStrategyMode) {
        try {
          const targetRes = await getPublicStrategyTargetsApi(currentPlatform.id, name);
          const targetIds = targetRes.data.targets || [];
          setSelectedStrategyAccountIds(targetIds);
          setPublicStrategyTargetsMap((prev) => ({
            ...prev,
            [name]: targetIds
          }));
        } catch {
          setSelectedStrategyAccountIds([]);
        }
      }

      const res = await loadStrategyApi(currentPlatform.id, loadAccountId, name);
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

  const handleDeleteStrategy = async (name) => {
    if (!currentPlatform) return;
    if (!name) return;

    const confirmed = window.confirm(`确认删除策略 "${name}" 吗？\n仅删除策略，不会删除账号。`);
    if (!confirmed) return;

    try {
      if (isPublicStrategyMode) {
        await deletePublicStrategyApi(currentPlatform.id, name);
        setPublicStrategyTargetsMap((prev) => {
          const next = { ...prev };
          delete next[name];
          return next;
        });
      } else {
        await deleteStrategyApi(currentPlatform.id, effectiveAccount?.id, name);
      }

      setStrategyList((prev) => prev.filter((item) => item !== name));

      if (currentStrategyName === name) {
        setCurrentStrategyName(null);
        setNodes([...DEFAULT_NODES]);
        setEdges([]);
        setViewMode('strategies');
      }

      alert(`✅ 策略 "${name}" 已删除（账号未删除）`);
      fetchStats();
    } catch (error) {
      console.error(error);
      alert('❌ 删除策略失败');
    }
  };

  const handleSave = async (showTip = true) => {
    if (!currentPlatform) return;
    if (currentPlatform.id === 'common') return;
    if (!effectiveAccount) {
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
      cdp_url: currentCdpUrl
    };

    try {
      if (isPublicStrategyMode) {
        if (selectedStrategyAccountIds.length === 0) {
          if (showTip) alert('请至少勾选一个目标账号');
          return;
        }

        // 调用新的公共策略 API，传递 targetAccounts 参数
        await savePublicStrategyApi(currentPlatform.id, currentStrategyName, payload, selectedStrategyAccountIds);
        setPublicStrategyTargetsMap((prev) => ({
          ...prev,
          [currentStrategyName]: [...selectedStrategyAccountIds]
        }));

        if (showTip) {
          alert(`✅ [${currentPlatform.name}] 公共策略 "${currentStrategyName}" 已同步到 ${selectedStrategyAccountIds.length} 个账号`);
        }
      } else {
        await saveStrategyApi(currentPlatform.id, effectiveAccount.id, currentStrategyName, payload);

        if (showTip) {
          alert(`✅ [${currentPlatform.name}/${effectiveAccount.name}] 策略 "${currentStrategyName}" 已保存！`);
        }
      }

      fetchStats();
    } catch (e) {
      console.error(e);
      if (showTip) alert('❌ 保存失败，请检查后端');
    }
  };

  const handleUpdatePublicTargets = async () => {
    if (!isPublicStrategyMode) return;
    if (!currentStrategyName) {
      alert('请先选择一个公共策略');
      return;
    }
    if (selectedStrategyAccountIds.length === 0) {
      alert('请至少选择一个作用账号');
      return;
    }

    try {
      await updatePublicStrategyTargetsApi(currentPlatform.id, currentStrategyName, selectedStrategyAccountIds);
      setPublicStrategyTargetsMap((prev) => ({
        ...prev,
        [currentStrategyName]: [...selectedStrategyAccountIds]
      }));
      alert(`✅ 已更新公共策略 "${currentStrategyName}" 的作用账号`);
    } catch (error) {
      console.error(error);
      alert('❌ 更新作用账号失败');
    }
  };

  const handleRun = async () => {
    if (!currentPlatform) return;
    setLoading(true);
    setLogs([]);
    setResultImg(null);

    await handleSave(false);

    const payload = {
      nodes,
      edges,
      cdp_url: currentCdpUrl,
      group_id: currentPlatform.id,
      strategy_name: currentStrategyName,
      is_public: isPublicStrategyMode,
      account_id: isPublicStrategyMode ? null : effectiveAccount?.id,
      target_account_ids: isPublicStrategyMode ? selectedStrategyAccountIds : []
    };

    try {
      const res = await runStrategyApi(payload);
      if (res.data.status === 'success' || res.data.status === 'partial_success') {
        setLogs(res.data.logs);
        setResultImg(res.data.screenshot);
        if (res.data.mode === 'multi') {
          alert(`✅ [${currentPlatform.name}/公共策略] 执行完成：${res.data.success_count}/${res.data.total_count}\n后端已按账号端口并发连接浏览器`);
        } else {
          alert(`✅ [${currentPlatform.name}/${effectiveAccount?.name || '-'}] 执行完成！\n目标: ${currentCdpUrl}`);
        }
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
    if (!currentPlatform) return;
    await fetchStrategiesForAccount(effectiveAccount);
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
          onPublicStrategyClick={handlePublicStrategyClick}
        />
      );
    }

    if (viewMode === 'strategies') {
      return (
        <StrategyList
          currentPlatform={currentPlatform}
          currentAccount={currentAccount?.name}
          strategyList={strategyList}
          strategyTargetsMap={publicStrategyTargetsMap}
          onBack={() => setViewMode('accounts')}
          onStrategyClick={handleStrategyClick}
          onCreateNew={handleCreateNew}
          showAccountSelector={isPublicStrategyMode}
          accountOptions={accountList}
          selectedAccountIds={selectedStrategyAccountIds}
          onToggleAccount={handleToggleStrategyAccount}
          onUpdateTargets={handleUpdatePublicTargets}
          onDeleteStrategy={handleDeleteStrategy}
        />
      );
    }

    if (viewMode === 'editor') {
      return (
        <EditorSidebar
          currentPlatform={currentPlatform}
          currentStrategyName={currentStrategyName}
          isPublicStrategyMode={isPublicStrategyMode}
          accountOptions={accountList}
          selectedAccountIds={selectedStrategyAccountIds}
          onToggleAccount={handleToggleStrategyAccount}
          onUpdateTargets={handleUpdatePublicTargets}
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