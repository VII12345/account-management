/**
 * 文件注释：autostra/frontend/src/services/autostraApi.js
 *
 * 职责：封装当前模块的初始化、常量、工具函数或组件逻辑。
 * 边界：仅承担本模块职责，不在此处定义跨模块业务规则。
 */

import axios from 'axios';

const getCoreApiBaseUrl = () => {
    const configuredBase = import.meta.env.VITE_ACCOUNT_API_BASE;
    if (configuredBase) {
        return configuredBase.replace(/\/$/, '');
    }

    return '/account-api';
};

const getAccountApiBaseUrl = () => {
    const configuredBase = import.meta.env.VITE_YANGHAO_API_BASE;
    if (configuredBase) {
        return configuredBase.replace(/\/$/, '');
    }

    return '/api';
};

const getAccountFallbackBaseUrl = () => `http://${window.location.hostname}:8080`;

const appendQueryArray = (baseUrl, params = {}) => {
    const query = new URLSearchParams();

    Object.entries(params).forEach(([key, value]) => {
        if (value === undefined || value === null) {
            return;
        }

        if (Array.isArray(value)) {
            value.forEach((item) => query.append(key, item));
            return;
        }

        query.append(key, value);
    });

    const queryString = query.toString();
    return queryString ? `${baseUrl}?${queryString}` : baseUrl;
};

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
        const accountIp = row[9] || '';
        const accountPort = row[10] || null;
        return {
            id: String(id),
            name: String(username),
            platform: String(platform),
            account_ip: accountIp ? String(accountIp) : '',
            account_port: accountPort !== null && accountPort !== undefined ? Number(accountPort) : null
        };
    }

    const id = row?.id ?? row?.account_id ?? row?.email ?? row?.username;
    const username = row?.username || row?.name || row?.account_id || row?.email || `账号_${id}`;
    const platform = row?.platform || row?.group_id || '';
    const accountIp = row?.account_ip || row?.ip || '';
    const accountPort = row?.account_port ?? row?.port ?? null;
    return {
        id: String(id),
        name: String(username),
        platform: String(platform),
        account_ip: accountIp ? String(accountIp) : '',
        account_port: accountPort !== null && accountPort !== undefined ? Number(accountPort) : null
    };
};

const parseAccountsResponse = (data) => {
    if (Array.isArray(data?.data)) {
        return data.data.map((item) => {
            const mapped = mapAccountRow(item);
            return {
                id: mapped.id,
                name: mapped.name,
                platform: mapped.platform,
                account_ip: mapped.account_ip,
                account_port: mapped.account_port
            };
        });
    }

    if (Array.isArray(data?.accounts)) {
        return data.accounts.map((item) => {
            if (typeof item === 'string' || typeof item === 'number') {
                const id = String(item);
                return { id, name: id, platform: '' };
            }

            const mapped = mapAccountRow(item);
            return {
                id: mapped.id,
                name: mapped.name,
                platform: mapped.platform,
                account_ip: mapped.account_ip,
                account_port: mapped.account_port
            };
        });
    }

    return [];
};

export const fetchStatsApi = () => axios.get(`${getCoreApiBaseUrl()}/stats`);

export const listAccountsApi = (platformId) => {
    const params = {
        page: 1,
        page_size: 20
    };

    const requestAccounts = (baseUrl) => {
        return axios.get(`${baseUrl}/accounts/`, { params }).then((res) => {
            const contentType = res.headers?.['content-type'] || '';
            if (contentType.includes('text/html') || typeof res.data === 'string') {
                throw new Error('账号接口返回了 HTML 页面');
            }

            const allAccounts = parseAccountsResponse(res.data);
            const matchedAccounts = allAccounts.filter((item) => isSamePlatform(item.platform, platformId));
            const visibleAccounts = matchedAccounts.length > 0 ? matchedAccounts : allAccounts;

            const accounts = visibleAccounts.map((item) => ({
                id: item.id,
                name: item.name,
                account_ip: item.account_ip || '',
                account_port: item.account_port ?? null
            }));

            return { data: { accounts } };
        });
    };

    return requestAccounts(getAccountApiBaseUrl()).catch(() =>
        requestAccounts(getAccountFallbackBaseUrl()).catch(() => {
            throw new Error('账号接口不可用，请检查 /api 反向代理或 8080 端口连通性。');
        })
    );
};

export const listStrategiesApi = (platformId, accountId) => {
    return axios.get(`${getCoreApiBaseUrl()}/list/${platformId}`, {
        params: { account_id: accountId }
    });
};

export const loadStrategyApi = (platformId, accountId, strategyName) => {
    return axios.get(`${getCoreApiBaseUrl()}/load/${platformId}/${strategyName}`, {
        params: { account_id: accountId }
    });
};

export const saveStrategyApi = (platformId, accountId, strategyName, payload) => {
    return axios.post(`${getCoreApiBaseUrl()}/save/${platformId}/${strategyName}`, payload, {
        params: { account_id: accountId }
    });
};

export const deleteStrategyApi = (platformId, accountId, strategyName) => {
    return axios.delete(`${getCoreApiBaseUrl()}/delete/${platformId}/${strategyName}`, {
        params: { account_id: accountId, is_public: false }
    });
};

export const deletePublicStrategyApi = (platformId, strategyName) => {
    return axios.delete(`${getCoreApiBaseUrl()}/delete/${platformId}/${strategyName}`, {
        params: { is_public: true }
    });
};

export const runStrategyApi = (payload) => {
    return axios.post(`${getCoreApiBaseUrl()}/run`, payload);
};

// ============ 公共策略 API ============

export const savePublicStrategyApi = (platformId, strategyName, payload, targetAccounts) => {
    const url = appendQueryArray(`${getCoreApiBaseUrl()}/save-public/${platformId}/${strategyName}`, {
        target_accounts: targetAccounts
    });
    return axios.post(url, payload);
};

export const listPublicStrategiesApi = (platformId) => {
    return axios.get(`${getCoreApiBaseUrl()}/list-public/${platformId}`);
};

export const getPublicStrategyTargetsApi = (platformId, strategyName) => {
    return axios.get(`${getCoreApiBaseUrl()}/public-targets/${platformId}/${strategyName}`);
};

export const updatePublicStrategyTargetsApi = (platformId, strategyName, targetAccounts) => {
    const url = appendQueryArray(`${getCoreApiBaseUrl()}/update-public-targets/${platformId}/${strategyName}`, {
        target_accounts: targetAccounts
    });
    return axios.post(url);
};