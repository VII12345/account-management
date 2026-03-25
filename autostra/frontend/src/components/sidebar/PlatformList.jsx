const PlatformList = ({ platforms, stats, onPlatformClick }) => {
  return (
    <div className="platform-list">
      <div style={{ padding: '15px', fontWeight: 'bold', fontSize: '16px' }}>📚 选择平台</div>
      {platforms.map((platform) => (
        <div key={platform.id} className="platform-item" onClick={() => onPlatformClick(platform)}>
          <div className="platform-left">
            <span className="platform-icon" style={{ color: platform.color }}>{platform.icon}</span>
            <span>{platform.name}</span>
          </div>
          <div className="badge-count">{stats[platform.id] || 0}</div>
        </div>
      ))}
    </div>
  );
};

export default PlatformList;