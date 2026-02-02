#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
场外基金实时估值API封装
提供便捷的基金数据查询接口

作者: JavaEdge
日期: 2025-02-01
"""

import akshare as ak
import pandas as pd
from typing import Optional, Dict, List
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')


class FundAPI:
    """场外基金API封装类"""

    def __init__(self):
        """初始化基金API"""
        self.fund_types = {
            '全部': 'all',
            '股票型': 'stock',
            '混合型': 'mixed',
            '债券型': 'bond',
            '指数型': 'index',
            'QDII': 'qdii',
            'ETF联接': 'etf_connection',
            'LOF': 'lof',
            '场内交易基金': 'on_exchange'
        }

    def get_fund_realtime_value(self, fund_code: str) -> Optional[Dict]:
        """
        获取指定场外基金的实时估值

        :param fund_code: 6位基金代码，如 '000001'
        :return: 包含基金实时估值信息的字典，失败返回None
        """
        try:
            # 获取所有基金的实时估值数据
            print(f"📊 正在查询基金 {fund_code} 的实时估值...")
            df = ak.fund_value_estimation_em(symbol="全部")

            if df is None or df.empty:
                print(f"❌ 未获取到任何基金数据")
                return None

            # 筛选指定基金代码
            fund_data = df[df['基金代码'] == fund_code]

            if fund_data.empty:
                print(f"❌ 未找到基金代码 {fund_code} 的数据")
                print(f"💡 提示：请确认基金代码是否正确，或该基金是否为场外基金")
                return None

            # 提取第一条记录（应该只有一条）
            row = fund_data.iloc[0]

            # 获取估算日期列名（动态的，包含日期）
            estimation_cols = [col for col in df.columns if '估算数据-估算值' in col]
            estimation_rate_cols = [col for col in df.columns if '估算数据-估算增长率' in col]
            public_value_cols = [col for col in df.columns if '公布数据-单位净值' in col]
            public_rate_cols = [col for col in df.columns if '公布数据-日增长率' in col]
            last_value_cols = [col for col in df.columns if '单位净值' in col and '公布数据' not in col]

            # 提取数据
            fund_info = {
                '基金代码': str(row['基金代码']),
                '基金名称': str(row['基金名称']),
                '查询时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }

            # 添加估算数据
            if estimation_cols:
                estimation_value = row[estimation_cols[0]]
                try:
                    fund_info['实时估算净值'] = float(estimation_value) if pd.notna(estimation_value) and str(estimation_value) != '---' else None
                except (ValueError, TypeError):
                    fund_info['实时估算净值'] = None

            if estimation_rate_cols:
                estimation_rate = row[estimation_rate_cols[0]]
                fund_info['实时估算增长率'] = str(estimation_rate) if pd.notna(estimation_rate) else '---'

            # 添加公布数据
            if public_value_cols:
                public_value = row[public_value_cols[0]]
                try:
                    fund_info['最新公布净值'] = float(public_value) if pd.notna(public_value) and str(public_value) != '---' else None
                except (ValueError, TypeError):
                    fund_info['最新公布净值'] = None

            if public_rate_cols:
                public_rate = row[public_rate_cols[0]]
                fund_info['最新公布增长率'] = str(public_rate) if pd.notna(public_rate) else '---'

            # 添加估算偏差
            if '估算偏差' in row:
                fund_info['估算偏差'] = str(row['估算偏差']) if pd.notna(row['估算偏差']) else '---'

            # 添加历史净值
            if last_value_cols:
                last_value = row[last_value_cols[0]]
                try:
                    fund_info['上一日净值'] = float(last_value) if pd.notna(last_value) and str(last_value) != '---' else None
                except (ValueError, TypeError):
                    fund_info['上一日净值'] = None

            return fund_info

        except Exception as e:
            print(f"❌ 查询基金 {fund_code} 时发生错误: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_funds_by_type(self, fund_type: str = "全部") -> Optional[pd.DataFrame]:
        """
        获取指定类型的所有基金实时估值

        :param fund_type: 基金类型，可选: '全部', '股票型', '混合型', '债券型', '指数型', 'QDII', 'ETF联接', 'LOF', '场内交易基金'
        :return: 包含所有基金数据的DataFrame
        """
        try:
            if fund_type not in self.fund_types:
                print(f"❌ 不支持的基金类型: {fund_type}")
                print(f"💡 支持的类型: {list(self.fund_types.keys())}")
                return None

            print(f"📊 正在查询 {fund_type} 基金的实时估值...")
            df = ak.fund_value_estimation_em(symbol=fund_type)

            if df is None or df.empty:
                print(f"❌ 未获取到 {fund_type} 基金数据")
                return None

            print(f"✅ 成功获取 {len(df)} 只基金的实时估值数据")
            return df

        except Exception as e:
            print(f"❌ 查询 {fund_type} 基金时发生错误: {e}")
            import traceback
            traceback.print_exc()
            return None

    def search_funds(self, keyword: str) -> Optional[pd.DataFrame]:
        """
        根据关键词搜索基金

        :param keyword: 搜索关键词（基金名称或代码）
        :return: 匹配的基金数据DataFrame
        """
        try:
            print(f"🔍 正在搜索包含 '{keyword}' 的基金...")
            df = ak.fund_value_estimation_em(symbol="全部")

            if df is None or df.empty:
                print(f"❌ 未获取到基金数据")
                return None

            # 搜索基金代码或名称中包含关键词的记录
            mask = (df['基金代码'].astype(str).str.contains(keyword, na=False) |
                    df['基金名称'].astype(str).str.contains(keyword, na=False))
            result = df[mask]

            if result.empty:
                print(f"❌ 未找到包含 '{keyword}' 的基金")
                return None

            print(f"✅ 找到 {len(result)} 只相关基金")
            return result

        except Exception as e:
            print(f"❌ 搜索基金时发生错误: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_top_funds(self, fund_type: str = "全部", top_n: int = 10,
                      sort_by: str = "估算增长率") -> Optional[pd.DataFrame]:
        """
        获取涨幅排名前N的基金

        :param fund_type: 基金类型
        :param top_n: 返回前N只基金
        :param sort_by: 排序字段，'估算增长率' 或 '公布增长率'
        :return: 排序后的基金数据DataFrame
        """
        try:
            df = self.get_funds_by_type(fund_type)

            if df is None or df.empty:
                return None

            # 找到估算增长率列
            rate_cols = [col for col in df.columns if '估算数据-估算增长率' in col]

            if not rate_cols:
                print(f"❌ 未找到估算增长率数据列")
                return None

            rate_col = rate_cols[0]

            # 转换增长率为数值类型（去除%号）
            df[rate_col + '_num'] = df[rate_col].astype(str).str.rstrip('%').replace('---', None)
            df[rate_col + '_num'] = pd.to_numeric(df[rate_col + '_num'], errors='coerce')

            # 排序并获取前N只
            result = df.dropna(subset=[rate_col + '_num']).nlargest(top_n, rate_col + '_num')

            print(f"✅ 获取涨幅前 {top_n} 的基金:")
            return result

        except Exception as e:
            print(f"❌ 获取排名时发生错误: {e}")
            import traceback
            traceback.print_exc()
            return None

    def print_fund_info(self, fund_info: Dict):
        """
        格式化打印基金信息

        :param fund_info: 基金信息字典
        """
        if not fund_info:
            print("❌ 无基金信息可显示")
            return

        print("\n" + "=" * 80)
        print(f"  📈 基金实时估值信息")
        print("=" * 80)
        print(f"  基金代码: {fund_info.get('基金代码', 'N/A')}")
        print(f"  基金名称: {fund_info.get('基金名称', 'N/A')}")
        print(f"  查询时间: {fund_info.get('查询时间', 'N/A')}")
        print("-" * 80)

        # 实时估算数据
        if fund_info.get('实时估算净值'):
            print(f"  💰 实时估算净值: {fund_info.get('实时估算净值'):.4f}")
            estimation_rate = fund_info.get('实时估算增长率', '---')
            if estimation_rate != '---':
                rate_num = float(estimation_rate.rstrip('%'))
                if rate_num > 0:
                    print(f"  📈 实时估算增长率: +{estimation_rate} 🔴")
                elif rate_num < 0:
                    print(f"  📉 实时估算增长率: {estimation_rate} 🟢")
                else:
                    print(f"  ➡️  实时估算增长率: {estimation_rate} ⚪")
            else:
                print(f"  📊 实时估算增长率: {estimation_rate}")
        else:
            print(f"  💰 实时估算净值: 暂无数据")

        print("-" * 80)

        # 最新公布数据
        if fund_info.get('最新公布净值'):
            print(f"  📊 最新公布净值: {fund_info.get('最新公布净值'):.4f}")
            print(f"  📊 最新公布增长率: {fund_info.get('最新公布增长率', '---')}")
        else:
            print(f"  📊 最新公布净值: 暂无数据")

        if fund_info.get('上一日净值'):
            print(f"  📊 上一日净值: {fund_info.get('上一日净值'):.4f}")

        if fund_info.get('估算偏差') and fund_info.get('估算偏差') != '---':
            print(f"  📊 估算偏差: {fund_info.get('估算偏差')}")

        print("=" * 80 + "\n")


def demo_fund_query():
    """演示基金查询功能"""
    api = FundAPI()

    print("\n🎯 场外基金实时估值API演示\n")

    # 示例1: 查询单个基金
    print("【示例1】查询单个基金实时估值")
    print("-" * 80)
    fund_code = "000001"  # 华夏成长混合
    fund_info = api.get_fund_realtime_value(fund_code)
    if fund_info:
        api.print_fund_info(fund_info)

    # 示例2: 查询QDII基金
    print("\n【示例2】查询QDII基金")
    print("-" * 80)
    fund_code = "161116"  # 易方达黄金主题
    fund_info = api.get_fund_realtime_value(fund_code)
    if fund_info:
        api.print_fund_info(fund_info)

    # 示例3: 搜索基金
    print("\n【示例3】搜索包含'黄金'的基金")
    print("-" * 80)
    result = api.search_funds("黄金")
    if result is not None:
        # 只显示前5条
        display_cols = ['基金代码', '基金名称']
        estimation_cols = [col for col in result.columns if '估算增长率' in col]
        if estimation_cols:
            display_cols.append(estimation_cols[0])
        print(result[display_cols].head())

    # 示例4: 获取涨幅前10的QDII基金
    print("\n【示例4】获取涨幅前10的QDII基金")
    print("-" * 80)
    top_funds = api.get_top_funds(fund_type="QDII", top_n=10)
    if top_funds is not None:
        display_cols = ['基金代码', '基金名称']
        estimation_cols = [col for col in top_funds.columns if '估算增长率' in col]
        if estimation_cols:
            display_cols.append(estimation_cols[0])
        print(top_funds[display_cols])


if __name__ == "__main__":
    demo_fund_query()
