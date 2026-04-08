const StrategyList = ({
  currentPlatform,
  currentAccount,
  strategyList,
  strategyTargetsMap = {},
  onBack,
  onStrategyClick,
  onCreateNew,
  showAccountSelector = false,
  accountOptions = [],
  selectedAccountIds = [],
  onToggleAccount,
  onUpdateTargets,
  onDeleteStrategy
}) => {
  const accountNameMap = Object.fromEntries(accountOptions.map((account) => [account.id, account.name]));

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div className="sidebar-nav">
        <button className="back-btn" onClick={onBack}>⬅️</button>
        <span style={{ fontWeight: 'bold' }}>
          {currentPlatform?.name} / {currentAccount || '-'} / 策略库
        </span>
      </div>
      {showAccountSelector && (
        <div style={{ padding: '10px', borderBottom: '1px solid #eee' }}>
          <div style={{ fontSize: 12, color: '#666', marginBottom: 6 }}>作用账号（可多选）</div>
          <div style={{ maxHeight: 140, overflowY: 'auto', border: '1px solid #eee', borderRadius: 6 }}>
            {accountOptions.map((account) => (
              <label
                key={account.id}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 8,
                  padding: '8px 10px',
                  borderBottom: '1px solid #f5f5f5',
                  cursor: 'pointer'
                }}
              >
                <input
                  type="checkbox"
                  checked={selectedAccountIds.includes(account.id)}
                  onChange={() => onToggleAccount?.(account.id)}
                />
                <span style={{ fontSize: 13 }}>{account.name}</span>
              </label>
            ))}
            {accountOptions.length === 0 && (
              <div style={{ padding: '8px 10px', color: '#999', fontSize: 12 }}>暂无可选账号</div>
            )}
          </div>
        </div>
      )}
      <div style={{ flex: 1, overflowY: 'auto' }}>
        {strategyList.length === 0 && <div style={{ padding: 20, color: '#999', fontSize: 12 }}>暂无策略，请新建</div>}
        {strategyList.map((name) => {
          const targets = strategyTargetsMap[name] || [];
          return (
            <div key={name} className="strategy-item" onClick={() => onStrategyClick(name)}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 8 }}>
                <span>📄 {name}</span>
                <button
                  onClick={(event) => {
                    event.stopPropagation();
                    onDeleteStrategy?.(name);
                  }}
                  style={{
                    border: '1px solid #ffd2d2',
                    color: '#c62828',
                    background: '#fff5f5',
                    borderRadius: 6,
                    fontSize: 11,
                    padding: '2px 6px',
                    cursor: 'pointer'
                  }}
                >
                  删除
                </button>
              </div>
              {showAccountSelector && (
                <div style={{ marginTop: 4, fontSize: 11, color: '#777', lineHeight: 1.4 }}>
                  作用账号：{targets.length > 0 ? targets.map((accountId) => accountNameMap[accountId] || accountId).join('、') : '未绑定'}
                </div>
              )}
            </div>
          );
        })}
      </div>
      <div style={{ padding: 10, borderTop: '1px solid #eee' }}>
        <button className="run-btn" onClick={onCreateNew}>+ 新建策略</button>
        {showAccountSelector && (
          <button
            className="run-btn"
            onClick={() => onUpdateTargets?.()}
            style={{ marginTop: 8, background: '#f3f6ff', color: '#2457ff', border: '1px solid #cdd8ff' }}
          >
            更新作用账号
          </button>
        )}
      </div>
    </div>
  );
};

export default StrategyList;