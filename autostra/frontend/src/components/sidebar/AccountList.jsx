const AccountList = ({ currentPlatform, accountList, onBack, onAccountClick, onPublicStrategyClick }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div className="sidebar-nav">
        <button className="back-btn" onClick={onBack}>⬅️</button>
        <span style={{ fontWeight: 'bold' }}>{currentPlatform?.name} 账号</span>
      </div>

      <div style={{ flex: 1, overflowY: 'auto' }}>
        <div className="strategy-item" onClick={onPublicStrategyClick}>
          🌐 公共策略
        </div>
        {accountList.length === 0 && <div style={{ padding: 20, color: '#999', fontSize: 12 }}>暂无账号</div>}
        {accountList.map((account) => (
          <div key={account.id} className="strategy-item" onClick={() => onAccountClick(account)}>
            👤 {account.name}
          </div>
        ))}
      </div>
    </div>
  );
};

export default AccountList;