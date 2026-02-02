#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
快速开始示例
最简单的基金查询和投资建议示例

作者: JavaEdge
日期: 2025-02-01
"""

print("正在加载模块...")

from fund_api import FundAPI
from fund_investment_advisor import FundInvestmentAdvisor

print("✅ 模块加载成功\n")

# 创建实例
api = FundAPI()
advisor = FundInvestmentAdvisor(use_llm=False)  # 先不用AI，速度快

print("=" * 80)
print("  场外基金投资决策快速示例")
print("=" * 80)

# 示例1: 查询华夏成长混合
print("\n【示例1】查询基金实时估值")
print("-" * 80)

fund_code = "000001"
print(f"查询基金: {fund_code}")

fund_info = api.get_fund_realtime_value(fund_code)

if fund_info:
    print(f"✅ 查询成功")
    print(f"   基金名称: {fund_info['基金名称']}")
    print(f"   实时净值: {fund_info['实时估算净值']}")
    print(f"   涨跌幅: {fund_info['实时估算增长率']}")
else:
    print("❌ 查询失败")

# 示例2: 获取投资建议
print("\n【示例2】获取投资建议")
print("-" * 80)

if fund_info:
    analysis = advisor.analyze_fund(fund_info)

    print(f"基金: {analysis['fund_name']}")
    print(f"状态: {analysis['status']} {analysis['status_emoji']}")
    print(f"风险: {analysis['risk_level']}")
    print(f"建议: {analysis['signal']}")

print("\n" + "=" * 80)
print("✅ 示例完成！")
print("=" * 80)
print("\n💡 提示:")
print("   - 修改 fund_code 变量可查询其他基金")
print("   - 设置 use_llm=True 可启用AI深度分析")
print("   - 查看 README_FUND_ADVISOR.md 了解更多用法")
print()
