#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
AKShare A股核心API实战教程 - 湖南黄金（002716）
通过实际操作学习AKShare的核心功能

作者: JavaEdge
日期: 2026-01-25
"""

import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.font_manager as fm

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
print(f"📚 AKShare A股核心API实战教程")
print(f"🎯 目标股票: {STOCK_NAME} ({STOCK_CODE})")
print("=" * 80)


def lesson_1_basic_info():
    """第1课：获取股票基本信息"""
    print("\n" + "=" * 80)
    print("📖 第1课：获取股票基本信息")
    print("=" * 80)

    print(f"\n🔍 正在查询 {STOCK_NAME} 的基本信息...")

    try:
        # API 1: 获取A股所有股票代码和名称
        print("\n【API 1】ak.stock_info_a_code_name() - 获取所有A股代码名称")
        all_stocks = ak.stock_info_a_code_name()
        hunan_stock = all_stocks[all_stocks['code'] == STOCK_CODE]
        print(f"✅ 找到股票: {hunan_stock['name'].values[0]} ({hunan_stock['code'].values[0]})")
        print(f"   数据包含 {len(all_stocks)} 只A股")

        # API 2: 获取个股信息
        print(f"\n【API 2】ak.stock_individual_info_em(symbol='{STOCK_CODE}') - 获取个股详细信息")
        stock_info = ak.stock_individual_info_em(symbol=STOCK_CODE)
        print("\n股票详细信息:")
        for _, row in stock_info.iterrows():
            print(f"  {row['item']:12s}: {row['value']}")

        print("\n✅ 第1课完成！您已学会获取股票基本信息")
        return stock_info

    except Exception as e:
        print(f"❌ 错误: {e}")
        return None


def lesson_2_realtime_quote():
    """第2课：获取实时行情数据"""
    print("\n" + "=" * 80)
    print("📖 第2课：获取实时行情数据")
    print("=" * 80)

    try:
        # API 3: 获取A股实时行情
        print(f"\n【API 3】ak.stock_zh_a_spot_em() - 获取A股实时行情")
        print("⏳ 正在获取A股实时行情...")
        spot_df = ak.stock_zh_a_spot_em()
        hunan_spot = spot_df[spot_df['代码'] == STOCK_CODE]

        if not hunan_spot.empty:
            print(f"\n✅ {STOCK_NAME} 实时行情:")
            row = hunan_spot.iloc[0]
            print(f"  最新价: {row['最新价']:.2f} 元")
            print(f"  涨跌幅: {row['涨跌幅']:.2f}%")
            print(f"  涨跌额: {row['涨跌额']:.2f} 元")
            print(f"  成交量: {row['成交量']/10000:.2f} 万手")
            print(f"  成交额: {row['成交额']/100000000:.2f} 亿元")
            print(f"  今开: {row['今开']:.2f} 元")
            print(f"  最高: {row['最高']:.2f} 元")
            print(f"  最低: {row['最低']:.2f} 元")
            print(f"  昨收: {row['昨收']:.2f} 元")
            print(f"  换手率: {row['换手率']:.2f}%")
            print(f"  市盈率: {row['市盈率-动态']:.2f}")
            print(f"  市净率: {row['市净率']:.2f}")

            print("\n✅ 第2课完成！您已学会获取实时行情")
            return hunan_spot
        else:
            print(f"⚠️  未找到 {STOCK_CODE} 的实时行情")
            return None

    except Exception as e:
        print(f"❌ 错误: {e}")
        return None


def lesson_3_historical_data():
    """第3课：获取历史行情数据"""
    print("\n" + "=" * 80)
    print("📖 第3课：获取历史行情数据")
    print("=" * 80)

    try:
        # 计算日期范围
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=90)).strftime("%Y%m%d")

        # API 4: 获取历史行情
        print(f"\n【API 4】ak.stock_zh_a_hist(symbol='{STOCK_CODE}', period='daily', start_date='{start_date}', end_date='{end_date}')")
        print(f"⏳ 正在获取 {STOCK_NAME} 近90天历史数据...")

        hist_df = ak.stock_zh_a_hist(
            symbol=STOCK_CODE,
            period="daily",
            start_date=start_date,
            end_date=end_date,
            adjust=""
        )

        print(f"\n✅ 成功获取 {len(hist_df)} 个交易日数据")
        print(f"\n最近10个交易日行情:")
        print(hist_df[['日期', '开盘', '收盘', '最高', '最低', '涨跌幅', '成交量']].head(10).to_string(index=False))

        # 计算统计数据
        print(f"\n📊 近90天统计:")
        print(f"  最高价: {hist_df['最高'].max():.2f} 元")
        print(f"  最低价: {hist_df['最低'].min():.2f} 元")
        print(f"  平均收盘价: {hist_df['收盘'].mean():.2f} 元")
        print(f"  累计涨跌幅: {hist_df['涨跌幅'].sum():.2f}%")
        print(f"  日均成交量: {hist_df['成交量'].mean()/10000:.2f} 万手")
        print(f"  日均成交额: {hist_df['成交额'].mean()/100000000:.2f} 亿元")

        print("\n✅ 第3课完成！您已学会获取历史行情数据")
        return hist_df

    except Exception as e:
        print(f"❌ 错误: {e}")
        return None


def lesson_4_technical_analysis(hist_df):
    """第4课：技术指标计算"""
    print("\n" + "=" * 80)
    print("📖 第4课：技术指标计算与分析")
    print("=" * 80)

    if hist_df is None or hist_df.empty:
        print("⚠️  没有历史数据，跳过技术分析")
        return None

    try:
        df = hist_df.copy()

        print("\n📈 计算技术指标...")

        # 计算移动平均线
        df['MA5'] = df['收盘'].rolling(window=5).mean()
        df['MA10'] = df['收盘'].rolling(window=10).mean()
        df['MA20'] = df['收盘'].rolling(window=20).mean()
        df['MA60'] = df['收盘'].rolling(window=60).mean()

        # 计算RSI
        def calculate_rsi(prices, period=14):
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi

        df['RSI'] = calculate_rsi(df['收盘'])

        # 计算MACD
        exp1 = df['收盘'].ewm(span=12, adjust=False).mean()
        exp2 = df['收盘'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['Histogram'] = df['MACD'] - df['Signal']

        # 计算布林带
        df['BB_middle'] = df['收盘'].rolling(window=20).mean()
        bb_std = df['收盘'].rolling(window=20).std()
        df['BB_upper'] = df['BB_middle'] + 2 * bb_std
        df['BB_lower'] = df['BB_middle'] - 2 * bb_std

        print("\n✅ 技术指标计算完成")

        # 显示最新指标
        latest = df.iloc[-1]
        print(f"\n📊 最新技术指标 ({latest['日期']}):")
        print(f"  收盘价: {latest['收盘']:.2f} 元")
        print(f"  MA5:  {latest['MA5']:.2f} 元")
        print(f"  MA10: {latest['MA10']:.2f} 元")
        print(f"  MA20: {latest['MA20']:.2f} 元")
        print(f"  MA60: {latest['MA60']:.2f} 元" if pd.notna(latest['MA60']) else "  MA60: 数据不足")
        print(f"  RSI:  {latest['RSI']:.2f}" if pd.notna(latest['RSI']) else "  RSI: 数据不足")
        print(f"  MACD: {latest['MACD']:.4f}" if pd.notna(latest['MACD']) else "  MACD: 数据不足")
        print(f"  BB上轨: {latest['BB_upper']:.2f} 元" if pd.notna(latest['BB_upper']) else "  BB上轨: 数据不足")
        print(f"  BB中轨: {latest['BB_middle']:.2f} 元" if pd.notna(latest['BB_middle']) else "  BB中轨: 数据不足")
        print(f"  BB下轨: {latest['BB_lower']:.2f} 元" if pd.notna(latest['BB_lower']) else "  BB下轨: 数据不足")

        # 技术分析
        print(f"\n💡 技术分析:")
        if pd.notna(latest['MA5']) and pd.notna(latest['MA10']):
            if latest['MA5'] > latest['MA10']:
                print(f"  • MA5 > MA10: 短期趋势向上 📈")
            else:
                print(f"  • MA5 < MA10: 短期趋势向下 📉")

        if pd.notna(latest['RSI']):
            if latest['RSI'] > 70:
                print(f"  • RSI = {latest['RSI']:.1f}: 超买区域，可能回调 ⚠️")
            elif latest['RSI'] < 30:
                print(f"  • RSI = {latest['RSI']:.1f}: 超卖区域，可能反弹 💡")
            else:
                print(f"  • RSI = {latest['RSI']:.1f}: 正常区域 ✅")

        if pd.notna(latest['BB_upper']) and pd.notna(latest['BB_lower']):
            if latest['收盘'] > latest['BB_upper']:
                print(f"  • 价格突破布林上轨: 强势上涨 🚀")
            elif latest['收盘'] < latest['BB_lower']:
                print(f"  • 价格跌破布林下轨: 超跌反弹 🔄")

        print("\n✅ 第4课完成！您已学会计算技术指标")
        return df

    except Exception as e:
        print(f"❌ 错误: {e}")
        return None


def lesson_5_financial_data():
    """第5课：获取财务数据"""
    print("\n" + "=" * 80)
    print("📖 第5课：获取财务数据")
    print("=" * 80)

    try:
        # API 5: 获取主要指标
        print(f"\n【API 5】ak.stock_financial_analysis_indicator(symbol='{STOCK_CODE}') - 获取财务分析指标")
        print("⏳ 正在获取财务数据...")

        financial_df = ak.stock_financial_analysis_indicator(symbol=STOCK_CODE)

        if not financial_df.empty:
            print(f"\n✅ 成功获取 {len(financial_df)} 期财务数据")
            print(f"\n最近4期主要财务指标:")
            display_cols = ['日期', 'ROE', 'ROA', '净利润同比增长率', '营业收入同比增长率',
                          '资产负债比率', '流动比率', '速动比率']
            available_cols = [col for col in display_cols if col in financial_df.columns]
            print(financial_df[available_cols].head(4).to_string(index=False))

            # 最新财务指标
            latest = financial_df.iloc[0]
            print(f"\n📊 最新财务指标 ({latest['日期']}):")
            if 'ROE' in financial_df.columns:
                print(f"  ROE (净资产收益率): {latest['ROE']:.2f}%")
            if 'ROA' in financial_df.columns:
                print(f"  ROA (总资产收益率): {latest['ROA']:.2f}%")
            if '净利润同比增长率' in financial_df.columns:
                print(f"  净利润同比增长: {latest['净利润同比增长率']:.2f}%")
            if '营业收入同比增长率' in financial_df.columns:
                print(f"  营收同比增长: {latest['营业收入同比增长率']:.2f}%")
            if '资产负债比率' in financial_df.columns:
                print(f"  资产负债率: {latest['资产负债比率']:.2f}%")

            print("\n✅ 第5课完成！您已学会获取财务数据")
            return financial_df
        else:
            print("⚠️  未获取到财务数据")
            return None

    except Exception as e:
        print(f"❌ 错误: {e}")
        print("💡 提示: 部分股票可能没有完整的财务数据")
        return None


def lesson_6_capital_flow():
    """第6课：获取资金流向数据"""
    print("\n" + "=" * 80)
    print("📖 第6课：获取资金流向数据")
    print("=" * 80)

    try:
        # API 6: 获取个股资金流
        print(f"\n【API 6】ak.stock_individual_fund_flow(stock='{STOCK_CODE}', market='深证') - 获取个股资金流向")
        print("⏳ 正在获取资金流向数据...")

        fund_flow = ak.stock_individual_fund_flow(stock=STOCK_CODE, market="深证")

        if not fund_flow.empty:
            print(f"\n✅ 成功获取 {len(fund_flow)} 天资金流向数据")
            print(f"\n最近10天资金流向:")
            print(fund_flow.head(10).to_string(index=False))

            # 统计分析
            print(f"\n📊 资金流向统计:")
            print(f"  主力净流入总额: {fund_flow['主力净流入-净额'].sum()/100000000:.2f} 亿元")
            print(f"  超大单净流入总额: {fund_flow['超大单净流入-净额'].sum()/100000000:.2f} 亿元")
            print(f"  大单净流入总额: {fund_flow['大单净流入-净额'].sum()/100000000:.2f} 亿元")
            print(f"  中单净流入总额: {fund_flow['中单净流入-净额'].sum()/100000000:.2f} 亿元")
            print(f"  小单净流入总额: {fund_flow['小单净流入-净额'].sum()/100000000:.2f} 亿元")

            # 最新资金流向
            latest = fund_flow.iloc[0]
            print(f"\n💰 最新资金流向 ({latest['日期']}):")
            print(f"  主力净流入: {latest['主力净流入-净额']/10000:.2f} 万元 ({latest['主力净流入-净占比']:.2f}%)")

            if latest['主力净流入-净额'] > 0:
                print(f"  💡 主力资金净流入，市场看好 📈")
            else:
                print(f"  ⚠️  主力资金净流出，需要谨慎 📉")

            print("\n✅ 第6课完成！您已学会获取资金流向数据")
            return fund_flow
        else:
            print("⚠️  未获取到资金流向数据")
            return None

    except Exception as e:
        print(f"❌ 错误: {e}")
        print("💡 提示: 资金流向数据可能有延迟或限制")
        return None


def lesson_7_visualization(hist_df, tech_df):
    """第7课：数据可视化"""
    print("\n" + "=" * 80)
    print("📖 第7课：数据可视化")
    print("=" * 80)

    if hist_df is None or hist_df.empty:
        print("⚠️  没有历史数据，跳过可视化")
        return

    try:
        print("\n📊 正在生成K线图和技术指标图...")

        # 创建图表
        fig, axes = plt.subplots(3, 1, figsize=(14, 10))
        fig.suptitle(f'{STOCK_NAME} ({STOCK_CODE}) 技术分析图表', fontsize=16, fontweight='bold')

        df = tech_df if tech_df is not None else hist_df

        # 图1: K线图 + 均线
        ax1 = axes[0]
        ax1.plot(df['日期'], df['收盘'], label='收盘价', linewidth=2, color='black')
        if 'MA5' in df.columns:
            ax1.plot(df['日期'], df['MA5'], label='MA5', linewidth=1, alpha=0.8)
        if 'MA10' in df.columns:
            ax1.plot(df['日期'], df['MA10'], label='MA10', linewidth=1, alpha=0.8)
        if 'MA20' in df.columns:
            ax1.plot(df['日期'], df['MA20'], label='MA20', linewidth=1, alpha=0.8)

        ax1.set_title('股价走势 + 移动平均线', fontsize=12)
        ax1.set_ylabel('价格 (元)')
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)

        # 图2: 成交量
        ax2 = axes[1]
        colors = ['red' if x >= 0 else 'green' for x in df['涨跌幅']]
        ax2.bar(df['日期'], df['成交量']/10000, color=colors, alpha=0.6)
        ax2.set_title('成交量', fontsize=12)
        ax2.set_ylabel('成交量 (万手)')
        ax2.grid(True, alpha=0.3)

        # 图3: RSI或涨跌幅
        ax3 = axes[2]
        if 'RSI' in df.columns and df['RSI'].notna().any():
            ax3.plot(df['日期'], df['RSI'], label='RSI', linewidth=2, color='purple')
            ax3.axhline(y=70, color='r', linestyle='--', alpha=0.5, label='超买线(70)')
            ax3.axhline(y=30, color='g', linestyle='--', alpha=0.5, label='超卖线(30)')
            ax3.set_title('RSI 相对强弱指标', fontsize=12)
            ax3.set_ylabel('RSI')
            ax3.legend(loc='best')
        else:
            ax3.plot(df['日期'], df['涨跌幅'], label='涨跌幅', linewidth=2, color='blue')
            ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3)
            ax3.set_title('涨跌幅', fontsize=12)
            ax3.set_ylabel('涨跌幅 (%)')
            ax3.legend(loc='best')

        ax3.set_xlabel('日期')
        ax3.grid(True, alpha=0.3)

        # 调整布局
        plt.tight_layout()

        # 保存图表
        filename = f'{STOCK_NAME}_{STOCK_CODE}_分析图表.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\n✅ 图表已保存: {filename}")

        # 显示图表
        plt.show()

        print("\n✅ 第7课完成！您已学会数据可视化")

    except Exception as e:
        print(f"❌ 错误: {e}")


def lesson_8_industry_analysis():
    """第8课：行业分析"""
    print("\n" + "=" * 80)
    print("📖 第8课：行业与板块分析")
    print("=" * 80)

    try:
        # API 7: 获取行业板块数据
        print(f"\n【API 7】ak.stock_board_industry_name_em() - 获取行业板块")
        print("⏳ 正在获取行业板块数据...")

        industry_df = ak.stock_board_industry_name_em()

        print(f"\n✅ 共有 {len(industry_df)} 个行业板块")
        print("\n主要行业板块 (按涨跌幅排序):")
        print(industry_df.sort_values('涨跌幅', ascending=False).head(10)[['板块名称', '涨跌幅', '总市值', '换手率']].to_string(index=False))

        # 找到黄金相关板块
        gold_industry = industry_df[industry_df['板块名称'].str.contains('黄金|贵金属', na=False)]
        if not gold_industry.empty:
            print(f"\n💎 {STOCK_NAME} 所属行业相关板块:")
            print(gold_industry[['板块名称', '涨跌幅', '总市值', '换手率', '上涨家数', '下跌家数']].to_string(index=False))

        print("\n✅ 第8课完成！您已学会行业分析")
        return industry_df

    except Exception as e:
        print(f"❌ 错误: {e}")
        return None


def lesson_9_summary_report():
    """第9课：生成综合分析报告"""
    print("\n" + "=" * 80)
    print("📖 第9课：生成综合分析报告")
    print("=" * 80)

    print(f"\n📝 正在生成 {STOCK_NAME} ({STOCK_CODE}) 综合分析报告...")

    # 汇总所有分析结果
    print("\n" + "=" * 80)
    print(f"📊 {STOCK_NAME} ({STOCK_CODE}) 综合分析报告")
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    print("\n🎯 学习成果总结:")
    print("  ✅ 第1课: 获取股票基本信息 - stock_info_a_code_name(), stock_individual_info_em()")
    print("  ✅ 第2课: 获取实时行情 - stock_zh_a_spot_em()")
    print("  ✅ 第3课: 获取历史数据 - stock_zh_a_hist()")
    print("  ✅ 第4课: 技术指标计算 - MA, RSI, MACD, 布林带")
    print("  ✅ 第5课: 获取财务数据 - stock_financial_analysis_indicator()")
    print("  ✅ 第6课: 获取资金流向 - stock_individual_fund_flow()")
    print("  ✅ 第7课: 数据可视化 - matplotlib绘图")
    print("  ✅ 第8课: 行业分析 - stock_board_industry_name_em()")
    print("  ✅ 第9课: 生成综合报告")

    print("\n📚 核心API总结:")
    print("  1. stock_info_a_code_name() - 获取所有A股代码")
    print("  2. stock_individual_info_em() - 获取个股详细信息")
    print("  3. stock_zh_a_spot_em() - 获取实时行情")
    print("  4. stock_zh_a_hist() - 获取历史数据")
    print("  5. stock_financial_analysis_indicator() - 获取财务指标")
    print("  6. stock_individual_fund_flow() - 获取资金流向")
    print("  7. stock_board_industry_name_em() - 获取行业板块")

    print("\n🚀 进阶学习建议:")
    print("  1. 学习更多技术指标: KDJ, BOLL, OBV等")
    print("  2. 研究量化策略: 趋势跟踪, 均值回归, 动量策略")
    print("  3. 实践回测: 验证策略有效性")
    print("  4. 风险管理: 仓位控制, 止损止盈")
    print("  5. 组合管理: 多股票组合优化")

    print("\n💡 下一步行动:")
    print("  • 修改 STOCK_CODE 变量，分析其他股票")
    print("  • 结合投资原则 (docs/principle.md) 做决策")
    print("  • 使用 investment_advisor.py 生成AI建议")
    print("  • 将数据保存到数据库进行长期跟踪")

    print("\n✅ 第9课完成！恭喜您完成AKShare A股核心API学习！")


def main():
    """主函数 - 运行所有课程"""
    print("\n🎓 开始AKShare A股核心API实战教程")
    print(f"⏰ 学习时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        # 第1课：基本信息
        stock_info = lesson_1_basic_info()
        input("\n按回车键继续下一课...")

        # 第2课：实时行情
        realtime_quote = lesson_2_realtime_quote()
        input("\n按回车键继续下一课...")

        # 第3课：历史数据
        hist_df = lesson_3_historical_data()
        input("\n按回车键继续下一课...")

        # 第4课：技术分析
        tech_df = lesson_4_technical_analysis(hist_df)
        input("\n按回车键继续下一课...")

        # 第5课：财务数据
        financial_df = lesson_5_financial_data()
        input("\n按回车键继续下一课...")

        # 第6课：资金流向
        fund_flow = lesson_6_capital_flow()
        input("\n按回车键继续下一课...")

        # 第7课：可视化
        lesson_7_visualization(hist_df, tech_df)
        input("\n按回车键继续下一课...")

        # 第8课：行业分析
        industry_df = lesson_8_industry_analysis()
        input("\n按回车键继续下一课...")

        # 第9课：综合报告
        lesson_9_summary_report()

        print("\n" + "=" * 80)
        print("🎉 恭喜！您已完成所有课程！")
        print("=" * 80)
        print("\n💪 现在您可以:")
        print("  1. 独立分析任何A股股票")
        print("  2. 构建自己的量化策略")
        print("  3. 结合AI投资顾问做决策")
        print("  4. 开发更复杂的交易系统")

        print("\n📖 推荐阅读:")
        print("  • akshare_quant_guide.md - AKShare量化开发指南")
        print("  • USAGE_GUIDE.md - AI投资顾问使用指南")
        print("  • docs/principle.md - 投资原则文档")

    except KeyboardInterrupt:
        print("\n\n⚠️  学习被中断")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
