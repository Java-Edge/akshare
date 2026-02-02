#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
快速测试API功能
验证API是否可以正常工作

作者: JavaEdge
日期: 2025-02-01
"""

print("正在测试API模块...")
print("=" * 80)

# 测试1: 导入模块
print("\n【测试1】导入模块")
try:
    from fund_estimate_api import (
        app, fund_api, fund_db,
        parse_estimate_rate,
        calculate_change_amount,
        convert_to_fund_estimate
    )
    print("✅ 所有模块导入成功")
except Exception as e:
    print(f"❌ 导入失败: {e}")
    exit(1)

# 测试2: 测试辅助函数
print("\n【测试2】测试辅助函数")
try:
    # 测试解析增长率
    rate1 = parse_estimate_rate("0.65%")
    print(f"✅ 解析 '0.65%' = {rate1}")

    rate2 = parse_estimate_rate("-0.03%")
    print(f"✅ 解析 '-0.03%' = {rate2}")

    # 测试计算涨跌额
    amount = calculate_change_amount(1.1806, 0.65)
    print(f"✅ 计算涨跌额 (1.1806, 0.65%) = {amount}")

except Exception as e:
    print(f"❌ 辅助函数测试失败: {e}")
    exit(1)

# 测试3: 测试fund_api
print("\n【测试3】测试fund_api查询")
try:
    fund_info = fund_api.get_fund_realtime_value("000001")
    if fund_info:
        print(f"✅ 查询成功: {fund_info['基金名称']}")
        print(f"   净值: {fund_info['实时估算净值']}")
        print(f"   涨跌: {fund_info['实时估算增长率']}")
    else:
        print("⚠️  查询返回空数据")
except Exception as e:
    print(f"❌ 查询失败: {e}")
    import traceback
    traceback.print_exc()

# 测试4: 测试数据转换
print("\n【测试4】测试数据转换")
try:
    if fund_info:
        estimate_data = convert_to_fund_estimate(fund_info)
        print("✅ 转换成功:")
        print(f"   code: {estimate_data['code']}")
        print(f"   estimateNav: {estimate_data['estimateNav']}")
        print(f"   estimateChange: {estimate_data['estimateChange']}")
        print(f"   estimateChangeAmount: {estimate_data['estimateChangeAmount']}")
except Exception as e:
    print(f"❌ 转换失败: {e}")
    import traceback
    traceback.print_exc()

# 测试5: 数据库状态
print("\n【测试5】数据库状态")
if fund_db:
    print("✅ 数据库已连接")
    try:
        # 测试保存数据
        if fund_info:
            success = fund_db.save_estimate(fund_info)
            print(f"✅ 保存测试: {'成功' if success else '失败'}")
    except Exception as e:
        print(f"⚠️  数据库操作失败: {e}")
else:
    print("⚠️  数据库未连接（将以纯API模式运行）")

# 测试6: Flask app
print("\n【测试6】Flask应用")
try:
    with app.test_client() as client:
        # 测试健康检查
        response = client.get('/api/health')
        print(f"✅ 健康检查接口: {response.status_code}")

        # 测试基金查询接口
        response = client.get('/api/fund/estimate/000001')
        print(f"✅ 基金查询接口: {response.status_code}")

        if response.status_code == 200:
            data = response.get_json()
            if data.get('success'):
                print(f"✅ 返回数据格式正确")
            else:
                print(f"⚠️  返回失败: {data.get('message')}")

except Exception as e:
    print(f"❌ Flask测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("✅ API功能测试完成")
print("=" * 80)
print("\n💡 提示:")
print("   1. 运行 'python fund_estimate_api.py' 启动服务")
print("   2. 运行 'python test_api_client.py' 进行完整测试")
print("   3. 查看 'API_DOCUMENTATION.md' 了解API使用方法")
print()
