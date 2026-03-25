const EditorSidebar = ({
  currentPlatform,
  currentStrategyName,
  commonItems,
  logs,
  resultImg,
  onBack,
  onDragStart,
  onSave,
  onRun
}) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div className="sidebar-nav">
        <button className="back-btn" onClick={onBack}>⬅️</button>
        <span style={{ fontWeight: 'bold', fontSize: 12, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
          正在编辑: {currentStrategyName}
        </span>
      </div>

      <div style={{ flex: 1, overflowY: 'auto', padding: 10 }}>
        <div style={{ marginBottom: 15 }}>
          <div style={{ fontSize: 12, color: '#999', marginBottom: 5 }}>专属动作</div>
          {currentPlatform?.items?.map((item) => (
            <div
              key={item.type}
              className="dndnode"
              onDragStart={(event) => onDragStart(event, item.type, item.label)}
              draggable
              style={{ borderLeft: `3px solid ${currentPlatform.color}` }}
            >
              {item.label}
            </div>
          ))}
        </div>

        <div>
          <div style={{ fontSize: 12, color: '#999', marginBottom: 5 }}>公共动作</div>
          {commonItems.map((item) => (
            <div
              key={item.type}
              className="dndnode"
              onDragStart={(event) => onDragStart(event, item.type, item.label)}
              draggable
            >
              {item.label}
            </div>
          ))}
        </div>
      </div>

      <div style={{ padding: 10, borderTop: '1px solid #eee', display: 'flex', flexDirection: 'column', gap: 5 }}>
        <button className="run-btn" style={{ background: '#fff', color: '#333', border: '1px solid #ccc' }} onClick={onSave}>💾 保存</button>
        <button className="run-btn" onClick={onRun} style={{ background: currentPlatform?.color || '#4CAF50' }}>▶ 运行</button>
      </div>

      {logs.length > 0 && (
        <div style={{ height: 100, overflowY: 'auto', fontSize: 10, background: '#eee', padding: 5 }}>
          {logs.map((log, index) => <div key={index}>{log}</div>)}
        </div>
      )}
      {resultImg && <img src={resultImg} style={{ width: '100%' }} />}
    </div>
  );
};

export default EditorSidebar;