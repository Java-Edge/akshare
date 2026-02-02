#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
每日基金监控和投资决策工具
用于每日跟踪自选基金，获取投资建议，辅助买卖决策

作者: JavaEdge
日期: 2025-02-01
"""

import sys
from datetime import datetime
from fund_api import FundAPI
from fund_investment_advisor import FundInvestmentAdvisor


# 我的自选基金列表
MY_FUNDS = [
    ("000001", "华夏成长混合"),
    ("161116", "易方达黄金主题"),
    # 在这里添加更多自选基金
    # ("基金代码", "基金名称"),
]


def print_header():
    """打印标题"""
    print("\n" + "=" * 100)
    print(f"  📊 每日基金监控报告 - {datetime.now().strftime('%Y年%m月%d日 %H:%M')}")
    print("=" * 100)


def print_summary(results):
    """打印汇总信息"""
    print("\n" + "=" * 100)
    print("  📈 今日汇总")
    print("=" * 100)

    # 统计各类信号
    signals = {}
    for result in results:
        signal = result.get('signal', 'N/A')
        base_signal = signal.split('(')[0].strip()  # 去掉括号内的说明
        signals[base_signal] = signals.get(base_signal, 0) + 1

    print(f"\n  监控基金数: {len(results)}")
    print(f"  信号分布:")
    for signal, count in signals.items():
        print(f"    - {signal}: {count} 只")

    # 涨跌统计
    up_count = sum(1 for r in results if r.get('rate_value', 0) > 0)
    down_count = sum(1 for r in results if r.get('rate_value', 0) < 0)
    flat_count = len(results) - up_count - down_count

    print(f"\n  涨跌分布:")
    print(f"    - 上涨: {up_count} 只 🔴")
    print(f"    - 下跌: {down_count} 只 🟢")
    print(f"    - 平盘: {flat_count} 只 ⚪")

    print("\n" + "=" * 100)


def monitor_daily(use_llm=True, detailed=True):
    """
    每日监控主函数

    :param use_llm: 是否使用AI分析
    :param detailed: 是否显示详细信息
    """
    if not MY_FUNDS:
        print("❌ 请先在 MY_FUNDS 中添加自选基金！")
        return

    print_header()
    print(f"\n  使用AI分析: {'是 🤖' if use_llm else '否'}")
    print(f"  详细模式: {'是' if detailed else '否'}")

    # 初始化
    api = FundAPI()
    advisor = FundInvestmentAdvisor(use_llm=use_llm)

    results = []

    # 逐个分析基金
    for i, (fund_code, fund_name) in enumerate(MY_FUNDS, 1):
        print(f"\n{'-' * 100}")
        print(f"[{i}/{len(MY_FUNDS)}] 正在分析: {fund_name} ({fund_code})")
        print(f"{'-' * 100}")

        # 获取基金数据
        fund_info = api.get_fund_realtime_value(fund_code)

        if fund_info:
            # 分析并生成建议
            analysis = advisor.analyze_fund(fund_info)
            results.append(analysis)

            if detailed:
                # 详细模式：显示完整分析
                advisor.print_advice(analysis)
            else:
                # 简要模式：只显示关键信息
                print(f"\n  📊 {analysis.get('fund_name', 'N/A')}")
                print(f"  💰 净值: {analysis.get('current_value', 'N/A')}  |  "
                      f"涨跌: {analysis.get('estimation_rate', 'N/A')} {analysis.get('status_emoji', '')}")
                print(f"  🎯 建议: {analysis.get('signal', 'N/A')}")

                if use_llm and 'llm_advice' in analysis:
                    llm_text = analysis['llm_advice']
                    # 只显示操作建议部分
                    if '操作建议' in llm_text:
                        advice_line = [line for line in llm_text.split('\n') if '操作建议' in line]
                        if advice_line:
                            print(f"  🤖 {advice_line[0].strip()}")
        else:
            print(f"  ❌ 无法获取基金数据")

    # 打印汇总
    if results:
        print_summary(results)

    print(f"\n⚠️  风险提示: 以上建议仅供参考，投资需谨慎！")
    print(f"📅 报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


def interactive_mode():
    """交互模式：查询任意基金"""
    print("\n" + "=" * 100)
    print("  🔍 基金查询模式")
    print("=" * 100)
    print("\n  输入基金代码查询投资建议，输入 'q' 退出")

    api = FundAPI()
    advisor = FundInvestmentAdvisor(use_llm=True)

    while True:
        print("\n" + "-" * 100)
        fund_code = input("请输入基金代码 (6位数字): ").strip()

        if fund_code.lower() == 'q':
            print("\n👋 再见！")
            break

        if len(fund_code) != 6 or not fund_code.isdigit():
            print("❌ 基金代码格式错误，请输入6位数字")
            continue

        print(f"\n正在分析基金 {fund_code}...\n")

        # 获取并分析
        fund_info = api.get_fund_realtime_value(fund_code)

        if fund_info:
            analysis = advisor.analyze_fund(fund_info)
            advisor.print_advice(analysis)
        else:
            print("❌ 无法获取基金数据，请检查基金代码是否正确")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='每日基金监控和投资决策工具')
    parser.add_argument('--no-llm', action='store_true', help='不使用AI分析')
    parser.add_argument('--simple', action='store_true', help='简要模式（不显示详细信息）')
    parser.add_argument('--interactive', action='store_true', help='交互查询模式')

    args = parser.parse_args()

    if args.interactive:
        # 交互模式
        interactive_mode()
    else:
        # 监控模式
        monitor_daily(
            use_llm=not args.no_llm,
            detailed=not args.simple
        )


if __name__ == "__main__":
    # 如果没有参数，直接运行默认监控
    if len(sys.argv) == 1:
        print("\n💡 提示: 使用 --help 查看更多选项")
        print("   示例: python daily_monitor.py --simple  # 简要模式")
        print("         python daily_monitor.py --no-llm   # 不使用AI")
        print("         python daily_monitor.py --interactive  # 交互查询模式")

        # 运行默认监控（使用AI，详细模式）
        monitor_daily(use_llm=True, detailed=True)
    else:
        main()
