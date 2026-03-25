export const PLATFORMS = [
    {
        id: 'x',
        name: 'X (Twitter)',
        icon: '𝕏',
        color: '#000000',
        items: [
            { type: 'login_x', label: '🔑 登录账号' },
            { type: 'like_x', label: '❤️ 随机点赞' },
            { type: 'zhuan_x', label: '🔁 随机转发' },
            { type: 'post_x', label: '📝 发布推文' }
        ]
    },
    {
        id: 'youtube',
        name: 'YouTube',
        icon: '▶️',
        color: '#ff0000',
        items: [
            { type: 'youtube_login', label: '🔑 打开网站' },
            { type: 'youtube_search', label: '👀 搜索视频' },
            { type: 'youtube_watch', label: '🔔 观看视频' },
            { type: 'youtube_interact', label: '🔔 订阅频道' },
            { type: 'youtube_like', label: '🔔 视频点赞' }
        ]
    },
    {
        id: 'tiktok',
        name: 'TikTok',
        icon: '🎵',
        color: '#00f2ea',
        items: [
            { type: 'swipe_tk', label: '👆 刷视频' },
            { type: 'like_tk', label: '❤️ 双击点赞' }
        ]
    },
    { id: 'instagram', name: 'Instagram', icon: '📷', color: '#E1306C', items: [] },
    { id: 'facebook', name: 'Facebook', icon: '📘', color: '#1877f2', items: [{ type: 'login_fb', label: '🔑 登录FB' }] },
    { id: 'threads', name: 'Threads', icon: '🌀', color: '#000000', items: [] },
    { id: 'tinder', name: 'Tinder', icon: '🔥', color: '#fe3c72', items: [] },
    {
        id: 'common',
        name: '公共动作',
        icon: '🧩',
        color: '#333',
        items: [
            { type: 'loop_start', label: '🔄 循环开始' },
            { type: 'wait', label: '⏳ 等待时间' }
        ]
    }
];

export const getCommonItems = () => {
    return PLATFORMS.find((platform) => platform.id === 'common')?.items || [];
};