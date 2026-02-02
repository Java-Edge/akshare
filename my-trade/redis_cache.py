#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Redis缓存模块
用于缓存基金估值数据，避免频繁调用API

作者: JavaEdge
日期: 2025-02-02
"""

import redis
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class RedisCache:
    """Redis缓存管理类"""

    def __init__(self, host: str = 'localhost', port: int = 6379,
                 db: int = 0, password: Optional[str] = None,
                 default_ttl: int = 30):
        """
        初始化Redis缓存

        :param host: Redis主机地址
        :param port: Redis端口
        :param db: Redis数据库编号
        :param password: Redis密码
        :param default_ttl: 默认过期时间（秒），默认30秒
        """
        self.default_ttl = default_ttl
        self.redis_client = None
        self.enabled = False

        try:
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2
            )
            # 测试连接
            self.redis_client.ping()
            self.enabled = True
            logger.info(f"✅ Redis缓存已启用 (TTL: {default_ttl}秒)")
        except Exception as e:
            logger.warning(f"⚠️  Redis连接失败: {e}，缓存功能已禁用")
            self.redis_client = None
            self.enabled = False

    def _generate_key(self, prefix: str, key: str) -> str:
        """
        生成Redis键名

        :param prefix: 键前缀
        :param key: 键值
        :return: 完整的Redis键名
        """
        return f"{prefix}:{key}"

    def get(self, prefix: str, key: str) -> Optional[Dict]:
        """
        从缓存获取数据

        :param prefix: 键前缀，如 'fund_estimate'
        :param key: 键值，如基金代码 '000001'
        :return: 缓存的数据字典，不存在返回None
        """
        if not self.enabled:
            return None

        try:
            redis_key = self._generate_key(prefix, key)
            data = self.redis_client.get(redis_key)

            if data:
                logger.debug(f"✅ Redis缓存命中: {redis_key}")
                return json.loads(data)
            else:
                logger.debug(f"⚪ Redis缓存未命中: {redis_key}")
                return None

        except Exception as e:
            logger.warning(f"⚠️  Redis获取数据失败: {e}")
            return None

    def set(self, prefix: str, key: str, value: Dict, ttl: Optional[int] = None) -> bool:
        """
        设置缓存数据

        :param prefix: 键前缀
        :param key: 键值
        :param value: 要缓存的数据字典
        :param ttl: 过期时间（秒），不指定则使用默认值
        :return: 是否设置成功
        """
        if not self.enabled:
            return False

        try:
            redis_key = self._generate_key(prefix, key)
            expire_time = ttl if ttl is not None else self.default_ttl

            # 添加缓存时间戳
            cache_data = {
                **value,
                '_cached_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            self.redis_client.setex(
                redis_key,
                expire_time,
                json.dumps(cache_data, ensure_ascii=False)
            )

            logger.debug(f"✅ Redis缓存已设置: {redis_key} (TTL: {expire_time}秒)")
            return True

        except Exception as e:
            logger.warning(f"⚠️  Redis设置数据失败: {e}")
            return False

    def delete(self, prefix: str, key: str) -> bool:
        """
        删除缓存数据

        :param prefix: 键前缀
        :param key: 键值
        :return: 是否删除成功
        """
        if not self.enabled:
            return False

        try:
            redis_key = self._generate_key(prefix, key)
            result = self.redis_client.delete(redis_key)

            if result:
                logger.debug(f"✅ Redis缓存已删除: {redis_key}")
                return True
            else:
                logger.debug(f"⚪ Redis缓存不存在: {redis_key}")
                return False

        except Exception as e:
            logger.warning(f"⚠️  Redis删除数据失败: {e}")
            return False

    def exists(self, prefix: str, key: str) -> bool:
        """
        检查缓存是否存在

        :param prefix: 键前缀
        :param key: 键值
        :return: 是否存在
        """
        if not self.enabled:
            return False

        try:
            redis_key = self._generate_key(prefix, key)
            return bool(self.redis_client.exists(redis_key))
        except Exception as e:
            logger.warning(f"⚠️  Redis检查存在失败: {e}")
            return False

    def get_ttl(self, prefix: str, key: str) -> int:
        """
        获取缓存剩余过期时间

        :param prefix: 键前缀
        :param key: 键值
        :return: 剩余秒数，-1表示永久，-2表示不存在
        """
        if not self.enabled:
            return -2

        try:
            redis_key = self._generate_key(prefix, key)
            return self.redis_client.ttl(redis_key)
        except Exception as e:
            logger.warning(f"⚠️  Redis获取TTL失败: {e}")
            return -2

    def clear_prefix(self, prefix: str) -> int:
        """
        清空指定前缀的所有缓存

        :param prefix: 键前缀
        :return: 删除的键数量
        """
        if not self.enabled:
            return 0

        try:
            pattern = f"{prefix}:*"
            keys = self.redis_client.keys(pattern)

            if keys:
                count = self.redis_client.delete(*keys)
                logger.info(f"✅ 清空Redis缓存: {pattern} ({count}个键)")
                return count
            else:
                logger.debug(f"⚪ 没有匹配的Redis缓存: {pattern}")
                return 0

        except Exception as e:
            logger.warning(f"⚠️  Redis清空缓存失败: {e}")
            return 0

    def get_stats(self) -> Dict[str, Any]:
        """
        获取Redis缓存统计信息

        :return: 统计信息字典
        """
        if not self.enabled:
            return {
                'enabled': False,
                'message': 'Redis未启用'
            }

        try:
            info = self.redis_client.info()
            return {
                'enabled': True,
                'connected_clients': info.get('connected_clients', 0),
                'used_memory_human': info.get('used_memory_human', 'N/A'),
                'total_keys': self.redis_client.dbsize(),
                'uptime_in_seconds': info.get('uptime_in_seconds', 0)
            }
        except Exception as e:
            logger.warning(f"⚠️  获取Redis统计失败: {e}")
            return {
                'enabled': False,
                'error': str(e)
            }

    def close(self):
        """关闭Redis连接"""
        if self.redis_client:
            try:
                self.redis_client.close()
                logger.info("Redis连接已关闭")
            except Exception as e:
                logger.warning(f"⚠️  关闭Redis连接失败: {e}")


# 全局Redis缓存实例
_redis_cache = None


def get_redis_cache(host: str = 'localhost', port: int = 6379,
                    db: int = 0, password: Optional[str] = None,
                    ttl: int = 30) -> RedisCache:
    """
    获取全局Redis缓存实例（单例模式）

    :param host: Redis主机
    :param port: Redis端口
    :param db: 数据库编号
    :param password: 密码
    :param ttl: 默认过期时间（秒）
    :return: RedisCache实例
    """
    global _redis_cache

    if _redis_cache is None:
        _redis_cache = RedisCache(
            host=host,
            port=port,
            db=db,
            password=password,
            default_ttl=ttl
        )

    return _redis_cache


def test_redis_cache():
    """测试Redis缓存功能"""
    print("=" * 80)
    print("测试Redis缓存功能")
    print("=" * 80)

    # 创建缓存实例
    cache = RedisCache(default_ttl=5)

    if not cache.enabled:
        print("❌ Redis未启用，无法测试")
        return

    # 测试1: 设置和获取
    print("\n【测试1】设置和获取缓存")
    test_data = {
        'code': '000001',
        'name': '华夏成长混合',
        'value': 1.1806
    }

    success = cache.set('test', 'fund_001', test_data, ttl=10)
    print(f"设置缓存: {'✅ 成功' if success else '❌ 失败'}")

    cached_data = cache.get('test', 'fund_001')
    if cached_data:
        print(f"获取缓存: ✅ 成功")
        print(f"  数据: {cached_data}")
    else:
        print(f"获取缓存: ❌ 失败")

    # 测试2: TTL
    print("\n【测试2】检查TTL")
    ttl = cache.get_ttl('test', 'fund_001')
    print(f"剩余过期时间: {ttl}秒")

    # 测试3: 存在性检查
    print("\n【测试3】检查存在性")
    exists = cache.exists('test', 'fund_001')
    print(f"缓存存在: {'✅ 是' if exists else '❌ 否'}")

    # 测试4: 删除
    print("\n【测试4】删除缓存")
    deleted = cache.delete('test', 'fund_001')
    print(f"删除缓存: {'✅ 成功' if deleted else '❌ 失败'}")

    exists_after = cache.exists('test', 'fund_001')
    print(f"删除后存在: {'❌ 仍存在' if exists_after else '✅ 已删除'}")

    # 测试5: 统计信息
    print("\n【测试5】获取统计信息")
    stats = cache.get_stats()
    print(f"统计信息:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\n" + "=" * 80)
    print("✅ 测试完成")
    print("=" * 80)


if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    test_redis_cache()
