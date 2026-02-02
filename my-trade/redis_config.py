# Redis缓存配置
REDIS_CONFIG = {
    'host': 'localhost',      # Redis主机地址
    'port': 6379,             # Redis端口
    'db': 0,                  # 数据库编号
    'password': None,         # Redis密码（如果有）
    'default_ttl': 30         # 默认过期时间（秒）
}

# 缓存键前缀配置
CACHE_PREFIX = {
    'fund_estimate': 'fund_estimate',    # 基金估值缓存前缀
    'fund_search': 'fund_search',        # 基金搜索缓存前缀
    'fund_history': 'fund_history'       # 历史数据缓存前缀
}
