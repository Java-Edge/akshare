#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
基金估值API测试客户端
测试所有API接口功能

作者: JavaEdge
日期: 2025-02-01
"""

import requests
import json
from typing import Dict, List

API_BASE_URL = "http://localhost:5000/api"


def test_health_check():
    """测试健康检查接口"""
    print("\n" + "=" * 80)
    print("【测试1】健康检查")
    print("=" * 80)

    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_single_fund_estimate():
    """测试单个基金估值查询"""
    print("\n" + "=" * 80)
    print("【测试2】查询单个基金估值")
    print("=" * 80)

    fund_code = "000001"
    print(f"查询基金代码: {fund_code}")

    try:
        response = requests.get(f"{API_BASE_URL}/fund/estimate/{fund_code}")
        print(f"状态码: {response.status_code}")

        result = response.json()
        print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")

        if result.get('success'):
            data = result['data']
            print(f"\n✅ 查询成功:")
            print(f"   基金代码: {data['code']}")
            print(f"   估算净值: {data['estimateNav']}")
            print(f"   涨跌幅: {data['estimateChange']}%")
            print(f"   涨跌额: {data['estimateChangeAmount']}")
            print(f"   估算时间: {data['estimateTime']}")
            print(f"   是否缓存: {result.get('cached', False)}")
            return True
        else:
            print(f"❌ 查询失败: {result.get('message')}")
            return False

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_batch_fund_estimate():
    """测试批量基金估值查询"""
    print("\n" + "=" * 80)
    print("【测试3】批量查询基金估值")
    print("=" * 80)

    fund_codes = ["000001", "161116", "999999"]  # 最后一个是不存在的
    print(f"查询基金代码: {fund_codes}")

    try:
        response = requests.post(
            f"{API_BASE_URL}/fund/estimate/batch",
            json={"codes": fund_codes},
            headers={"Content-Type": "application/json"}
        )
        print(f"状态码: {response.status_code}")

        result = response.json()

        if result.get('success'):
            print(f"\n✅ 查询成功: {result.get('message')}")
            print(f"\n成功获取 {len(result['data'])} 个基金估值:")

            for data in result['data']:
                print(f"\n  基金代码: {data['code']}")
                print(f"  估算净值: {data['estimateNav']}")
                print(f"  涨跌幅: {data['estimateChange']}%")

            if result.get('failed'):
                print(f"\n失败 {len(result['failed'])} 个:")
                for failed in result['failed']:
                    print(f"  {failed['code']}: {failed['reason']}")

            return True
        else:
            print(f"❌ 查询失败: {result.get('message')}")
            return False

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_search_funds():
    """测试基金搜索"""
    print("\n" + "=" * 80)
    print("【测试4】搜索基金")
    print("=" * 80)

    keyword = "黄金"
    print(f"搜索关键词: {keyword}")

    try:
        response = requests.get(f"{API_BASE_URL}/fund/search?keyword={keyword}")
        print(f"状态码: {response.status_code}")

        result = response.json()

        if result.get('success'):
            print(f"\n✅ {result.get('message')}")

            for fund in result['data'][:5]:  # 只显示前5个
                print(f"\n  代码: {fund['code']}")
                print(f"  名称: {fund['name']}")
                print(f"  净值: {fund['estimateNav']}")
                print(f"  涨跌: {fund['estimateChange']}%")

            if len(result['data']) > 5:
                print(f"\n  ... 还有 {len(result['data']) - 5} 个结果")

            return True
        else:
            print(f"❌ 搜索失败: {result.get('message')}")
            return False

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_fund_history():
    """测试历史估值查询"""
    print("\n" + "=" * 80)
    print("【测试5】查询历史估值数据")
    print("=" * 80)

    fund_code = "000001"
    days = 7
    print(f"查询基金代码: {fund_code}")
    print(f"查询天数: {days}")

    try:
        response = requests.get(f"{API_BASE_URL}/fund/history/{fund_code}?days={days}")
        print(f"状态码: {response.status_code}")

        result = response.json()

        if result.get('success'):
            print(f"\n✅ {result.get('message')}")

            for record in result['data'][:3]:  # 只显示前3条
                print(f"\n  估算时间: {record['estimateTime']}")
                print(f"  净值: {record['estimateNav']}")
                print(f"  涨跌: {record['estimateChange']}%")

            if len(result['data']) > 3:
                print(f"\n  ... 还有 {len(result['data']) - 3} 条记录")

            return True
        else:
            print(f"⚠️  {result.get('message')}")
            print("   提示: 历史数据需要先有数据入库")
            return True  # 这个测试允许失败（数据库可能还没数据）

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_error_handling():
    """测试错误处理"""
    print("\n" + "=" * 80)
    print("【测试6】错误处理")
    print("=" * 80)

    # 测试无效的基金代码
    print("\n测试无效的基金代码格式:")
    try:
        response = requests.get(f"{API_BASE_URL}/fund/estimate/abc")
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"错误信息: {result.get('message')}")

        if response.status_code == 400:
            print("✅ 错误处理正确")
            return True
        else:
            print("❌ 错误处理不正确")
            return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("\n" + "=" * 80)
    print("  基金估值API测试客户端")
    print("=" * 80)
    print("\n⚠️  请确保API服务已启动 (python fund_estimate_api.py)")
    print("   服务地址: http://localhost:5000")

    input("\n按回车键开始测试...")

    # 运行所有测试
    results = []

    results.append(("健康检查", test_health_check()))
    results.append(("单个基金查询", test_single_fund_estimate()))
    results.append(("批量基金查询", test_batch_fund_estimate()))
    results.append(("基金搜索", test_search_funds()))
    results.append(("历史数据查询", test_fund_history()))
    results.append(("错误处理", test_error_handling()))

    # 汇总结果
    print("\n" + "=" * 80)
    print("  测试结果汇总")
    print("=" * 80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name:20s} : {status}")

    print("\n" + "-" * 80)
    print(f"  总计: {passed}/{total} 项测试通过")

    if passed == total:
        print("\n  🎉 所有测试通过！API服务正常工作。")
    else:
        print("\n  ⚠️  部分测试失败，请检查API服务状态。")

    print("=" * 80 + "\n")

    return passed == total


if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ 测试过程出错: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
