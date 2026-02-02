#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
基金投资决策建议模块
基于技术指标、市场数据和投资原则，结合本地大模型提供智能投资建议

功能：
1. 基金实时估值分析
2. 趋势判断和风险评估
3. 买入/卖出/持有决策建议
4. 结合投资原则的智能分析

作者: JavaEdge
日期: 2025-02-01
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, List
from datetime import datetime
from enum import Enum
import os


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


class FundInvestmentAdvisor:
    """基金投资建议生成器"""

    def __init__(self, use_llm: bool = True):
        """
        初始化投资顾问

        :param use_llm: 是否使用本地大模型进行深度分析
        """
        self.use_llm = use_llm
        self.llm_client = None
        self.investment_principles = None

        if use_llm:
            self._init_llm()

    def _init_llm(self):
        """初始化本地大模型"""
        try:
            from llm_client import get_llm_client
            self.llm_client = get_llm_client()
            if self.llm_client:
                print("✅ 本地大模型已启用")
            else:
                print("⚠️  本地大模型不可用，将使用基础分析")
                self.use_llm = False
        except ImportError:
            print("⚠️  未找到llm_client模块，将使用基础分析")
            self.use_llm = False

        # 加载投资原则
        self._load_investment_principles()

    def _load_investment_principles(self):
        """加载投资原则文档"""
        principles_path = os.path.join(os.path.dirname(__file__), "docs", "skills.md")
        if os.path.exists(principles_path):
            with open(principles_path, 'r', encoding='utf-8') as f:
                self.investment_principles = f.read()
            print("✅ 已加载投资原则文档")
        else:
            print("⚠️  未找到投资原则文档")
            self.investment_principles = """
            核心投资原则：
            1. 永远不要追涨杀跌
            2. 不要幻想买在最低点，卖在最高点
            3. 沉没成本不参与重大决策
            4. 方向不对要及时止损
            5. 红的才卖，绿的套着不卖（但要看大势）
            """

    def analyze_fund(self, fund_info: Dict, historical_data: Optional[pd.DataFrame] = None) -> Dict:
        """
        分析基金并生成投资建议

        :param fund_info: 基金实时信息字典
        :param historical_data: 历史数据DataFrame（可选）
        :return: 包含分析结果和建议的字典
        """
        if not fund_info:
            return {
                'error': '无效的基金信息',
                'signal': Signal.HOLD.value,
                'confidence': 0
            }

        # 基础分析
        basic_analysis = self._basic_analysis(fund_info)

        # 如果有历史数据，进行趋势分析
        if historical_data is not None and not historical_data.empty:
            trend_analysis = self._trend_analysis(historical_data)
            basic_analysis.update(trend_analysis)

        # 生成交易信号
        signal = self._generate_signal(basic_analysis)
        basic_analysis['signal'] = signal

        # 如果启用了LLM，进行深度分析
        if self.use_llm and self.llm_client:
            llm_analysis = self._llm_analysis(fund_info, basic_analysis)
            basic_analysis['llm_advice'] = llm_analysis

        return basic_analysis

    def _basic_analysis(self, fund_info: Dict) -> Dict:
        """
        基础分析：根据实时数据进行分析

        :param fund_info: 基金信息
        :return: 分析结果
        """
        result = {
            'fund_code': fund_info.get('基金代码', 'N/A'),
            'fund_name': fund_info.get('基金名称', 'N/A'),
            'current_value': fund_info.get('实时估算净值', 0),
            'estimation_rate': fund_info.get('实时估算增长率', '0%'),
            'last_value': fund_info.get('上一日净值', 0),
            'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # 解析增长率
        rate_str = fund_info.get('实时估算增长率', '0%')
        try:
            rate = float(rate_str.rstrip('%')) if rate_str != '---' else 0.0
        except (ValueError, AttributeError):
            rate = 0.0

        result['rate_value'] = rate

        # 判断涨跌状态
        if rate > 2.0:
            result['status'] = '大涨'
            result['status_emoji'] = '🔴🔴'
        elif rate > 0.5:
            result['status'] = '上涨'
            result['status_emoji'] = '🔴'
        elif rate > -0.5:
            result['status'] = '横盘'
            result['status_emoji'] = '⚪'
        elif rate > -2.0:
            result['status'] = '下跌'
            result['status_emoji'] = '🟢'
        else:
            result['status'] = '大跌'
            result['status_emoji'] = '🟢🟢'

        # 风险评估
        if abs(rate) > 3.0:
            result['risk_level'] = RiskLevel.VERY_HIGH.value
        elif abs(rate) > 2.0:
            result['risk_level'] = RiskLevel.HIGH.value
        elif abs(rate) > 1.0:
            result['risk_level'] = RiskLevel.MEDIUM.value
        else:
            result['risk_level'] = RiskLevel.LOW.value

        return result

    def _trend_analysis(self, historical_data: pd.DataFrame) -> Dict:
        """
        趋势分析：基于历史数据分析趋势

        :param historical_data: 历史净值数据
        :return: 趋势分析结果
        """
        # 这里是占位实现，实际需要历史数据
        return {
            'trend': '需要历史数据',
            'trend_strength': 0
        }

    def _generate_signal(self, analysis: Dict) -> str:
        """
        生成交易信号

        基于投资原则：
        1. 不追涨杀跌
        2. 红的才卖，绿的不卖（除非大势不对）

        :param analysis: 分析结果
        :return: 交易信号
        """
        rate = analysis.get('rate_value', 0)
        status = analysis.get('status', '横盘')

        # 核心原则：不追涨杀跌
        if status == '大涨':
            # 大涨时不买入，持有或考虑止盈
            if rate > 5.0:
                return Signal.SELL.value + " (止盈考虑)"
            else:
                return Signal.HOLD.value + " (不追涨)"

        elif status == '上涨':
            # 适度上涨，观望为主
            return Signal.HOLD.value + " (观望)"

        elif status == '横盘':
            # 横盘时，可以考虑建仓或加仓
            return Signal.BUY.value + " (可建仓)"

        elif status == '下跌':
            # 下跌时，根据跌幅决策
            if rate < -5.0:
                # 大跌可能是机会，但也要注意止损
                return Signal.BUY.value + " (谨慎抄底)"
            else:
                # 轻微下跌，持有观望
                return Signal.HOLD.value + " (持有观望)"

        elif status == '大跌':
            # 大跌时需要判断是抄底机会还是趋势反转
            if rate < -10.0:
                # 暴跌，风险极高
                return Signal.HOLD.value + " (警惕趋势)"
            else:
                return Signal.BUY.value + " (抄底机会)"

        return Signal.HOLD.value

    def _llm_analysis(self, fund_info: Dict, basic_analysis: Dict) -> str:
        """
        使用本地大模型进行深度分析

        :param fund_info: 基金信息
        :param basic_analysis: 基础分析结果
        :return: LLM分析建议
        """
        if not self.llm_client:
            return "LLM不可用"

        try:
            # 构建分析提示词
            prompt = f"""
你是一位专业的基金投资顾问。请基于以下信息和投资原则，给出投资建议。

## 投资原则
{self.investment_principles}

## 基金信息
- 基金名称: {fund_info.get('基金名称', 'N/A')}
- 基金代码: {fund_info.get('基金代码', 'N/A')}
- 实时估算净值: {fund_info.get('实时估算净值', 'N/A')}
- 实时估算增长率: {fund_info.get('实时估算增长率', 'N/A')}
- 最新公布净值: {fund_info.get('最新公布净值', 'N/A')}
- 上一日净值: {fund_info.get('上一日净值', 'N/A')}

## 基础分析结果
- 当前状态: {basic_analysis.get('status', 'N/A')} {basic_analysis.get('status_emoji', '')}
- 风险等级: {basic_analysis.get('risk_level', 'N/A')}
- 初步信号: {basic_analysis.get('signal', 'N/A')}

## 请提供
1. 市场判断（30字以内）
2. 操作建议（买入/持有/卖出，并说明理由，50字以内）
3. 风险提示（30字以内）

请简洁明了，总共不超过150字。
"""

            messages = [
                {"role": "system", "content": "你是一位专业的基金投资顾问，基于价值投资和风险控制原则提供建议。"},
                {"role": "user", "content": prompt}
            ]

            response = self.llm_client.chat(messages, temperature=0.7)

            if response:
                content = self.llm_client.get_response_content(response)
                return content if content else "LLM分析失败"
            else:
                return "LLM响应失败"

        except Exception as e:
            return f"LLM分析出错: {str(e)}"

    def print_advice(self, analysis: Dict):
        """
        格式化打印投资建议

        :param analysis: 分析结果
        """
        print("\n" + "=" * 80)
        print("  💡 基金投资决策建议")
        print("=" * 80)
        print(f"  基金名称: {analysis.get('fund_name', 'N/A')}")
        print(f"  基金代码: {analysis.get('fund_code', 'N/A')}")
        print(f"  分析时间: {analysis.get('analysis_time', 'N/A')}")
        print("-" * 80)

        # 当前状态
        print(f"\n  📊 当前状态: {analysis.get('status', 'N/A')} {analysis.get('status_emoji', '')}")
        print(f"  💰 实时净值: {analysis.get('current_value', 'N/A')}")
        print(f"  📈 涨跌幅: {analysis.get('estimation_rate', 'N/A')}")
        print(f"  ⚠️  风险等级: {analysis.get('risk_level', 'N/A')}")

        # 交易信号
        print("\n" + "-" * 80)
        signal = analysis.get('signal', Signal.HOLD.value)
        print(f"  🎯 交易信号: {signal}")

        # LLM建议
        if 'llm_advice' in analysis and analysis['llm_advice']:
            print("\n" + "-" * 80)
            print("  🤖 AI深度分析:")
            print("-" * 80)
            llm_text = analysis['llm_advice']
            for line in llm_text.split('\n'):
                if line.strip():
                    print(f"  {line}")

        print("\n" + "=" * 80)
        print("  ⚠️  风险提示: 以上建议仅供参考，投资需谨慎！")
        print("=" * 80 + "\n")


def demo_fund_advisor():
    """演示基金投资建议功能"""
    from fund_api import FundAPI

    print("\n" + "=" * 80)
    print("  基金投资决策建议系统")
    print("=" * 80)

    # 创建API和顾问实例
    fund_api = FundAPI()
    advisor = FundInvestmentAdvisor(use_llm=True)

    # 测试基金列表
    test_funds = [
        ("000001", "华夏成长混合"),
        ("161116", "易方达黄金主题"),
    ]

    for fund_code, fund_name in test_funds:
        print(f"\n{'=' * 80}")
        print(f"  分析基金: {fund_name} ({fund_code})")
        print(f"{'=' * 80}")

        # 获取基金实时数据
        fund_info = fund_api.get_fund_realtime_value(fund_code)

        if fund_info:
            # 分析并生成建议
            analysis = advisor.analyze_fund(fund_info)

            # 打印建议
            advisor.print_advice(analysis)
        else:
            print(f"❌ 无法获取基金 {fund_code} 的数据")

        print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    demo_fund_advisor()
