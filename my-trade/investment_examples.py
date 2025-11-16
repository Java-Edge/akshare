#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
投资建议模块使用示例
演示如何使用不同策略进行投资决策
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
from investment_advisor import InvestmentAdvisor, quick_advice
from investment_config import get_strategy_config, list_strategies


def example_1_basic_usage():
    """示例1: 基础使用 - 使用默认配置"""
    print("\n" + "="*70)
    print("示例1: 基础使用（默认配置）")
    print("="*70)

    # 模拟数据
    df = create_sample_data()

    # 快速生成投资建议
    advice = quick_advice(df, fund_code='513100')

    return advice


def example_2_with_strategy():
    """示例2: 使用预设策略"""
    print("\n" + "="*70)
    print("示例2: 使用激进策略")
    print("="*70)

    # 获取激进策略配置
    config = get_strategy_config('aggressive')

    # 模拟数据
    df = create_sample_data()

    # 使用激进策略生成建议
    advice = quick_advice(df, fund_code='513100', config=config)

    return advice


def example_3_compare_strategies():
    """示例3: 比较不同策略的建议"""
    print("\n" + "="*70)
    print("示例3: 比较不同策略")
    print("="*70)

    # 模拟数据
    df = create_sample_data()

    strategies = ['conservative', 'balanced', 'aggressive']

    for strategy_name in strategies:
        print(f"\n\n{'='*70}")
        print(f"使用策略: {strategy_name.upper()}")
        print(f"{'='*70}")

        config = get_strategy_config(strategy_name)
        advisor = InvestmentAdvisor(config)
        advice = advisor.analyze(df, '513100')

        # 只打印关键信息
        print(f"\n策略: {config['name']}")
        print(f"交易信号: {advice['signal']['signal']}")
        print(f"建议仓位: {advice['position']['recommended']}%")
        print(f"操作建议: {advice['action']['summary']}")


def example_4_custom_config():
    """示例4: 使用自定义配置"""
    print("\n" + "="*70)
    print("示例4: 自定义配置")
    print("="*70)

    # 自定义配置
    custom_config = {
        'strong_buy_return': 4.0,   # 4%才强烈买入
        'buy_return': 1.5,          # 1.5%就买入
        'sell_return': -2.5,        # -2.5%就卖出
        'strong_sell_return': -4.5, # -4.5%强烈卖出
        'high_volatility': 3.5,
        'medium_volatility': 2.0,
        'low_volatility': 1.0,
        'trend_days': 7,
        'momentum_threshold': 0.65,
        'max_position': 90,
        'min_position': 15,
    }

    # 模拟数据
    df = create_sample_data()

    # 使用自定义配置
    advice = quick_advice(df, fund_code='513100', config=custom_config)

    return advice


def example_5_real_data():
    """示例5: 使用真实数据（需要网络）"""
    print("\n" + "="*70)
    print("示例5: 使用真实数据")
    print("="*70)

    try:
        # 从akshare获取真实数据
        fund_code = "513100"
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=60)).strftime("%Y%m%d")

        print(f"正在获取基金 {fund_code} 的真实数据...")
        df = ak.fund_etf_hist_em(
            symbol=fund_code,
            period="daily",
            start_date=start_date,
            end_date=end_date,
            adjust=""
        )

        if df.empty:
            print("未获取到数据，使用模拟数据代替")
            df = create_sample_data()
        else:
            df['日期'] = pd.to_datetime(df['日期'])
            df = df.sort_values('日期', ascending=False).head(30)
            print(f"✅ 成功获取 {len(df)} 条真实数据")

        # 使用稳健策略
        config = get_strategy_config('balanced')
        advice = quick_advice(df, fund_code=fund_code, config=config)

        return advice

    except Exception as e:
        print(f"❌ 获取真实数据失败: {e}")
        print("使用模拟数据代替")
        df = create_sample_data()
        advice = quick_advice(df, fund_code='513100')
        return advice


def create_sample_data():
    """创建样本数据用于演示"""
    import numpy as np

    days = 30
    dates = pd.date_range(end=datetime.now(), periods=days, freq='B')

    # 模拟价格走势（总体上涨）
    base_price = 100
    changes = np.random.normal(0.5, 2.0, days)  # 均值0.5%，标准差2%

    close_prices = [base_price]
    for change in changes[1:]:
        close_prices.append(close_prices[-1] * (1 + change/100))

    df = pd.DataFrame({
        '日期': dates,
        '开盘': [p * (1 - np.random.uniform(0, 0.01)) for p in close_prices],
        '收盘': close_prices,
        '最高': [p * (1 + np.random.uniform(0, 0.02)) for p in close_prices],
        '最低': [p * (1 - np.random.uniform(0, 0.02)) for p in close_prices],
        '涨跌幅': changes,
        '成交量': np.random.randint(100000, 500000, days),
        '成交额': [v * p for v, p in zip(np.random.randint(100000, 500000, days), close_prices)]
    })

    return df.sort_values('日期', ascending=False).reset_index(drop=True)


def main():
    """主函数"""
    print("\n🎯 投资建议模块使用示例")
    print("="*70)

    examples = {
        '1': ('基础使用', example_1_basic_usage),
        '2': ('使用预设策略', example_2_with_strategy),
        '3': ('比较不同策略', example_3_compare_strategies),
        '4': ('自定义配置', example_4_custom_config),
        '5': ('使用真实数据', example_5_real_data),
        'list': ('查看所有策略', lambda: list_strategies()),
    }

    print("\n请选择示例：")
    for key, (name, _) in examples.items():
        print(f"  {key}. {name}")

    choice = input("\n请输入选项 (1-5/list/q退出): ").strip()

    if choice.lower() == 'q':
        print("退出示例")
        return

    if choice in examples:
        _, func = examples[choice]
        func()
    else:
        print("无效选择，运行默认示例")
        example_1_basic_usage()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n示例已取消")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()

