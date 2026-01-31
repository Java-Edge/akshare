#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
AKShare A股核心API快速演示 - 湖南黄金（002716）
自动运行所有API示例，无需手动干预

作者: JavaEdge
日期: 2026-01-25
"""

import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.font_manager as fm
import time

# 设置中文字体
try:
    zh_fonts = ['PingFang SC', 'Hiragino Sans GB', 'STHeiti', 'Microsoft YaHei', 'SimHei']
    for font_name in zh_fonts:
        if font_name in [f.name for f in fm.fontManager.ttflist]:
            plt.rcParams['font.sans-serif'] = [font_name]
            plt.rcParams['axes.unicode_minus'] = False
            break
except:
    pass

# 股票基本信息
STOCK_CODE = "002716"
STOCK_NAME = "湖南黄金"

print("=" * 80)
print(f"📚 AKShare A股核心API快速演示")
print(f"🎯 目标股票: {STOCK_NAME} ({STOCK_CODE})")
print(f"⏰ 演示时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)


def demo_1_basic_info():
    """演示1：获取股票基本信息"""
    print("\n" + "=" * 80)
    print("📖 演示1：获取股票基本信息")
    print("=" * 80)

    try:
        # API 1: 获取A股所有股票代码和名称
        print(f"\n【API】ak.stock_info_a_code_name()")
        print("💡 用途: 获取所有A股股票的代码和名称")
        print("⏳ 执行中...")

        all_stocks = ak.stock_info_a_code_name()
        hunan_stock = all_stocks[all_stocks['code'] == STOCK_CODE]

        print(f"✅ 成功! 数据包含 {len(all_stocks)} 只A股")
        print(f"✅ 找到股票: {hunan_stock['name'].values[0]} ({hunan_stock['code'].values[0]})")

        # API 2: 获取个股信息
        print(f"\n【API】ak.stock_individual_info_em(symbol='{STOCK_CODE}')")
        print("💡 用途: 获取个股详细信息（总市值、流通市值、PE、PB等）")
        print("⏳ 执行中...")

        stock_info = ak.stock_individual_info_em(symbol=STOCK_CODE)

        print("\n✅ 成功! 股票详细信息:")
        for _, row in stock_info.iterrows():
            print(f"  {row['item']:15s}: {row['value']}")

        return stock_info

    except Exception as e:
        print(f"❌ 错误: {e}")
        return None


def demo_2_realtime_quote():
    """演示2：获取实时行情数据"""
    print("\n" + "=" * 80)
    print("📖 演示2：获取实时行情数据")
    print("=" * 80)

    try:
        print(f"\n【API】ak.stock_zh_a_spot_em()")
        print("💡 用途: 获取A股所有股票实时行情")
        print("⏳ 执行中...")

        spot_df = ak.stock_zh_a_spot_em()
        hunan_spot = spot_df[spot_df['代码'] == STOCK_CODE]

        if not hunan_spot.empty:
            row = hunan_spot.iloc[0]
            print(f"\n✅ 成功! {STOCK_NAME} 实时行情:")
            print(f"  {'最新价':<12s}: {row['最新价']:>10.2f} 元")
            print(f"  {'涨跌幅':<12s}: {row['涨跌幅']:>9.2f}%")
            print(f"  {'涨跌额':<12s}: {row['涨跌额']:>10.2f} 元")
            print(f"  {'成交量':<12s}: {row['成交量']/10000:>10.2f} 万手")
            print(f"  {'成交额':<12s}: {row['成交额']/100000000:>10.2f} 亿元")
            print(f"  {'今开':<12s}: {row['今开']:>10.2f} 元")
            print(f"  {'最高':<12s}: {row['最高']:>10.2f} 元")
            print(f"  {'最低':<12s}: {row['最低']:>10.2f} 元")
            print(f"  {'昨收':<12s}: {row['昨收']:>10.2f} 元")
            print(f"  {'换手率':<12s}: {row['换手率']:>9.2f}%")
            print(f"  {'市盈率(动态)':<12s}: {row['市盈率-动态']:>10.2f}")
            print(f"  {'市净率':<12s}: {row['市净率']:>10.2f}")

            return hunan_spot
        else:
            print(f"⚠️  未找到 {STOCK_CODE} 的实时行情")
            return None

    except Exception as e:
        print(f"❌ 错误: {e}")
        return None


def demo_3_historical_data():
    """演示3：获取历史行情数据"""
    print("\n" + "=" * 80)
    print("📖 演示3：获取历史行情数据")
    print("=" * 80)

    try:
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=90)).strftime("%Y%m%d")

        print(f"\n【API】ak.stock_zh_a_hist(symbol='{STOCK_CODE}', period='daily', start_date='{start_date}', end_date='{end_date}')")
        print("💡 用途: 获取股票历史K线数据（日线、周线、月线等）")
        print(f"📅 查询范围: {start_date} 至 {end_date}")
        print("⏳ 执行中...")

        hist_df = ak.stock_zh_a_hist(
            symbol=STOCK_CODE,
            period="daily",
            start_date=start_date,
            end_date=end_date,
            adjust=""
        )

        print(f"\n✅ 成功! 获取 {len(hist_df)} 个交易日数据")
        print(f"\n最近5个交易日行情:")
        print(hist_df[['日期', '开盘', '收盘', '最高', '最低', '涨跌幅', '成交量']].head(5).to_string(index=False))

        print(f"\n📊 近90天统计:")
        print(f"  最高价: {hist_df['最高'].max():.2f} 元")
        print(f"  最低价: {hist_df['最低'].min():.2f} 元")
        print(f"  平均收盘价: {hist_df['收盘'].mean():.2f} 元")
        print(f"  累计涨跌幅: {hist_df['涨跌幅'].sum():.2f}%")
        print(f"  上涨天数: {len(hist_df[hist_df['涨跌幅'] > 0])}/{len(hist_df)} ({len(hist_df[hist_df['涨跌幅'] > 0])/len(hist_df)*100:.1f}%)")

        return hist_df

    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None


def demo_4_technical_indicators(hist_df):
    """演示4：技术指标计算"""
    print("\n" + "=" * 80)
    print("📖 演示4：技术指标计算")
    print("=" * 80)

    if hist_df is None or hist_df.empty:
        print("⚠️  没有历史数据，跳过技术分析")
        return None

    try:
        print("\n💡 计算技术指标: MA5, MA10, MA20, RSI, MACD, 布林带")
        print("⏳ 执行中...")

        df = hist_df.copy()

        # 移动平均线
        df['MA5'] = df['收盘'].rolling(window=5).mean()
        df['MA10'] = df['收盘'].rolling(window=10).mean()
        df['MA20'] = df['收盘'].rolling(window=20).mean()

        # RSI
        delta = df['收盘'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))

        # MACD
        exp1 = df['收盘'].ewm(span=12, adjust=False).mean()
        exp2 = df['收盘'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

        # 布林带
        df['BB_middle'] = df['收盘'].rolling(window=20).mean()
        bb_std = df['收盘'].rolling(window=20).std()
        df['BB_upper'] = df['BB_middle'] + 2 * bb_std
        df['BB_lower'] = df['BB_middle'] - 2 * bb_std

        print("\n✅ 成功! 技术指标计算完成")

        latest = df.iloc[-1]
        print(f"\n📊 最新技术指标 ({latest['日期']}):")
        print(f"  收盘价: {latest['收盘']:.2f} 元")
        print(f"  MA5:  {latest['MA5']:.2f} 元" if pd.notna(latest['MA5']) else "  MA5:  计算中...")
        print(f"  MA10: {latest['MA10']:.2f} 元" if pd.notna(latest['MA10']) else "  MA10: 计算中...")
        print(f"  MA20: {latest['MA20']:.2f} 元" if pd.notna(latest['MA20']) else "  MA20: 计算中...")
        print(f"  RSI:  {latest['RSI']:.2f}" if pd.notna(latest['RSI']) else "  RSI:  计算中...")
        print(f"  MACD: {latest['MACD']:.4f}" if pd.notna(latest['MACD']) else "  MACD: 计算中...")

        # 简单技术分析
        print(f"\n💡 技术分析提示:")
        if pd.notna(latest['MA5']) and pd.notna(latest['MA10']):
            if latest['MA5'] > latest['MA10']:
                print(f"  ✅ MA5 > MA10: 短期上升趋势")
            else:
                print(f"  ⚠️  MA5 < MA10: 短期下降趋势")

        if pd.notna(latest['RSI']):
            if latest['RSI'] > 70:
                print(f"  ⚠️  RSI = {latest['RSI']:.1f}: 超买区域")
            elif latest['RSI'] < 30:
                print(f"  💡 RSI = {latest['RSI']:.1f}: 超卖区域")
            else:
                print(f"  ✅ RSI = {latest['RSI']:.1f}: 正常区域")

        return df

    except Exception as e:
        print(f"❌ 错误: {e}")
        return None


def demo_5_financial_data():
    """演示5：获取财务数据"""
    print("\n" + "=" * 80)
    print("📖 演示5：获取财务数据")
    print("=" * 80)

    try:
        print(f"\n【API】ak.stock_financial_analysis_indicator(symbol='{STOCK_CODE}')")
        print("💡 用途: 获取股票财务分析指标（ROE、ROA、净利润增长率等）")
        print("⏳ 执行中...")

        financial_df = ak.stock_financial_analysis_indicator(symbol=STOCK_CODE)

        if not financial_df.empty:
            print(f"\n✅ 成功! 获取 {len(financial_df)} 期财务数据")

            latest = financial_df.iloc[0]
            print(f"\n📊 最新财务指标 ({latest['日期']}):")

            key_metrics = {
                'ROE': 'ROE (净资产收益率)',
                'ROA': 'ROA (总资产收益率)',
                '净利润同比增长率': '净利润同比增长',
                '营业收入同比增长率': '营收同比增长',
                '资产负债比率': '资产负债率',
                '流动比率': '流动比率',
                '速动比率': '速动比率'
            }

            for col, label in key_metrics.items():
                if col in financial_df.columns and pd.notna(latest[col]):
                    print(f"  {label:<16s}: {latest[col]:>8.2f}{'%' if '率' in col or '增长' in col else ''}")

            return financial_df
        else:
            print("⚠️  未获取到财务数据")
            return None

    except Exception as e:
        print(f"❌ 错误: {e}")
        print("💡 提示: 部分股票可能没有完整的财务数据")
        return None


def demo_6_capital_flow():
    """演示6：获取资金流向"""
    print("\n" + "=" * 80)
    print("📖 演示6：获取资金流向数据")
    print("=" * 80)

    try:
        print(f"\n【API】ak.stock_individual_fund_flow(stock='{STOCK_CODE}', market='深证')")
        print("💡 用途: 获取个股主力资金、大单、中单、小单流向")
        print("⏳ 执行中...")

        fund_flow = ak.stock_individual_fund_flow(stock=STOCK_CODE, market="深证")

        if not fund_flow.empty:
            print(f"\n✅ 成功! 获取 {len(fund_flow)} 天资金流向数据")
            print(f"\n最近5天资金流向:")
            print(fund_flow.head(5).to_string(index=False))

            latest = fund_flow.iloc[0]
            print(f"\n💰 最新资金流向 ({latest['日期']}):")
            print(f"  主力净流入: {latest['主力净流入-净额']/10000:>10.2f} 万元 ({latest['主力净流入-净占比']:>6.2f}%)")
            print(f"  超大单净流入: {latest['超大单净流入-净额']/10000:>10.2f} 万元")
            print(f"  大单净流入: {latest['大单净流入-净额']/10000:>10.2f} 万元")
            print(f"  中单净流入: {latest['中单净流入-净额']/10000:>10.2f} 万元")
            print(f"  小单净流入: {latest['小单净流入-净额']/10000:>10.2f} 万元")

            if latest['主力净流入-净额'] > 0:
                print(f"\n  💡 主力资金净流入，市场看好 📈")
            else:
                print(f"\n  ⚠️  主力资金净流出，需要谨慎 📉")

            return fund_flow
        else:
            print("⚠️  未获取到资金流向数据")
            return None

    except Exception as e:
        print(f"❌ 错误: {e}")
        print("💡 提示: 资金流向数据可能有延迟或限制")
        return None


def demo_7_industry_analysis():
    """演示7：行业板块分析"""
    print("\n" + "=" * 80)
    print("📖 演示7：行业板块分析")
    print("=" * 80)

    try:
        print(f"\n【API】ak.stock_board_industry_name_em()")
        print("💡 用途: 获取所有行业板块的涨跌幅、市值等数据")
        print("⏳ 执行中...")

        industry_df = ak.stock_board_industry_name_em()

        print(f"\n✅ 成功! 共有 {len(industry_df)} 个行业板块")
        print("\n涨幅前5的行业板块:")
        print(industry_df.sort_values('涨跌幅', ascending=False).head(5)[['板块名称', '涨跌幅', '总市值', '换手率']].to_string(index=False))

        print("\n跌幅前5的行业板块:")
        print(industry_df.sort_values('涨跌幅', ascending=True).head(5)[['板块名称', '涨跌幅', '总市值', '换手率']].to_string(index=False))

        # 黄金相关板块
        gold_industry = industry_df[industry_df['板块名称'].str.contains('黄金|贵金属', na=False)]
        if not gold_industry.empty:
            print(f"\n💎 黄金相关板块:")
            print(gold_industry[['板块名称', '涨跌幅', '总市值', '上涨家数', '下跌家数']].to_string(index=False))

        return industry_df

    except Exception as e:
        print(f"❌ 错误: {e}")
        return None


def demo_summary():
    """演示总结"""
    print("\n" + "=" * 80)
    print("📚 AKShare A股核心API总结")
    print("=" * 80)

    print("\n✅ 已演示的核心API:")
    print("  1. stock_info_a_code_name()         - 获取所有A股代码和名称")
    print("  2. stock_individual_info_em()       - 获取个股详细信息")
    print("  3. stock_zh_a_spot_em()             - 获取实时行情")
    print("  4. stock_zh_a_hist()                - 获取历史K线数据")
    print("  5. 技术指标计算                      - MA, RSI, MACD, 布林带")
    print("  6. stock_financial_analysis_indicator() - 获取财务分析指标")
    print("  7. stock_individual_fund_flow()     - 获取资金流向")
    print("  8. stock_board_industry_name_em()   - 获取行业板块数据")

    print("\n📖 更多实用API:")
    print("  • stock_zh_a_tick_tx()             - 获取分笔成交数据")
    print("  • stock_comment_em()               - 获取千股千评")
    print("  • stock_rank_forecast_cninfo()     - 获取业绩预告")
    print("  • stock_ipo_info()                 - 获取IPO信息")
    print("  • stock_market_fund_flow()         - 获取大盘资金流向")

    print("\n🎯 实战应用场景:")
    print("  1. 选股策略: 结合财务指标、技术指标筛选优质股票")
    print("  2. 趋势跟踪: 利用均线系统判断买卖时机")
    print("  3. 资金监控: 追踪主力资金动向")
    print("  4. 行业轮动: 分析行业板块强弱")
    print("  5. 风险控制: 监控波动率、回撤等风险指标")

    print("\n💡 进阶学习建议:")
    print("  • 查看 akshare_quant_guide.md 了解更多API")
    print("  • 结合 investment_advisor.py 生成AI投资建议")
    print("  • 将数据保存到MySQL数据库进行长期跟踪")
    print("  • 开发自己的量化策略并回测")

    print("\n🚀 下一步操作:")
    print("  1. 修改 STOCK_CODE 变量，分析其他股票")
    print("  2. 调整参数（时间范围、周期等）")
    print("  3. 添加更多技术指标")
    print("  4. 构建完整的量化交易系统")


def main():
    """主函数"""
    try:
        # 演示1: 基本信息
        demo_1_basic_info()
        time.sleep(1)

        # 演示2: 实时行情
        demo_2_realtime_quote()
        time.sleep(1)

        # 演示3: 历史数据
        hist_df = demo_3_historical_data()
        time.sleep(1)

        # 演示4: 技术指标
        tech_df = demo_4_technical_indicators(hist_df)
        time.sleep(1)

        # 演示5: 财务数据
        demo_5_financial_data()
        time.sleep(1)

        # 演示6: 资金流向
        demo_6_capital_flow()
        time.sleep(1)

        # 演示7: 行业分析
        demo_7_industry_analysis()
        time.sleep(1)

        # 总结
        demo_summary()

        print("\n" + "=" * 80)
        print("🎉 演示完成！")
        print("=" * 80)
        print(f"\n⏰ 完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    except KeyboardInterrupt:
        print("\n\n⚠️  演示被中断")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
