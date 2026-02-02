#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
场外基金实时估值查询示例
演示如何使用fund_api查询指定基金的实时估值

作者: JavaEdge
日期: 2025-02-01
"""

from fund_api import FundAPI


def query_single_fund(fund_code: str):
    """
    查询单个基金的实时估值

    :param fund_code: 6位基金代码
    """
    api = FundAPI()

    print(f"\n🎯 开始查询基金 {fund_code} 的实时估值\n")

    # 获取基金实时估值
    fund_info = api.get_fund_realtime_value(fund_code)

    if fund_info:
        # 打印格式化的基金信息
        api.print_fund_info(fund_info)

        # 也可以直接访问字典数据
        print("📝 原始数据字典:")
        print(f"   {fund_info}")

        return fund_info
    else:
        print(f"❌ 无法获取基金 {fund_code} 的数据")
        return None


def main():
    """主函数"""
    print("=" * 80)
    print("  场外基金实时估值查询工具")
    print("=" * 80)

    # 示例1: 查询华夏成长混合 (000001)
    print("\n【示例1】查询 华夏成长混合 (000001)")
    print("-" * 80)
    query_single_fund("000001")

    # 示例2: 查询易方达黄金主题 (161116)
    print("\n【示例2】查询 易方达黄金主题 (161116)")
    print("-" * 80)
    query_single_fund("161116")

    # 示例3: 查询一个不存在的基金代码
    print("\n【示例3】查询不存在的基金 (999999)")
    print("-" * 80)
    query_single_fund("999999")

    # 示例4: 用户自定义查询
    print("\n" + "=" * 80)
    print("  自定义查询")
    print("=" * 80)

    while True:
        fund_code = input("\n请输入基金代码(6位数字，输入q退出): ").strip()

        if fund_code.lower() == 'q':
            print("\n👋 感谢使用，再见！")
            break

        if len(fund_code) != 6 or not fund_code.isdigit():
            print("❌ 基金代码格式错误，请输入6位数字")
            continue

        query_single_fund(fund_code)


if __name__ == "__main__":
    # 直接运行时，只执行前三个示例，不进入交互模式
    # 如果需要交互模式，取消下面的注释
    # main()

    # 快速查询模式
    print("=" * 80)
    print("  场外基金实时估值查询工具")
    print("=" * 80)

    # 直接查询几个常见基金
    funds_to_query = [
        ("000001", "华夏成长混合"),
        ("161116", "易方达黄金主题"),
        ("110022", "易方达消费行业"),
    ]

    for fund_code, fund_name in funds_to_query:
        print(f"\n查询 {fund_name} ({fund_code})")
        print("-" * 80)
        query_single_fund(fund_code)
