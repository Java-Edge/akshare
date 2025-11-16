#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
投资策略配置文件
根据个人风险偏好和投资风格调整参数

使用方法:
from investment_config import get_strategy_config
config = get_strategy_config('aggressive')  # 激进策略
或
config = get_strategy_config('conservative')  # 保守策略
"""


# 激进策略配置（适合风险承受能力强的投资者）
AGGRESSIVE_STRATEGY = {
    'name': '激进策略',
    'description': '追求高收益，能承受较大波动',

    # 收益率阈值（更激进的买入标准）
    'strong_buy_return': 3.0,       # 3%就强烈买入
    'buy_return': 1.0,              # 1%就考虑买入
    'sell_return': -2.0,            # -2%才卖出
    'strong_sell_return': -4.0,     # -4%强烈卖出

    # 波动率阈值
    'high_volatility': 4.0,         # 能接受更高波动
    'medium_volatility': 2.0,
    'low_volatility': 1.0,

    # 趋势判断参数
    'trend_days': 3,                # 只看短期趋势
    'momentum_threshold': 0.5,      # 较低的动量阈值

    # 仓位建议（更高的仓位）
    'max_position': 100,
    'min_position': 20,
}


# 稳健策略配置（适合平衡型投资者）
BALANCED_STRATEGY = {
    'name': '稳健策略',
    'description': '平衡收益与风险',

    # 收益率阈值
    'strong_buy_return': 5.0,
    'buy_return': 2.0,
    'sell_return': -3.0,
    'strong_sell_return': -5.0,

    # 波动率阈值
    'high_volatility': 3.0,
    'medium_volatility': 1.5,
    'low_volatility': 1.0,

    # 趋势判断参数
    'trend_days': 5,
    'momentum_threshold': 0.6,

    # 仓位建议
    'max_position': 80,
    'min_position': 10,
}


# 保守策略配置（适合风险厌恶型投资者）
CONSERVATIVE_STRATEGY = {
    'name': '保守策略',
    'description': '追求稳定，规避风险',

    # 收益率阈值（更严格的买入标准）
    'strong_buy_return': 8.0,       # 需要8%才强烈买入
    'buy_return': 4.0,              # 需要4%才考虑买入
    'sell_return': -2.0,            # -2%就卖出
    'strong_sell_return': -3.0,     # -3%强烈卖出

    # 波动率阈值（更低的容忍度）
    'high_volatility': 2.0,
    'medium_volatility': 1.0,
    'low_volatility': 0.5,

    # 趋势判断参数
    'trend_days': 10,               # 看更长期的趋势
    'momentum_threshold': 0.7,      # 更高的动量要求

    # 仓位建议（更保守的仓位）
    'max_position': 60,
    'min_position': 5,
}


# 日内交易策略配置（适合短线交易者）
DAYTRADER_STRATEGY = {
    'name': '短线策略',
    'description': '适合短线操作，快进快出',

    # 收益率阈值（对短期波动敏感）
    'strong_buy_return': 2.0,
    'buy_return': 0.5,
    'sell_return': -1.0,
    'strong_sell_return': -2.0,

    # 波动率阈值
    'high_volatility': 3.0,
    'medium_volatility': 1.5,
    'low_volatility': 0.8,

    # 趋势判断参数
    'trend_days': 3,                # 只看最近3天
    'momentum_threshold': 0.6,

    # 仓位建议（灵活调整）
    'max_position': 100,
    'min_position': 0,              # 可以空仓
}


# 长线持有策略配置（适合价值投资者）
LONGTERM_STRATEGY = {
    'name': '长线策略',
    'description': '长期持有，忽略短期波动',

    # 收益率阈值（只关注大趋势）
    'strong_buy_return': 10.0,
    'buy_return': 5.0,
    'sell_return': -5.0,
    'strong_sell_return': -10.0,

    # 波动率阈值（对波动不敏感）
    'high_volatility': 5.0,
    'medium_volatility': 3.0,
    'low_volatility': 1.5,

    # 趋势判断参数
    'trend_days': 20,               # 看更长期趋势
    'momentum_threshold': 0.6,

    # 仓位建议（长期满仓）
    'max_position': 100,
    'min_position': 60,             # 最少保持60%仓位
}


# 策略字典
STRATEGIES = {
    'aggressive': AGGRESSIVE_STRATEGY,
    'balanced': BALANCED_STRATEGY,
    'conservative': CONSERVATIVE_STRATEGY,
    'daytrader': DAYTRADER_STRATEGY,
    'longterm': LONGTERM_STRATEGY,
}


def get_strategy_config(strategy_name: str = 'balanced'):
    """
    获取策略配置

    :param strategy_name: 策略名称
        - 'aggressive': 激进策略
        - 'balanced': 稳健策略
        - 'conservative': 保守策略
        - 'daytrader': 短线策略
        - 'longterm': 长线策略
    :return: 策略配置字典
    """
    config = STRATEGIES.get(strategy_name.lower(), BALANCED_STRATEGY)
    return config.copy()


def list_strategies():
    """列出所有可用策略"""
    print("\n可用的投资策略：")
    print("=" * 60)
    for key, strategy in STRATEGIES.items():
        print(f"\n策略代码: {key}")
        print(f"策略名称: {strategy['name']}")
        print(f"策略描述: {strategy['description']}")
        print(f"买入阈值: {strategy['buy_return']}%")
        print(f"卖出阈值: {strategy['sell_return']}%")
        print(f"最大仓位: {strategy['max_position']}%")
    print("=" * 60)


def create_custom_strategy(
    name: str,
    strong_buy: float = 5.0,
    buy: float = 2.0,
    sell: float = -3.0,
    strong_sell: float = -5.0,
    max_pos: int = 80,
    min_pos: int = 10,
) -> dict:
    """
    创建自定义策略

    :param name: 策略名称
    :param strong_buy: 强烈买入阈值
    :param buy: 买入阈值
    :param sell: 卖出阈值
    :param strong_sell: 强烈卖出阈值
    :param max_pos: 最大仓位
    :param min_pos: 最小仓位
    :return: 策略配置字典
    """
    return {
        'name': name,
        'description': '自定义策略',
        'strong_buy_return': strong_buy,
        'buy_return': buy,
        'sell_return': sell,
        'strong_sell_return': strong_sell,
        'high_volatility': 3.0,
        'medium_volatility': 1.5,
        'low_volatility': 1.0,
        'trend_days': 5,
        'momentum_threshold': 0.6,
        'max_position': max_pos,
        'min_position': min_pos,
    }


if __name__ == "__main__":
    # 显示所有策略
    list_strategies()

    # 示例：获取激进策略
    print("\n\n获取激进策略配置：")
    config = get_strategy_config('aggressive')
    print(config)

    # 示例：创建自定义策略
    print("\n\n创建自定义策略：")
    custom = create_custom_strategy(
        name="我的策略",
        strong_buy=4.0,
        buy=1.5,
        sell=-2.5,
        strong_sell=-4.5,
        max_pos=90,
        min_pos=15
    )
    print(custom)

