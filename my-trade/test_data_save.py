#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
测试数据保存逻辑（不使用LLM）
"""

if __name__ == "__main__":
    import subprocess
    import sys

    # 运行主程序但跳过LLM和绘图
    print("=" * 70)
    print("测试数据保存逻辑")
    print("=" * 70)

    # 导入必要的模块
    import akshare as ak
    import pandas as pd
    from datetime import datetime, timedelta
    import pymysql
    import database_config

    # 导入函数
    import importlib.util
    spec = importlib.util.spec_from_file_location("qdii", "qdii-stock-plan.py")
    qdii = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(qdii)

    fund_code = "513100"
    days = 30

    print(f"\n正在获取基金 {fund_code} 近{days}个交易日数据...")
    df, new_data = qdii.get_qdii_fund_data(fund_code, days)

    print(f"\n完整数据: {len(df)} 条")
    print(f"新数据: {len(new_data)} 条")

    if not new_data.empty:
        print(f"\n💾 正在保存 {len(new_data)} 条新数据到数据库...")
        print(f"新数据日期范围: {new_data['日期'].min()} 至 {new_data['日期'].max()}")
        qdii.save_to_database(new_data, fund_code)
    else:
        print(f"\n✅ 无需保存，数据库已是最新")

    print("\n测试完成！")
