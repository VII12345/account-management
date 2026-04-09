/**
 * 文件注释：autostra/frontend/src/components/sidebar/EditorSidebar.jsx
 *
 * 职责：封装当前模块的初始化、常量、工具函数或组件逻辑。
 * 边界：仅承担本模块职责，不在此处定义跨模块业务规则。
 */

import { useState } from 'react';

const EditorSidebar = ({
  currentPlatform,
  currentStrategyName,
  isPublicStrategyMode = false,
  accountOptions = [],
  selectedAccountIds = [],
  onToggleAccount,
  onUpdateTargets,
  commonItems,
  logs,
  resultImg,
  onBack,
  onDragStart,
  onSave,
  onRun
}) => {
  const [isPreviewOpen, setIsPreviewOpen] = useState(false);
  const accountNameMap = Object.fromEntries(accountOptions.map((account) => [account.id, account.name]));

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div className="sidebar-nav">
        <button className="back-btn" onClick={onBack}>⬅️</button>
        <span style={{ fontWeight: 'bold', fontSize: 12, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
          正在编辑: {currentStrategyName}
        </span>
      </div>

      <div style={{ flex: 1, overflowY: 'auto', padding: 10 }}>
        {isPublicStrategyMode && (
          <div style={{ marginBottom: 15, padding: 10, border: '1px solid #e6eaff', borderRadius: 8, background: '#fafbff' }}>
            <div style={{ fontSize: 12, color: '#2457ff', marginBottom: 8, fontWeight: 'bold' }}>公共策略作用账号</div>
            <div style={{ maxHeight: 160, overflowY: 'auto', border: '1px solid #e5e5e5', borderRadius: 6, background: '#fff' }}>
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
            <div style={{ marginTop: 8, fontSize: 11, color: '#666' }}>
              当前已选：{selectedAccountIds.length > 0 ? selectedAccountIds.map((accountId) => accountNameMap[accountId] || accountId).join('、') : '未选择'}
            </div>
            <button
              className="run-btn"
              onClick={() => onUpdateTargets?.()}
              style={{ marginTop: 8, background: '#f3f6ff', color: '#2457ff', border: '1px solid #cdd8ff' }}
            >
              更新作用账号
            </button>
          </div>
        )}

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
      {resultImg && (
        <div style={{ borderTop: '1px solid #eee', padding: 8, background: '#fafafa' }}>
          <div style={{ fontSize: 11, color: '#666', marginBottom: 6 }}>运行结果截图（点击可放大）</div>
          <img
            src={resultImg}
            onClick={() => setIsPreviewOpen(true)}
            style={{
              width: '100%',
              maxHeight: 180,
              objectFit: 'cover',
              cursor: 'zoom-in',
              borderRadius: 6,
              border: '1px solid #e5e7eb'
            }}
          />
        </div>
      )}

      {isPreviewOpen && resultImg && (
        <div
          onClick={() => setIsPreviewOpen(false)}
          style={{
            position: 'fixed',
            inset: 0,
            zIndex: 2000,
            background: 'rgba(0, 0, 0, 0.82)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: 20,
            cursor: 'zoom-out'
          }}
        >
          <img
            src={resultImg}
            onClick={(event) => event.stopPropagation()}
            style={{
              maxWidth: '92vw',
              maxHeight: '92vh',
              borderRadius: 8,
              boxShadow: '0 12px 48px rgba(0, 0, 0, 0.45)'
            }}
          />
          <button
            onClick={() => setIsPreviewOpen(false)}
            style={{
              position: 'fixed',
              top: 16,
              right: 16,
              width: 36,
              height: 36,
              borderRadius: 18,
              border: '1px solid rgba(255,255,255,0.5)',
              background: 'rgba(0,0,0,0.45)',
              color: '#fff',
              fontSize: 20,
              lineHeight: '34px',
              cursor: 'pointer'
            }}
          >
            ×
          </button>
        </div>
      )}
    </div>
  );
};

export default EditorSidebar;