#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
AKShare A股核心API快速测试 - 湖南黄金（002716）
快速演示最重要的几个API

作者: JavaEdge
日期: 2026-01-25
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

STOCK_CODE = "002716"
STOCK_NAME = "湖南黄金"

print("=" * 80)
print(f"🚀 AKShare A股核心API快速测试 - {STOCK_NAME} ({STOCK_CODE})")
print("=" * 80)

# API 1: 获取实时行情
print("\n【API 1】获取实时行情")
print(f"ak.stock_zh_a_spot_em()")
try:
    spot_df = ak.stock_zh_a_spot_em()
    hunan = spot_df[spot_df['代码'] == STOCK_CODE]
    if not hunan.empty:
        row = hunan.iloc[0]
        print(f"✅ {STOCK_NAME} 实时行情:")
        print(f"  最新价: {row['最新价']:.2f} 元")
        print(f"  涨跌幅: {row['涨跌幅']:.2f}%")
        print(f"  成交额: {row['成交额']/100000000:.2f} 亿")
        print(f"  市盈率: {row['市盈率-动态']:.2f}")
except Exception as e:
    print(f"❌ 错误: {e}")

# API 2: 获取历史数据
print("\n【API 2】获取历史K线数据")
end_date = datetime.now().strftime("%Y%m%d")
start_date = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")
print(f"ak.stock_zh_a_hist(symbol='{STOCK_CODE}', start_date='{start_date}', end_date='{end_date}')")
try:
    hist_df = ak.stock_zh_a_hist(
        symbol=STOCK_CODE,
        period="daily",
        start_date=start_date,
        end_date=end_date,
        adjust=""
    )
    print(f"✅ 成功获取 {len(hist_df)} 个交易日数据")
    print(f"\n最近5天行情:")
    print(hist_df[['日期', '收盘', '涨跌幅', '成交量']].head(5).to_string(index=False))

    # 计算技术指标
    hist_df['MA5'] = hist_df['收盘'].rolling(window=5).mean()
    hist_df['MA10'] = hist_df['收盘'].rolling(window=10).mean()
    latest = hist_df.iloc[-1]
    print(f"\n📊 技术指标:")
    print(f"  MA5:  {latest['MA5']:.2f} 元")
    print(f"  MA10: {latest['MA10']:.2f} 元")
    print(f"  累计涨跌幅: {hist_df['涨跌幅'].sum():.2f}%")
except Exception as e:
    print(f"❌ 错误: {e}")

# API 3: 获取个股信息
print("\n【API 3】获取个股详细信息")
print(f"ak.stock_individual_info_em(symbol='{STOCK_CODE}')")
try:
    info_df = ak.stock_individual_info_em(symbol=STOCK_CODE)
    print(f"✅ 股票详细信息:")
    for _, row in info_df.head(10).iterrows():
        print(f"  {row['item']}: {row['value']}")
except Exception as e:
    print(f"❌ 错误: {e}")

# API 4: 获取行业板块
print("\n【API 4】获取行业板块数据")
print(f"ak.stock_board_industry_name_em()")
try:
    industry_df = ak.stock_board_industry_name_em()
    print(f"✅ 共有 {len(industry_df)} 个行业板块")
    gold_industry = industry_df[industry_df['板块名称'].str.contains('黄金', na=False)]
    if not gold_industry.empty:
        print(f"\n💎 黄金板块:")
        print(gold_industry[['板块名称', '涨跌幅', '总市值']].to_string(index=False))
except Exception as e:
    print(f"❌ 错误: {e}")

print("\n" + "=" * 80)
print("✅ 核心API测试完成!")
print("=" * 80)

print("\n📚 已测试的API:")
print("  1. stock_zh_a_spot_em()             - 实时行情")
print("  2. stock_zh_a_hist()                - 历史K线")
print("  3. stock_individual_info_em()       - 个股信息")
print("  4. stock_board_industry_name_em()   - 行业板块")

print("\n💡 更多功能请查看:")
print("  • stock_demo_hunan_silver.py - 完整演示版本")
print("  • stock_tutorial_hunan_silver.py - 互动教程版本")
print("  • akshare_quant_guide.md - 完整API文档")
