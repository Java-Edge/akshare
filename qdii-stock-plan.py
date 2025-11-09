#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
QDII基金分析工具
传入指定的QDII基金代码，查询近30个交易日的涨跌幅数据并绘制折线图
"""

import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import argparse
import matplotlib.font_manager as fm
import pymysql
from pymysql import Error
import database_config

fund_code = "513100"  # 可以替换为其他QDII基金代码
days = 30  # 分析最近30个交易日

def query_from_database(fund_code: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    从数据库查询基金数据

    :param fund_code: 基金代码
    :param start_date: 开始日期 (YYYY-MM-DD)
    :param end_date: 结束日期 (YYYY-MM-DD)
    :return: 包含基金数据的DataFrame
    """
    try:
        connection = pymysql.connect(**database_config.MYSQL_CONFIG)
        with connection.cursor() as cursor:
            cursor.execute(database_config.QUERY_DATA_SQL, (fund_code, start_date, end_date))
            results = cursor.fetchall()

            if results:
                df = pd.DataFrame(results)
                df['日期'] = pd.to_datetime(df['日期'])
                return df
            else:
                return pd.DataFrame()

    except Exception as e:
        print(f"❌ 数据库查询失败: {e}")
        return pd.DataFrame()
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

def get_missing_dates(existing_dates, all_dates):
    """
    获取缺失的日期

    :param existing_dates: 已存在的日期列表
    :param all_dates: 所有需要的日期列表
    :return: 缺失的日期列表
    """
    existing_date_set = set(existing_dates)
    return [date for date in all_dates if date not in existing_date_set]

def get_qdii_fund_data(fund_code: str, days: int = 30) -> pd.DataFrame:
    """
    获取QDII基金近N个交易日的涨跌幅数据（智能获取：先查数据库，再补全缺失数据）

    :param fund_code: QDII基金代码
    :param days: 交易日天数
    :return: 包含涨跌幅数据的DataFrame
    """
    try:
        # 计算日期范围
        end_date = datetime.now().date()
        start_date = (end_date - timedelta(days=days*2)).strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")

        print(f"📊 先从数据库查询数据 ({start_date} 到 {end_date_str})...")

        # 1. 先从数据库查询数据
        db_df = query_from_database(fund_code, start_date, end_date_str)

        if not db_df.empty:
            print(f"✅ 从数据库获取到 {len(db_df)} 条历史数据")

        # 2. 计算需要的所有交易日日期
        all_required_dates = pd.date_range(end=end_date, periods=days, freq='B')  # 工作日

        if not db_df.empty:
            # 3. 检查哪些日期在数据库中缺失
            existing_dates = set(db_df['日期'].dt.date)
            missing_dates = [date for date in all_required_dates if date.date() not in existing_dates]

            if missing_dates:
                print(f"📝 发现 {len(missing_dates)} 个缺失交易日，正在从API获取...")
                # 4. 获取缺失日期的数据
                missing_start = missing_dates[0].strftime("%Y%m%d")
                missing_end = missing_dates[-1].strftime("%Y%m%d")

                api_df = ak.fund_etf_hist_em(
                    symbol=fund_code,
                    period="daily",
                    start_date=missing_start,
                    end_date=missing_end,
                    adjust=""
                )

                if not api_df.empty:
                    api_df['日期'] = pd.to_datetime(api_df['日期'])
                    # 5. 合并数据库数据和API数据
                    combined_df = pd.concat([db_df, api_df], ignore_index=True)
                    # 去重并排序
                    combined_df = combined_df.drop_duplicates('日期').sort_values('日期', ascending=False).head(days)
                    print(f"✅ 成功合并数据库和API数据，总计 {len(combined_df)} 条数据")
                    return combined_df.reset_index(drop=True)
                else:
                    print("⚠️  API未返回缺失日期数据，使用数据库现有数据")
                    return db_df.sort_values('日期', ascending=False).head(days).reset_index(drop=True)
            else:
                print("✅ 数据库已包含所有需要的数据")
                return db_df.sort_values('日期', ascending=False).head(days).reset_index(drop=True)
        else:
            # 数据库中没有数据，完全从API获取
            print("📡 数据库中无数据，从API获取完整数据...")
            start_date_api = (end_date - timedelta(days=days*2)).strftime("%Y%m%d")
            end_date_api = end_date.strftime("%Y%m%d")

            df = ak.fund_etf_hist_em(
                symbol=fund_code,
                period="daily",
                start_date=start_date_api,
                end_date=end_date_api,
                adjust=""
            )

            if df.empty:
                raise ValueError(f"未找到基金代码 {fund_code} 的历史数据")

            df['日期'] = pd.to_datetime(df['日期'])
            df = df.sort_values('日期', ascending=False).head(days)
            return df.reset_index(drop=True)

    except Exception as e:
        print(f"❌ 数据获取失败: {e}")
        print("💡 正在尝试使用模拟数据演示功能...")
        return generate_mock_data(fund_code, days)

def generate_mock_data(fund_code: str, days: int = 30) -> pd.DataFrame:
    """
    生成模拟的QDII基金数据用于演示

    :param fund_code: 基金代码
    :param days: 天数
    :return: 模拟数据DataFrame
    """
    import numpy as np

    # 生成日期
    dates = pd.date_range(end=datetime.now(), periods=days, freq='B')  # 工作日

    # 生成模拟的涨跌幅数据 (-3% 到 +5% 之间)
    np.random.seed(42)  # 固定随机种子以便重现
    changes = np.random.uniform(-3, 5, days)

    # 生成收盘价（从100开始）
    close_prices = [100]
    for change in changes:
        close_prices.append(close_prices[-1] * (1 + change/100))
    close_prices = close_prices[1:]  # 去掉初始值

    df = pd.DataFrame({
        '日期': dates,
        '开盘': [p * (1 + np.random.uniform(-0.01, 0.01)) for p in close_prices],
        '收盘': close_prices,
        '最高': [p * (1 + np.random.uniform(0, 0.02)) for p in close_prices],
        '最低': [p * (1 - np.random.uniform(0, 0.02)) for p in close_prices],
        '涨跌幅': changes,
        '成交量': np.random.randint(100000, 500000, days),
        '成交额': [v * p for v, p in zip(np.random.randint(100000, 500000, days), close_prices)]
    })

    print("📋 使用模拟数据演示功能（实际使用时需要网络连接）")
    return df

def plot_fund_performance(df: pd.DataFrame, fund_code: str, days: int = 30, save_path: str = None):
    """
    绘制基金涨跌幅折线图

    :param df: 包含基金数据的DataFrame
    :param fund_code: 基金代码
    :param days: 交易日天数
    :param save_path: 图片保存路径
    """
    # 设置中文字体支持
    try:
        # 尝试使用系统支持的中文字体
        zh_fonts = ['PingFang SC', 'Hiragino Sans GB', 'STHeiti', 'Microsoft YaHei', 'SimHei', 'DejaVu Sans']
        for font_name in zh_fonts:
            if font_name in [f.name for f in fm.fontManager.ttflist]:
                plt.rcParams['font.sans-serif'] = [font_name, 'DejaVu Sans']
                plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
                break
    except:
        # 如果字体设置失败，使用默认设置
        pass

    plt.figure(figsize=(12, 6))
    plt.plot(df['日期'], df['涨跌幅'], marker='o', linestyle='-', linewidth=2, markersize=4)

    # 设置图表标题和标签
    plt.title(f'QDII基金 {fund_code} 近{days}个交易日涨跌幅', fontsize=16, fontweight='bold')
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('涨跌幅 (%)', fontsize=12)

    # 设置x轴日期格式
    plt.gcf().autofmt_xdate()

    # 添加网格
    plt.grid(True, alpha=0.3)

    # 添加零线
    plt.axhline(y=0, color='r', linestyle='--', alpha=0.7)

    # 在最后一个数据点标注数值
    last_date = df['日期'].iloc[-1]
    last_change = df['涨跌幅'].iloc[-1]
    plt.annotate(f'{last_change:.2f}%',
                xy=(last_date, last_change),
                xytext=(10, 10),
                textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

    plt.tight_layout()

    # 保存或显示图片
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存至: {save_path}")
    else:
        plt.show()

def analyze_fund_performance(df: pd.DataFrame, fund_code: str, days: int):
    """
    分析基金表现并输出统计信息

    :param df: 包含基金数据的DataFrame
    :param fund_code: 基金代码
    :param days: 交易日天数
    """
    print(f"\n📊 QDII基金 {fund_code} 近{days}个交易日表现分析:")
    print("=" * 50)

    # 显示最近10条数据
    print(f"\n最近10个交易日数据:")
    print(df[['日期', '收盘', '涨跌幅']].head(10).to_string(index=False))

    # 计算统计信息
    total_return = df['涨跌幅'].sum()
    avg_daily_return = df['涨跌幅'].mean()
    max_gain = df['涨跌幅'].max()
    max_loss = df['涨跌幅'].min()
    positive_days = len(df[df['涨跌幅'] > 0])
    volatility = df['涨跌幅'].std()

    print(f"\n?? 统计分析:")
    print(f"总收益: {total_return:.2f}%")
    print(f"日均收益: {avg_daily_return:.2f}%")
    print(f"最大单日涨幅: {max_gain:.2f}%")
    print(f"最大单日跌幅: {max_loss:.2f}%")
    print(f"波动率: {volatility:.2f}%")
    print(f"上涨天数: {positive_days}/{days} ({positive_days/days*100:.1f}%)")

    # 投资建议
    print(f"\n?? 投资建议:")
    if total_return > 5:
        print("✅ 近期表现强劲，可以考虑关注或适量买入")
    elif total_return > 0:
        print("📊 近期表现平稳，可以继续观察")
    else:
        print("⚠️  近期表现较弱，建议谨慎操作")

    if volatility > 3:
        print("📉 波动较大，风险较高，建议控制仓位")
    elif volatility < 1:
        print("📈 波动较小，相对稳健")

def save_to_database(df: pd.DataFrame, fund_code: str):
    """
    将基金数据保存到MySQL数据库

    :param df: 包含基金数据的DataFrame
    :param fund_code: 基金代码
    """
    try:
        # 连接数据库
        connection = pymysql.connect(**database_config.MYSQL_CONFIG)

        with connection.cursor() as cursor:
            # 检查表是否存在，如果不存在则创建
            cursor.execute(database_config.CREATE_TABLE_SQL)

            # 准备插入数据的SQL
            insert_sql = """
            INSERT INTO qdii_fund_data 
            (fund_code, trade_date, open_price, close_price, high_price, low_price, change_percent, volume, turnover)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            open_price = VALUES(open_price),
            close_price = VALUES(close_price),
            high_price = VALUES(high_price),
            low_price = VALUES(low_price),
            change_percent = VALUES(change_percent),
            volume = VALUES(volume),
            turnover = VALUES(turnover),
            updated_time = CURRENT_TIMESTAMP
            """

            # 准备数据
            data_to_insert = []
            for _, row in df.iterrows():
                data_to_insert.append((
                    fund_code,
                    row['日期'].date(),
                    row['开盘'],
                    row['收盘'],
                    row['最高'],
                    row['最低'],
                    row['涨跌幅'],
                    row['成交量'],
                    row['成交额']
                ))

            # 批量插入数据
            cursor.executemany(insert_sql, data_to_insert)
            connection.commit()

            print(f"✅ 成功保存 {len(data_to_insert)} 条数据到数据库")

    except Error as e:
        print(f"❌ 数据库错误: {e}")
        print("?? 请检查数据库配置和连接")
    except Exception as e:
        print(f"❌ 保存数据时发生错误: {e}")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

def main():
    """主函数 - 直接代码调用示例"""
    try:
        # 直接在代码中设置参数
        fund_code = "513100"  # 纳斯达克100ETF，可以改成其他代码
        days = 30             # 分析最近30个交易日
        save_path = None      # 图片保存路径，设为None则显示不保存

        # 获取基金数据
        print(f"正在获取基金 {fund_code} 近{days}个交易日数据...")
        df = get_qdii_fund_data(fund_code, days)

        # 分析基金表现
        analyze_fund_performance(df, fund_code, days)

        # 保存数据到数据库
        print(f"\n💾 正在保存数据到数据库...")
        save_to_database(df, fund_code)

        # 绘制图表
        print(f"\n🎨 正在生成涨跌幅折线图...")
        plot_fund_performance(df, fund_code, days, save_path)

    except ValueError as e:
        print(f"❌ 错误: {e}")
        print("\n💡 常见QDII基金代码示例:")
        print("   - 513100: 纳斯达克100ETF")
        print("   - 513500: 标普500ETF")
        print("   - 159920: 恒生ETF")
        print("   - 513050: 中概互联ETF")
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        print("💡 请检查网络连接或代理设置，或稍后重试")

if __name__ == "__main__":
    main()