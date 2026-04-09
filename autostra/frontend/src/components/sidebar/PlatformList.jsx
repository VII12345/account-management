/**
 * 文件注释：autostra/frontend/src/components/sidebar/PlatformList.jsx
 *
 * 职责：封装当前模块的初始化、常量、工具函数或组件逻辑。
 * 边界：仅承担本模块职责，不在此处定义跨模块业务规则。
 */

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