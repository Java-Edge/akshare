#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
基金估值计算模块 - 基于持仓和股票实时行情
由于监管要求，基金实时估值API可能下架，本模块通过以下方式计算估值：
1. 获取基金最新持仓（前十大重仓股）
2. 获取这些股票的实时行情
3. 根据持仓比例计算基金估值

作者: JavaEdge
日期: 2025-02-02
"""

import akshare as ak
import pandas as pd
from typing import Dict, Optional, List, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FundEstimateCalculator:
    """基金估值计算器"""

    def __init__(self):
        """初始化计算器"""
        self.stock_quote_cache = {}  # 股票行情缓存
        self.fund_holdings_cache = {}  # 基金持仓缓存

    def get_fund_holdings(self, fund_code: str, year: str = None) -> Optional[pd.DataFrame]:
        """
        获取基金持仓数据（前十大重仓股）

        :param fund_code: 基金代码
        :param year: 年份，默认最新年份
        :return: 持仓数据DataFrame
        """
        try:
            if year is None:
                year = str(datetime.now().year)

            cache_key = f"{fund_code}_{year}"
            if cache_key in self.fund_holdings_cache:
                logger.info(f"从缓存获取基金 {fund_code} 持仓数据")
                return self.fund_holdings_cache[cache_key]

            logger.info(f"获取基金 {fund_code} 的持仓数据...")

            # 使用akshare获取基金持仓
            holdings_df = ak.fund_portfolio_hold_em(symbol=fund_code, date=year)

            if holdings_df is None or holdings_df.empty:
                logger.warning(f"未获取到基金 {fund_code} 的持仓数据")
                return None

            # 缓存数据
            self.fund_holdings_cache[cache_key] = holdings_df

            logger.info(f"✅ 获取到 {len(holdings_df)} 只重仓股")
            return holdings_df

        except Exception as e:
            logger.error(f"获取基金持仓失败: {e}")
            return None

    def get_stock_realtime_price(self, stock_codes: List[str]) -> Dict[str, float]:
        """
        获取股票实时价格

        :param stock_codes: 股票代码列表
        :return: {股票代码: 最新价} 字典
        """
        try:
            logger.info(f"获取 {len(stock_codes)} 只股票的实时行情...")

            # 获取A股实时行情
            spot_df = ak.stock_zh_a_spot_em()

            if spot_df is None or spot_df.empty:
                logger.warning("未获取到股票实时行情")
                return {}

            # 提取目标股票价格
            price_dict = {}
            for code in stock_codes:
                stock_data = spot_df[spot_df['代码'] == code]
                if not stock_data.empty:
                    price = float(stock_data.iloc[0]['最新价'])
                    price_dict[code] = price
                    logger.debug(f"  {code}: {price:.2f}")
                else:
                    logger.warning(f"  未找到股票 {code} 的行情")

            logger.info(f"✅ 成功获取 {len(price_dict)}/{len(stock_codes)} 只股票行情")
            return price_dict

        except Exception as e:
            logger.error(f"获取股票实时行情失败: {e}")
            return {}

    def calculate_fund_estimate(self, fund_code: str, base_nav: float = None) -> Optional[Dict]:
        """
        计算基金实时估值

        计算逻辑：
        1. 获取基金持仓（前十大重仓股及其占净值比例）
        2. 获取这些股票的实时涨跌幅
        3. 加权计算：估算涨跌幅 = Σ(持仓比例 × 股票涨跌幅)
        4. 计算估算净值 = 上一日净值 × (1 + 估算涨跌幅)

        :param fund_code: 基金代码
        :param base_nav: 基准净值（上一日净值），不提供则无法计算估算净值
        :return: 估值结果字典
        """
        try:
            logger.info(f"=" * 80)
            logger.info(f"开始计算基金 {fund_code} 的实时估值")
            logger.info(f"=" * 80)

            # 1. 获取基金持仓
            holdings_df = self.get_fund_holdings(fund_code)

            if holdings_df is None or holdings_df.empty:
                return {
                    'success': False,
                    'message': '无法获取基金持仓数据',
                    'fund_code': fund_code
                }

            # 2. 提取股票代码和持仓比例
            stock_codes = holdings_df['股票代码'].tolist()
            holding_ratios = holdings_df['占净值比例'].tolist()  # 单位：%

            logger.info(f"持仓股票数: {len(stock_codes)}")
            logger.info(f"前三大重仓股:")
            for i in range(min(3, len(holdings_df))):
                row = holdings_df.iloc[i]
                logger.info(f"  {i+1}. {row['股票名称']}({row['股票代码']}): {row['占净值比例']}%")

            # 3. 获取股票实时行情
            price_dict = self.get_stock_realtime_price(stock_codes)

            if not price_dict:
                return {
                    'success': False,
                    'message': '无法获取股票实时行情',
                    'fund_code': fund_code
                }

            # 4. 获取股票涨跌幅（需要昨收价）
            spot_df = ak.stock_zh_a_spot_em()

            weighted_change = 0.0  # 加权涨跌幅
            total_weight = 0.0     # 总权重（用于标准化）
            stock_changes = []     # 记录每只股票的贡献

            for i, code in enumerate(stock_codes):
                if code not in price_dict:
                    continue

                stock_data = spot_df[spot_df['代码'] == code]
                if stock_data.empty:
                    continue

                row = stock_data.iloc[0]
                stock_name = row['名称']
                latest_price = float(row['最新价'])
                yesterday_close = float(row['昨收'])

                # 计算涨跌幅
                if yesterday_close > 0:
                    change_pct = ((latest_price - yesterday_close) / yesterday_close) * 100
                else:
                    change_pct = 0.0

                # 持仓比例
                ratio = float(holding_ratios[i])

                # 加权贡献
                contribution = ratio * change_pct / 100
                weighted_change += contribution
                total_weight += ratio

                stock_changes.append({
                    'code': code,
                    'name': stock_name,
                    'ratio': ratio,
                    'change_pct': change_pct,
                    'contribution': contribution
                })

                logger.debug(f"{stock_name}({code}): 涨跌{change_pct:+.2f}%, 占比{ratio:.2f}%, 贡献{contribution:+.4f}%")

            # 5. 计算估算涨跌幅
            # 注意：前十大重仓股通常占基金净值的40-60%
            # 我们按实际权重进行标准化
            if total_weight > 0:
                estimated_change_pct = weighted_change  # 这是基于持仓比例的加权涨跌幅
            else:
                estimated_change_pct = 0.0

            logger.info(f"\n估算涨跌幅: {estimated_change_pct:+.4f}% (基于{total_weight:.2f}%的重仓股)")

            # 6. 计算估算净值
            estimated_nav = None
            if base_nav and base_nav > 0:
                estimated_nav = base_nav * (1 + estimated_change_pct / 100)
                logger.info(f"基准净值: {base_nav:.4f}")
                logger.info(f"估算净值: {estimated_nav:.4f}")

            # 7. 组装结果
            result = {
                'success': True,
                'fund_code': fund_code,
                'estimate_change': round(estimated_change_pct, 4),  # 估算涨跌幅(%)
                'estimate_nav': round(estimated_nav, 4) if estimated_nav else None,  # 估算净值
                'base_nav': base_nav,  # 基准净值
                'holdings_count': len(stock_changes),  # 持仓股票数
                'total_holding_ratio': round(total_weight, 2),  # 总持仓比例(%)
                'stock_details': stock_changes,  # 详细股票贡献
                'calculate_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'message': f'基于{len(stock_changes)}只重仓股({total_weight:.1f}%持仓)计算'
            }

            logger.info(f"✅ 估值计算完成")
            logger.info(f"=" * 80)

            return result

        except Exception as e:
            logger.error(f"计算基金估值失败: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'message': f'计算失败: {str(e)}',
                'fund_code': fund_code
            }

    def print_estimate_result(self, result: Dict):
        """
        格式化打印估值结果

        :param result: 估值结果字典
        """
        if not result.get('success'):
            print(f"\n❌ 计算失败: {result.get('message')}")
            return

        print("\n" + "=" * 80)
        print("  📊 基金实时估值（基于持仓计算）")
        print("=" * 80)
        print(f"  基金代码: {result['fund_code']}")
        print(f"  计算时间: {result['calculate_time']}")
        print(f"  计算依据: {result['message']}")
        print("-" * 80)

        # 估算结果
        change = result['estimate_change']
        if change >= 0:
            print(f"  📈 估算涨跌幅: +{change:.4f}% 🔴")
        else:
            print(f"  📉 估算涨跌幅: {change:.4f}% 🟢")

        if result.get('estimate_nav'):
            print(f"  💰 估算净值: {result['estimate_nav']:.4f}")
            print(f"  📊 基准净值: {result['base_nav']:.4f}")

        print(f"  📦 持仓股票: {result['holdings_count']}只")
        print(f"  ⚖️  总持仓比例: {result['total_holding_ratio']}%")

        # 前5大贡献
        if result.get('stock_details'):
            print("\n  前5大贡献股票:")
            sorted_stocks = sorted(
                result['stock_details'],
                key=lambda x: abs(x['contribution']),
                reverse=True
            )
            for i, stock in enumerate(sorted_stocks[:5]):
                emoji = "🔴" if stock['change_pct'] >= 0 else "🟢"
                print(f"    {i+1}. {stock['name']}({stock['code']})")
                print(f"       涨跌: {stock['change_pct']:+.2f}% {emoji} | 占比: {stock['ratio']:.2f}% | 贡献: {stock['contribution']:+.4f}%")

        print("=" * 80)
        print("  ⚠️  注意: 此估值基于前十大重仓股计算，仅供参考！")
        print("=" * 80 + "\n")


def demo_fund_estimate_calculator():
    """演示基金估值计算功能"""
    print("\n" + "=" * 80)
    print("  基金估值计算器演示")
    print("=" * 80)

    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    calculator = FundEstimateCalculator()

    # 示例1: 计算华夏成长混合（000001）
    print("\n【示例1】计算华夏成长混合(000001)的实时估值")
    print("-" * 80)

    # 假设上一日净值为1.1730（实际使用时应该从数据库或API获取）
    result = calculator.calculate_fund_estimate(
        fund_code="000001",
        base_nav=1.1730
    )

    if result:
        calculator.print_estimate_result(result)

    # 示例2: 计算易方达蓝筹精选混合（005827）
    print("\n【示例2】计算易方达蓝筹精选混合(005827)的实时估值")
    print("-" * 80)

    result2 = calculator.calculate_fund_estimate(
        fund_code="005827",
        base_nav=2.5000  # 假设值
    )

    if result2:
        calculator.print_estimate_result(result2)


if __name__ == "__main__":
    demo_fund_estimate_calculator()
