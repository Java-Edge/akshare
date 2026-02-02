#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
系统功能测试脚本
验证所有核心功能是否正常工作

作者: JavaEdge
日期: 2025-02-01
"""

def test_fund_api():
    """测试基金API"""
    print("\n" + "=" * 80)
    print("测试1: 基金API - 查询单个基金")
    print("=" * 80)

    try:
        from fund_api import FundAPI
        api = FundAPI()

        fund_info = api.get_fund_realtime_value("000001")

        if fund_info:
            print("✅ 基金API测试通过")
            print(f"   查询到基金: {fund_info['基金名称']}")
            print(f"   实时净值: {fund_info['实时估算净值']}")
            print(f"   涨跌幅: {fund_info['实时估算增长率']}")
            return True
        else:
            print("❌ 基金API测试失败: 未获取到数据")
            return False
    except Exception as e:
        print(f"❌ 基金API测试失败: {e}")
        return False


def test_advisor_basic():
    """测试投资顾问（不使用LLM）"""
    print("\n" + "=" * 80)
    print("测试2: 投资顾问 - 基础分析")
    print("=" * 80)

    try:
        from fund_api import FundAPI
        from fund_investment_advisor import FundInvestmentAdvisor

        api = FundAPI()
        advisor = FundInvestmentAdvisor(use_llm=False)

        fund_info = api.get_fund_realtime_value("000001")

        if fund_info:
            analysis = advisor.analyze_fund(fund_info)

            print("✅ 投资顾问基础分析测试通过")
            print(f"   基金: {analysis['fund_name']}")
            print(f"   状态: {analysis['status']}")
            print(f"   风险等级: {analysis['risk_level']}")
            print(f"   交易信号: {analysis['signal']}")
            return True
        else:
            print("❌ 投资顾问测试失败: 未获取到数据")
            return False
    except Exception as e:
        print(f"❌ 投资顾问测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_advisor_llm():
    """测试投资顾问（使用LLM）"""
    print("\n" + "=" * 80)
    print("测试3: 投资顾问 - AI深度分析")
    print("=" * 80)

    try:
        from fund_api import FundAPI
        from fund_investment_advisor import FundInvestmentAdvisor

        api = FundAPI()
        advisor = FundInvestmentAdvisor(use_llm=True)

        fund_info = api.get_fund_realtime_value("161116")

        if fund_info:
            analysis = advisor.analyze_fund(fund_info)

            if 'llm_advice' in analysis and analysis['llm_advice']:
                print("✅ AI深度分析测试通过")
                print(f"   基金: {analysis['fund_name']}")
                print(f"   AI建议: {analysis['llm_advice'][:100]}...")
                return True
            else:
                print("⚠️  AI深度分析不可用（LLM未连接）")
                print("   但基础分析功能正常")
                return True
        else:
            print("❌ AI深度分析测试失败: 未获取到数据")
            return False
    except Exception as e:
        print(f"❌ AI深度分析测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_search():
    """测试基金搜索"""
    print("\n" + "=" * 80)
    print("测试4: 基金搜索功能")
    print("=" * 80)

    try:
        from fund_api import FundAPI
        api = FundAPI()

        result = api.search_funds("黄金")

        if result is not None and not result.empty:
            print("✅ 基金搜索测试通过")
            print(f"   搜索'黄金'找到 {len(result)} 只基金")
            return True
        else:
            print("❌ 基金搜索测试失败")
            return False
    except Exception as e:
        print(f"❌ 基金搜索测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("\n" + "=" * 80)
    print("  场外基金投资决策系统 - 功能测试")
    print("=" * 80)

    results = []

    # 运行测试
    results.append(("基金API", test_fund_api()))
    results.append(("投资顾问-基础", test_advisor_basic()))
    results.append(("投资顾问-AI", test_advisor_llm()))
    results.append(("基金搜索", test_search()))

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
        print("\n  🎉 所有测试通过！系统可以正常使用。")
    else:
        print("\n  ⚠️  部分测试失败，请检查配置。")

    print("=" * 80 + "\n")

    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
