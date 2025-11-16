#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
QDII基金投资建议模块
基于技术指标和市场数据，提供买卖决策建议

功能：
1. 多维度技术分析（趋势、波动率、动量等）
2. 买入/卖出/持有信号生成
3. 风险评估和仓位建议
4. 可扩展的策略框架

作者: JavaEdge
日期: 2025-11-09
"""

import pandas as pd
import numpy as np
from typing import Dict
from datetime import datetime
from enum import Enum


class Signal(Enum):
    """交易信号枚举"""
    STRONG_BUY = "强烈买入"
    BUY = "买入"
    HOLD = "持有"
    SELL = "卖出"
    STRONG_SELL = "强烈卖出"


class RiskLevel(Enum):
    """风险等级枚举"""
    LOW = "低风险"
    MEDIUM = "中等风险"
    HIGH = "高风险"
    VERY_HIGH = "极高风险"


class InvestmentAdvisor:
    """投资建议生成器"""

    def __init__(self, config: Dict = None):
        """
        初始化投资顾问

        :param config: 配置参数字典
        """
        self.config = config or self._default_config()

    def _default_config(self) -> Dict:
        """默认配置参数"""
        return {
            # 收益率阈值
            'strong_buy_return': 5.0,      # 强烈买入的总收益率阈值
            'buy_return': 2.0,             # 买入的总收益率阈值
            'sell_return': -3.0,           # 卖出的总收益率阈值
            'strong_sell_return': -5.0,    # 强烈卖出的总收益率阈值

            # 波动率阈值
            'high_volatility': 3.0,        # 高波动率阈值
            'medium_volatility': 1.5,      # 中等波动率阈值
            'low_volatility': 1.0,         # 低波动率阈值

            # 趋势判断参数
            'trend_days': 5,               # 趋势判断的天数
            'momentum_threshold': 0.6,     # 动量阈值（上涨天数占比）

            # 仓位建议
            'max_position': 100,           # 最大仓位（%）
            'min_position': 10,            # 最小仓位（%）
        }

    def analyze(self, df: pd.DataFrame, fund_code: str = None) -> Dict:
        """
        综合分析并生成投资建议

        :param df: 包含基金数据的DataFrame
        :param fund_code: 基金代码（可选）
        :return: 包含分析结果和建议的字典
        """
        # 1. 基础统计指标
        stats = self._calculate_statistics(df)

        # 2. 技术指标
        technical = self._calculate_technical_indicators(df)

        # 3. 趋势分析
        trend = self._analyze_trend(df)

        # 4. 风险评估
        risk = self._assess_risk(stats, technical)

        # 5. 生成交易信号
        signal = self._generate_signal(stats, technical, trend)

        # 6. 仓位建议
        position = self._suggest_position(signal, risk, stats)

        # 7. 具体操作建议
        action = self._generate_action_plan(signal, position, stats, trend)

        return {
            'fund_code': fund_code,
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'statistics': stats,
            'technical': technical,
            'trend': trend,
            'risk': risk,
            'signal': signal,
            'position': position,
            'action': action,
        }

    def _calculate_statistics(self, df: pd.DataFrame) -> Dict:
        """计算基础统计指标"""
        return {
            'total_return': df['涨跌幅'].sum(),
            'avg_daily_return': df['涨跌幅'].mean(),
            'max_gain': df['涨跌幅'].max(),
            'max_loss': df['涨跌幅'].min(),
            'volatility': df['涨跌幅'].std(),
            'positive_days': len(df[df['涨跌幅'] > 0]),
            'negative_days': len(df[df['涨跌幅'] < 0]),
            'total_days': len(df),
            'win_rate': len(df[df['涨跌幅'] > 0]) / len(df) * 100 if len(df) > 0 else 0,
            'latest_price': df['收盘'].iloc[0] if len(df) > 0 else 0,
            'latest_change': df['涨跌幅'].iloc[0] if len(df) > 0 else 0,
        }

    def _calculate_technical_indicators(self, df: pd.DataFrame) -> Dict:
        """计算技术指标"""
        # 移动平均线
        ma5 = df['收盘'].head(5).mean() if len(df) >= 5 else df['收盘'].mean()
        ma10 = df['收盘'].head(10).mean() if len(df) >= 10 else df['收盘'].mean()
        ma20 = df['收盘'].head(20).mean() if len(df) >= 20 else df['收盘'].mean()

        # RSI（简化版）
        rsi = self._calculate_rsi(df, period=14)

        # 涨跌幅动量
        momentum_5d = df['涨跌幅'].head(5).sum() if len(df) >= 5 else 0
        momentum_10d = df['涨跌幅'].head(10).sum() if len(df) >= 10 else 0

        return {
            'ma5': ma5,
            'ma10': ma10,
            'ma20': ma20,
            'current_vs_ma5': (df['收盘'].iloc[0] - ma5) / ma5 * 100 if ma5 > 0 else 0,
            'current_vs_ma10': (df['收盘'].iloc[0] - ma10) / ma10 * 100 if ma10 > 0 else 0,
            'current_vs_ma20': (df['收盘'].iloc[0] - ma20) / ma20 * 100 if ma20 > 0 else 0,
            'rsi': rsi,
            'momentum_5d': momentum_5d,
            'momentum_10d': momentum_10d,
        }

    def _calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> float:
        """计算RSI指标"""
        if len(df) < period:
            period = len(df)

        changes = df['涨跌幅'].head(period).values
        gains = np.where(changes > 0, changes, 0)
        losses = np.where(changes < 0, -changes, 0)

        avg_gain = gains.mean()
        avg_loss = losses.mean()

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def _analyze_trend(self, df: pd.DataFrame) -> Dict:
        """分析趋势"""
        trend_days = min(self.config['trend_days'], len(df))
        recent_data = df.head(trend_days)

        up_days = len(recent_data[recent_data['涨跌幅'] > 0])
        down_days = len(recent_data[recent_data['涨跌幅'] < 0])

        # 判断趋势方向
        if up_days > down_days * 1.5:
            trend_direction = "上涨"
        elif down_days > up_days * 1.5:
            trend_direction = "下跌"
        else:
            trend_direction = "震荡"

        # 趋势强度
        momentum = up_days / trend_days if trend_days > 0 else 0
        if momentum >= 0.7:
            trend_strength = "强"
        elif momentum >= 0.5:
            trend_strength = "中"
        else:
            trend_strength = "弱"

        return {
            'direction': trend_direction,
            'strength': trend_strength,
            'momentum': momentum,
            'up_days': up_days,
            'down_days': down_days,
            'recent_days': trend_days,
        }

    def _assess_risk(self, stats: Dict, technical: Dict) -> Dict:
        """评估风险等级"""
        volatility = stats['volatility']

        # 基于波动率判断风险
        if volatility >= self.config['high_volatility']:
            level = RiskLevel.HIGH
        elif volatility >= self.config['medium_volatility']:
            level = RiskLevel.MEDIUM
        else:
            level = RiskLevel.LOW

        # RSI超买超卖风险
        rsi = technical['rsi']
        rsi_risk = "正常"
        if rsi >= 70:
            rsi_risk = "超买"
        elif rsi <= 30:
            rsi_risk = "超卖"

        return {
            'level': level.value,
            'volatility': volatility,
            'rsi_status': rsi_risk,
            'description': self._risk_description(level, volatility),
        }

    def _risk_description(self, level: RiskLevel, volatility: float) -> str:
        """风险描述"""
        descriptions = {
            RiskLevel.LOW: f"波动率{volatility:.2f}%，市场相对稳定",
            RiskLevel.MEDIUM: f"波动率{volatility:.2f}%，市场波动适中",
            RiskLevel.HIGH: f"波动率{volatility:.2f}%，市场波动较大",
            RiskLevel.VERY_HIGH: f"波动率{volatility:.2f}%，市场剧烈波动",
        }
        return descriptions.get(level, "无法判断")

    def _generate_signal(self, stats: Dict, technical: Dict, trend: Dict) -> Dict:
        """生成交易信号"""
        total_return = stats['total_return']
        momentum = trend['momentum']
        rsi = technical['rsi']

        score = 0  # 综合评分

        # 1. 收益率评分
        if total_return >= self.config['strong_buy_return']:
            score += 2
        elif total_return >= self.config['buy_return']:
            score += 1
        elif total_return <= self.config['strong_sell_return']:
            score -= 2
        elif total_return <= self.config['sell_return']:
            score -= 1

        # 2. 趋势评分
        if trend['direction'] == "上涨":
            score += 1
        elif trend['direction'] == "下跌":
            score -= 1

        # 3. RSI评分
        if 30 <= rsi <= 70:
            score += 0.5  # RSI正常区间
        elif rsi < 30:
            score += 1  # 超卖，可能反弹
        elif rsi > 70:
            score -= 1  # 超买，可能回调

        # 4. 胜率评分
        if stats['win_rate'] >= 60:
            score += 0.5
        elif stats['win_rate'] <= 40:
            score -= 0.5

        # 根据总分确定信号
        if score >= 3:
            signal = Signal.STRONG_BUY
        elif score >= 1.5:
            signal = Signal.BUY
        elif score <= -3:
            signal = Signal.STRONG_SELL
        elif score <= -1.5:
            signal = Signal.SELL
        else:
            signal = Signal.HOLD

        return {
            'signal': signal.value,
            'score': score,
            'confidence': min(abs(score) / 4 * 100, 100),  # 信号置信度
        }

    def _suggest_position(self, signal: Dict, risk: Dict, stats: Dict) -> Dict:
        """建议仓位"""
        signal_type = signal['signal']
        confidence = signal['confidence']

        # 基础仓位
        if signal_type == Signal.STRONG_BUY.value:
            base_position = 80
        elif signal_type == Signal.BUY.value:
            base_position = 60
        elif signal_type == Signal.HOLD.value:
            base_position = 40
        elif signal_type == Signal.SELL.value:
            base_position = 20
        else:  # STRONG_SELL
            base_position = 0

        # 根据风险调整
        if risk['level'] == RiskLevel.HIGH.value:
            base_position = int(base_position * 0.7)
        elif risk['level'] == RiskLevel.VERY_HIGH.value:
            base_position = int(base_position * 0.5)

        # 根据置信度微调
        adjusted_position = int(base_position * (0.8 + confidence / 100 * 0.4))

        # 限制在合理范围内
        final_position = max(self.config['min_position'],
                            min(self.config['max_position'], adjusted_position))

        return {
            'recommended': final_position,
            'min': self.config['min_position'],
            'max': self.config['max_position'],
            'description': f"建议仓位 {final_position}%",
        }

    def _generate_action_plan(self, signal: Dict, position: Dict,
                             stats: Dict, trend: Dict) -> Dict:
        """生成具体操作建议"""
        signal_type = signal['signal']
        current_price = stats['latest_price']

        actions = []
        reasons = []

        # 根据信号生成建议
        if signal_type == Signal.STRONG_BUY.value:
            actions.append(f"✅ 强烈建议买入，建议仓位{position['recommended']}%")
            reasons.append(f"近期总收益{stats['total_return']:.2f}%，表现强劲")
            reasons.append(f"趋势{trend['direction']}，动量{trend['momentum']:.1%}")
            reasons.append(f"当前价格{current_price:.4f}，处于上升通道")

        elif signal_type == Signal.BUY.value:
            actions.append(f"📈 建议适量买入，建议仓位{position['recommended']}%")
            reasons.append(f"近期表现良好，总收益{stats['total_return']:.2f}%")
            reasons.append(f"市场趋势{trend['direction']}，可以关注")

        elif signal_type == Signal.HOLD.value:
            actions.append(f"📊 建议持有观望，保持仓位{position['recommended']}%")
            reasons.append(f"市场处于{trend['direction']}状态")
            reasons.append("暂无明确买入或卖出信号")

        elif signal_type == Signal.SELL.value:
            actions.append(f"⚠️  建议减仓，降低仓位至{position['recommended']}%")
            reasons.append(f"近期表现较弱，总收益{stats['total_return']:.2f}%")
            reasons.append(f"市场趋势{trend['direction']}，需要谨慎")

        else:  # STRONG_SELL
            actions.append(f"🚫 强烈建议卖出，减少至{position['recommended']}%或清仓")
            reasons.append(f"近期表现很差，总收益{stats['total_return']:.2f}%")
            reasons.append(f"趋势明显{trend['direction']}，风险较高")

        # 添加风险提示
        if stats['volatility'] > self.config['high_volatility']:
            actions.append("⚠️  市场波动较大，注意控制风险")

        return {
            'actions': actions,
            'reasons': reasons,
            'summary': actions[0] if actions else "无操作建议",
        }

    def print_advice(self, advice: Dict):
        """格式化打印投资建议"""
        print(f"\n{'='*70}")
        print(f"💡 投资决策建议 - {advice['analysis_date']}")
        if advice['fund_code']:
            print(f"基金代码: {advice['fund_code']}")
        print(f"{'='*70}")

        # 市场状态
        stats = advice['statistics']
        print(f"\n📊 市场状态:")
        print(f"  最新价格: {stats['latest_price']:.4f}")
        print(f"  最新涨跌: {stats['latest_change']:+.2f}%")
        print(f"  近期总收益: {stats['total_return']:+.2f}%")
        print(f"  日均收益: {stats['avg_daily_return']:+.2f}%")
        print(f"  胜率: {stats['win_rate']:.1f}% ({stats['positive_days']}/{stats['total_days']}天上涨)")

        # 技术指标
        tech = advice['technical']
        print(f"\n📈 技术指标:")
        print(f"  RSI(14): {tech['rsi']:.1f}")
        print(f"  5日动量: {tech['momentum_5d']:+.2f}%")
        print(f"  相对MA5: {tech['current_vs_ma5']:+.2f}%")
        print(f"  相对MA10: {tech['current_vs_ma10']:+.2f}%")

        # 趋势分析
        trend = advice['trend']
        print(f"\n📉 趋势分析:")
        print(f"  方向: {trend['direction']} (强度: {trend['strength']})")
        print(f"  动量: {trend['momentum']:.1%}")
        print(f"  近{trend['recent_days']}天: {trend['up_days']}涨 {trend['down_days']}跌")

        # 风险评估
        risk = advice['risk']
        print(f"\n⚠️  风险评估:")
        print(f"  风险等级: {risk['level']}")
        print(f"  波动率: {risk['volatility']:.2f}%")
        print(f"  RSI状态: {risk['rsi_status']}")
        print(f"  说明: {risk['description']}")

        # 交易信号
        signal = advice['signal']
        print(f"\n🎯 交易信号:")
        print(f"  信号: {signal['signal']}")
        print(f"  综合评分: {signal['score']:.1f}")
        print(f"  信号置信度: {signal['confidence']:.1f}%")

        # 仓位建议
        position = advice['position']
        print(f"\n💰 仓位建议:")
        print(f"  {position['description']}")
        print(f"  (范围: {position['min']}%-{position['max']}%)")

        # 操作建议
        action = advice['action']
        print(f"\n🎬 操作建议:")
        for act in action['actions']:
            print(f"  {act}")

        print(f"\n📝 理由分析:")
        for reason in action['reasons']:
            print(f"  • {reason}")

        print(f"\n{'='*70}")
        print(f"{'='*70}\n")


def quick_advice(df: pd.DataFrame, fund_code: str = None, config: Dict = None) -> Dict:
    """
    快速生成投资建议的便捷函数

    :param df: 基金数据DataFrame
    :param fund_code: 基金代码
    :param config: 自定义配置
    :return: 投资建议字典
    """
    advisor = InvestmentAdvisor(config)
    advice = advisor.analyze(df, fund_code)
    advisor.print_advice(advice)
    return advice


if __name__ == "__main__":
    # 示例用法
    print("投资建议模块已加载")
    print("使用方法：")
    print("from investment_advisor import quick_advice")
    print("advice = quick_advice(df, fund_code='513100')")

