#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
本地大模型客户端
连接 LM Studio 提供的本地大模型服务，提供投资建议分析

作者: JavaEdge
日期: 2025-01-25
"""

import requests
import json
from typing import Dict, Optional
import time


class LocalLLMClient:
    """本地大模型客户端"""

    def __init__(self, api_url: str = "http://10.56.88.6:1234/v1/chat/completions",
                 model: str = "google/gemma-3-27b",
                 timeout: int = 120):
        """
        初始化本地LLM客户端

        :param api_url: 本地模型API地址
        :param model: 模型名称
        :param timeout: 请求超时时间（秒）
        """
        self.api_url = api_url
        self.model = model
        self.timeout = timeout
        self._test_connection()

    def _test_connection(self):
        """测试与本地模型的连接"""
        try:
            response = requests.get(
                self.api_url.replace('/v1/chat/completions', '/v1/models'),
                timeout=5
            )
            if response.status_code == 200:
                print("✅ 本地大模型连接成功")
            else:
                print(f"⚠️  本地模型响应异常: {response.status_code}")
        except Exception as e:
            print(f"⚠️  无法连接到本地模型: {e}")
            print("   将使用基础分析模式")

    def chat(self, messages: list, temperature: float = 0.7,
             max_tokens: int = -1, stream: bool = False) -> Optional[Dict]:
        """
        发送聊天请求到本地模型

        :param messages: 消息列表
        :param temperature: 温度参数
        :param max_tokens: 最大token数
        :param stream: 是否使用流式响应
        :return: 模型响应字典
        """
        request_data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }

        try:
            response = requests.post(
                url=self.api_url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(request_data),
                timeout=self.timeout
            )

            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    return result
                else:
                    print("❌ 模型响应格式异常")
                    return None
            else:
                print(f"❌ 模型请求失败: {response.status_code}")
                print(f"   错误信息: {response.text}")
                return None

        except requests.exceptions.Timeout:
            print("❌ 模型请求超时，请检查模型服务状态")
            return None
        except requests.exceptions.ConnectionError:
            print("❌ 无法连接到本地模型服务")
            return None
        except Exception as e:
            print(f"❌ 请求发生错误: {e}")
            return None

    def get_response_content(self, response: Dict) -> str:
        """
        从响应中提取内容

        :param response: 模型响应字典
        :return: 响应内容文本
        """
        if not response:
            return ""

        try:
            return response['choices'][0]['message']['content']
        except (KeyError, IndexError):
            return ""

    def analyze_investment(self, market_data: Dict, principles: str) -> str:
        """
        使用本地模型进行投资分析

        :param market_data: 市场数据字典
        :param principles: 投资原则文本
        :return: 分析结果
        """
        # 构建系统提示词
        system_prompt = f"""你是一位专业的投资顾问，精通技术分析和市场研判。

你必须严格遵守以下投资原则和策略：

{principles}

请基于以上原则，结合提供的市场数据，给出专业的投资建议。
你的建议必须：
1. 完全符合用户的投资原则
2. 基于技术指标和市场数据
3. 考虑风险控制和仓位管理
4. 给出明确的操作建议（买入/持有/卖出）
5. 解释决策理由

请用中文回答，保持专业且简洁。"""

        # 构建用户提示词
        user_prompt = f"""请分析以下市场数据并给出投资建议：

【基金代码】{market_data.get('fund_code', '未知')}
【分析日期】{market_data.get('analysis_date', '未知')}

【市场状态】
- 最新价格: {market_data['statistics']['latest_price']:.4f}
- 最新涨跌: {market_data['statistics']['latest_change']:+.2f}%
- 近期总收益: {market_data['statistics']['total_return']:+.2f}%
- 日均收益: {market_data['statistics']['avg_daily_return']:+.2f}%
- 波动率: {market_data['statistics']['volatility']:.2f}%
- 胜率: {market_data['statistics']['win_rate']:.1f}%

【技术指标】
- RSI(14): {market_data['technical']['rsi']:.1f}
- 5日动量: {market_data['technical']['momentum_5d']:+.2f}%
- 10日动量: {market_data['technical']['momentum_10d']:+.2f}%
- 相对MA5: {market_data['technical']['current_vs_ma5']:+.2f}%
- 相对MA10: {market_data['technical']['current_vs_ma10']:+.2f}%
- 相对MA20: {market_data['technical']['current_vs_ma20']:+.2f}%

【趋势分析】
- 方向: {market_data['trend']['direction']}
- 强度: {market_data['trend']['strength']}
- 动量: {market_data['trend']['momentum']:.1%}
- 近{market_data['trend']['recent_days']}天: {market_data['trend']['up_days']}涨 {market_data['trend']['down_days']}跌

【风险评估】
- 风险等级: {market_data['risk']['level']}
- RSI状态: {market_data['risk']['rsi_status']}
- 说明: {market_data['risk']['description']}

【基础交易信号】
- 信号: {market_data['signal']['signal']}
- 评分: {market_data['signal']['score']:.1f}
- 置信度: {market_data['signal']['confidence']:.1f}%

请基于以上数据和你的投资原则，给出：
1. 最终的操作建议（强烈买入/买入/持有/卖出/强烈卖出）
2. 建议的仓位比例（0-100%）
3. 详细的决策理由（至少3点）
4. 风险提示
5. 操作计划（什么时候买/卖，如何分批等）

请确保建议完全符合你的投资原则，特别是关于场内外基金选择、止盈策略、板块配置等方面的原则。"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        print("\n🤖 正在调用本地大模型进行深度分析...")
        print("⏳ 分析中，请稍候...")

        start_time = time.time()
        response = self.chat(messages, temperature=0.3)  # 较低温度以获得更稳定的建议
        elapsed_time = time.time() - start_time

        if response:
            content = self.get_response_content(response)
            if content:
                print(f"✅ 分析完成（耗时 {elapsed_time:.1f} 秒）\n")
                return content
            else:
                print("❌ 未能获取模型分析结果")
                return ""
        else:
            print("❌ 模型分析失败")
            return ""


# 全局客户端实例（单例模式）
_llm_client = None


def get_llm_client() -> Optional[LocalLLMClient]:
    """获取全局LLM客户端实例"""
    global _llm_client
    if _llm_client is None:
        try:
            _llm_client = LocalLLMClient()
        except Exception as e:
            print(f"⚠️  初始化本地模型客户端失败: {e}")
            return None
    return _llm_client


def test_llm_client():
    """测试LLM客户端"""
    print("=" * 80)
    print("测试本地大模型客户端")
    print("=" * 80)

    client = LocalLLMClient()

    # 简单测试
    messages = [
        {"role": "system", "content": "你是一个有帮助的助手。"},
        {"role": "user", "content": "请用一句话介绍什么是QDII基金？"}
    ]

    response = client.chat(messages)
    if response:
        content = client.get_response_content(response)
        print("\n模型回答:")
        print(content)
        print("\n✅ 测试成功！")
        return True
    else:
        print("\n❌ 测试失败")
        return False


if __name__ == "__main__":
    test_llm_client()
