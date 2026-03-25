import axios from 'axios';

const getBaseUrl = () => `http://${window.location.hostname}:8080`;
const getAccountBaseUrl = () => import.meta.env.VITE_ACCOUNT_API_BASE || getBaseUrl();
const hasCustomAccountBase = () => Boolean(import.meta.env.VITE_ACCOUNT_API_BASE);

const normalizePlatform = (value) => String(value || '').trim().toLowerCase();

const platformAliases = {
    x: ['x', 'twitter', 'x(twitter)', 'x (twitter)'],
    youtube: ['youtube', 'yt'],
    tiktok: ['tiktok', 'tik tok'],
    facebook: ['facebook', 'fb'],
    instagram: ['instagram', 'ig'],
    threads: ['threads'],
    tinder: ['tinder']
};

const isSamePlatform = (accountPlatform, selectedPlatform) => {
    const selected = normalizePlatform(selectedPlatform);
    if (!selected) return true;

    const account = normalizePlatform(accountPlatform);
    if (!account) return true;

    const aliases = platformAliases[selected] || [selected];
    return aliases.includes(account);
};

const mapAccountRow = (row) => {
    if (Array.isArray(row)) {
        const id = row[0];
        const username = row[2] || `账号_${id}`;
        const platform = row[1] || '';
        return { id: String(id), name: String(username), platform: String(platform) };
    }

    const id = row?.id;
    const username = row?.username || `账号_${id}`;
    const platform = row?.platform || '';
    return { id: String(id), name: String(username), platform: String(platform) };
};

export const fetchStatsApi = () => axios.get(`${getBaseUrl()}/stats`);

export const listAccountsApi = (platformId) => {
    return axios
        .get(`${getAccountBaseUrl()}/accounts/`, {
            params: {
                page: 1,
                page_size: 20
            }
        })
        .then((res) => {
            const contentType = res.headers?.['content-type'] || '';
            if (contentType.includes('text/html') || typeof res.data === 'string') {
                throw new Error('账号接口返回了 HTML 页面，请检查 Nginx /api 反向代理是否正确转发到后端。');
            }

            const rows = Array.isArray(res.data?.data) ? res.data.data : [];
            const allAccounts = rows
                .map(mapAccountRow)
                .map((item) => ({ id: item.id, name: item.name, platform: item.platform }));

            const matchedAccounts = allAccounts.filter((item) => isSamePlatform(item.platform, platformId));
            const visibleAccounts = matchedAccounts.length > 0 ? matchedAccounts : allAccounts;
            const accounts = visibleAccounts.map((item) => ({ id: item.id, name: item.name }));

            return { data: { accounts } };
        })
        .catch((error) => {
            if (hasCustomAccountBase()) {
                throw error;
            }

            return axios.get(`${getBaseUrl()}/accounts/${platformId}`).then((res) => {
                const accounts = (res.data?.accounts || []).map((item) => ({
                    id: String(item),
                    name: String(item)
                }));
                return { data: { accounts } };
            });
        });
};

export const listStrategiesApi = (platformId, accountId) => {
    return axios.get(`${getBaseUrl()}/list/${platformId}`, {
        params: { account_id: accountId }
    });
};

export const loadStrategyApi = (platformId, accountId, strategyName) => {
    return axios.get(`${getBaseUrl()}/load/${platformId}/${strategyName}`, {
        params: { account_id: accountId }
    });
};

export const saveStrategyApi = (platformId, accountId, strategyName, payload) => {
    return axios.post(`${getBaseUrl()}/save/${platformId}/${strategyName}`, payload, {
        params: { account_id: accountId }
    });
};

export const runStrategyApi = (payload) => {
    return axios.post(`${getBaseUrl()}/run`, payload);
};