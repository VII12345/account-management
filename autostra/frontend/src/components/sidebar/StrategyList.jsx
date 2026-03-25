const StrategyList = ({ currentPlatform, currentAccount, strategyList, onBack, onStrategyClick, onCreateNew }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div className="sidebar-nav">
        <button className="back-btn" onClick={onBack}>⬅️</button>
        <span style={{ fontWeight: 'bold' }}>
          {currentPlatform?.name} / {currentAccount || '-'} / 策略库
        </span>
      </div>
      <div style={{ flex: 1, overflowY: 'auto' }}>
        {strategyList.length === 0 && <div style={{ padding: 20, color: '#999', fontSize: 12 }}>暂无策略，请新建</div>}
        {strategyList.map((name) => (
          <div key={name} className="strategy-item" onClick={() => onStrategyClick(name)}>
            📄 {name}
          </div>
        ))}
      </div>
      <div style={{ padding: 10, borderTop: '1px solid #eee' }}>
        <button className="run-btn" onClick={onCreateNew}>+ 新建策略</button>
      </div>
    </div>
  );
};

export default StrategyList;