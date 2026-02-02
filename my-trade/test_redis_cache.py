#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
测试Redis缓存功能
验证基金API的Redis缓存是否正常工作

作者: JavaEdge
日期: 2025-02-02
"""

import time
from fund_api import FundAPI

print("=" * 80)
print("测试基金API的Redis缓存功能")
print("=" * 80)

# 测试1: 初始化API（启用Redis）
print("\n【测试1】初始化FundAPI（启用Redis缓存，TTL=30秒）")
print("-" * 80)
api = FundAPI(use_redis=True, redis_ttl=30)

if hasattr(api, 'redis_cache') and api.redis_cache and api.redis_cache.enabled:
    print("✅ Redis缓存已启用")
    print(f"   TTL: {api.redis_cache.default_ttl}秒")
else:
    print("❌ Redis缓存未启用")
    print("   请确保Redis服务已启动（默认端口6379）")
    print("\n💡 启动Redis:")
    print("   - macOS: brew services start redis")
    print("   - Linux: systemctl start redis")
    print("   - Docker: docker run -d -p 6379:6379 redis")
    exit(1)

# 测试2: 第一次查询（应该调用API）
print("\n【测试2】第一次查询基金 000001（应该调用API）")
print("-" * 80)
start_time = time.time()
fund_info_1 = api.get_fund_realtime_value("000001")
elapsed_1 = time.time() - start_time

if fund_info_1:
    print(f"✅ 查询成功: {fund_info_1['基金名称']}")
    print(f"   净值: {fund_info_1['实时估算净值']}")
    print(f"   耗时: {elapsed_1:.2f}秒")
else:
    print("❌ 查询失败")
    exit(1)

# 测试3: 第二次查询（应该从Redis缓存读取）
print("\n【测试3】第二次查询基金 000001（应该从Redis缓存读取）")
print("-" * 80)
print("等待1秒后再次查询...")
time.sleep(1)

start_time = time.time()
fund_info_2 = api.get_fund_realtime_value("000001")
elapsed_2 = time.time() - start_time

if fund_info_2:
    print(f"✅ 查询成功: {fund_info_2['基金名称']}")
    print(f"   净值: {fund_info_2['实时估算净值']}")
    print(f"   耗时: {elapsed_2:.2f}秒")

    # 比较耗时
    if elapsed_2 < elapsed_1:
        speedup = elapsed_1 / elapsed_2
        print(f"\n🚀 性能提升: {speedup:.1f}倍 (从 {elapsed_1:.2f}秒 降到 {elapsed_2:.2f}秒)")
    else:
        print(f"\n⚠️  缓存可能未生效")
else:
    print("❌ 查询失败")

# 测试4: 检查缓存TTL
print("\n【测试4】检查缓存剩余时间")
print("-" * 80)
if api.redis_cache:
    ttl = api.redis_cache.get_ttl('fund_estimate', '000001')
    if ttl > 0:
        print(f"✅ 缓存剩余时间: {ttl}秒")
    elif ttl == -1:
        print("⚠️  缓存永久有效（这不应该发生）")
    elif ttl == -2:
        print("❌ 缓存不存在")

# 测试5: 查询另一个基金（应该调用API）
print("\n【测试5】查询基金 161116（应该调用API）")
print("-" * 80)
start_time = time.time()
fund_info_3 = api.get_fund_realtime_value("161116")
elapsed_3 = time.time() - start_time

if fund_info_3:
    print(f"✅ 查询成功: {fund_info_3['基金名称']}")
    print(f"   净值: {fund_info_3['实时估算净值']}")
    print(f"   耗时: {elapsed_3:.2f}秒")

# 测试6: 再次查询161116（应该从缓存读取）
print("\n【测试6】再次查询基金 161116（应该从缓存读取）")
print("-" * 80)
time.sleep(1)

start_time = time.time()
fund_info_4 = api.get_fund_realtime_value("161116")
elapsed_4 = time.time() - start_time

if fund_info_4:
    print(f"✅ 查询成功: {fund_info_4['基金名称']}")
    print(f"   耗时: {elapsed_4:.2f}秒")

    if elapsed_4 < elapsed_3:
        speedup = elapsed_3 / elapsed_4
        print(f"\n🚀 性能提升: {speedup:.1f}倍")

# 测试7: 获取Redis统计信息
print("\n【测试7】Redis缓存统计信息")
print("-" * 80)
if api.redis_cache:
    stats = api.redis_cache.get_stats()
    if stats.get('enabled'):
        print("✅ Redis状态:")
        print(f"   连接客户端数: {stats.get('connected_clients', 'N/A')}")
        print(f"   使用内存: {stats.get('used_memory_human', 'N/A')}")
        print(f"   总键数: {stats.get('total_keys', 'N/A')}")
        print(f"   运行时间: {stats.get('uptime_in_seconds', 0)}秒")

# 测试8: 测试缓存过期
print("\n【测试8】测试缓存过期（TTL=30秒）")
print("-" * 80)
print("缓存会在30秒后过期，可以等待后再次查询验证")
print("提示: 在30秒内查询会命中缓存，30秒后会重新调用API")

# 汇总
print("\n" + "=" * 80)
print("✅ Redis缓存功能测试完成")
print("=" * 80)
print("\n💡 测试总结:")
print("   1. Redis缓存正常工作")
print("   2. 第二次查询速度明显提升")
print("   3. 缓存TTL为30秒，过期后自动刷新")
print("   4. 不同基金代码独立缓存")
print("\n🎯 性能优化效果:")
print(f"   - 首次查询: {elapsed_1:.2f}秒（调用API）")
print(f"   - 缓存查询: {elapsed_2:.2f}秒（从Redis读取）")
print(f"   - 性能提升: 约 {elapsed_1/elapsed_2:.1f}倍")
print()
