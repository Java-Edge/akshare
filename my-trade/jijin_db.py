#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
基金估值数据库模块 (jijin_db)
用于存储和读取基金估值数据到MySQL数据库

作者: JavaEdge
日期: 2025-02-01
"""

import pymysql
from datetime import datetime
from typing import Dict, List, Optional
import logging

from database_config import MYSQL_CONFIG

logger = logging.getLogger(__name__)


class FundEstimateDB:
    """基金估值数据库操作类"""

    # 建表SQL
    CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS fund_estimate (
        id INT AUTO_INCREMENT PRIMARY KEY,
        fund_code VARCHAR(10) NOT NULL COMMENT '基金代码',
        fund_name VARCHAR(100) COMMENT '基金名称',
        estimate_nav DECIMAL(10, 4) COMMENT '估算净值',
        estimate_change DECIMAL(8, 4) COMMENT '估算涨跌幅(%)',
        estimate_change_amount DECIMAL(10, 4) COMMENT '估算涨跌额',
        estimate_time DATETIME COMMENT '估算时间',
        update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
        created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
        UNIQUE KEY uk_fund_code_time (fund_code, estimate_time),
        INDEX idx_fund_code (fund_code),
        INDEX idx_estimate_time (estimate_time),
        INDEX idx_update_time (update_time)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='基金估值数据表';
    """

    def __init__(self, config: Dict = None):
        """
        初始化数据库连接

        :param config: 数据库配置，如果不提供则使用默认配置
        """
        self.config = config or MYSQL_CONFIG
        self.connection = None
        self._init_database()

    def _get_connection(self):
        """获取数据库连接"""
        if self.connection is None or not self.connection.open:
            self.connection = pymysql.connect(
                host=self.config['host'],
                port=self.config['port'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database'],
                charset=self.config['charset'],
                cursorclass=pymysql.cursors.DictCursor
            )
        return self.connection

    def _init_database(self):
        """初始化数据库表"""
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(self.CREATE_TABLE_SQL)
                conn.commit()
            logger.info("✅ 基金估值数据表初始化成功")
        except Exception as e:
            logger.error(f"❌ 初始化数据库表失败: {e}")
            raise

    def save_estimate(self, fund_info: Dict) -> bool:
        """
        保存基金估值数据

        :param fund_info: 基金信息字典（来自fund_api）
        :return: 是否保存成功
        """
        try:
            # 解析数据
            fund_code = fund_info.get('基金代码', '')
            fund_name = fund_info.get('基金名称', '')
            estimate_nav = fund_info.get('实时估算净值', 0.0)

            # 解析涨跌幅
            rate_str = fund_info.get('实时估算增长率', '0%')
            try:
                estimate_change = float(rate_str.rstrip('%')) if rate_str != '---' else 0.0
            except (ValueError, AttributeError):
                estimate_change = 0.0

            # 计算涨跌额
            if estimate_nav and estimate_change:
                estimate_change_amount = round(estimate_nav * estimate_change / (100 + estimate_change), 4)
            else:
                estimate_change_amount = 0.0

            # 估算时间
            estimate_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # 插入或更新数据
            sql = """
            INSERT INTO fund_estimate 
            (fund_code, fund_name, estimate_nav, estimate_change, estimate_change_amount, estimate_time)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                fund_name = VALUES(fund_name),
                estimate_nav = VALUES(estimate_nav),
                estimate_change = VALUES(estimate_change),
                estimate_change_amount = VALUES(estimate_change_amount),
                update_time = CURRENT_TIMESTAMP
            """

            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(sql, (
                    fund_code, fund_name, estimate_nav, estimate_change,
                    estimate_change_amount, estimate_time
                ))
                conn.commit()

            logger.info(f"✅ 保存基金估值成功: {fund_code} - {fund_name}")
            return True

        except Exception as e:
            logger.error(f"❌ 保存基金估值失败: {e}")
            return False

    def get_latest_estimate(self, fund_code: str) -> Optional[Dict]:
        """
        获取基金最新的估值数据

        :param fund_code: 基金代码
        :return: 估值数据字典或None
        """
        try:
            sql = """
            SELECT 
                fund_code as code,
                fund_name as name,
                estimate_nav as estimateNav,
                estimate_change as estimateChange,
                estimate_change_amount as estimateChangeAmount,
                estimate_time as estimateTime,
                update_time as updateTime
            FROM fund_estimate
            WHERE fund_code = %s
            ORDER BY estimate_time DESC
            LIMIT 1
            """

            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(sql, (fund_code,))
                result = cursor.fetchone()

            if result:
                # 转换时间格式
                result['estimateTime'] = result['estimateTime'].strftime('%Y-%m-%d %H:%M:%S')
                result['updateTime'] = result['updateTime'].strftime('%Y-%m-%d %H:%M:%S')
                return result
            else:
                return None

        except Exception as e:
            logger.error(f"❌ 查询基金估值失败: {e}")
            return None

    def get_history_estimates(self, fund_code: str, days: int = 7) -> List[Dict]:
        """
        获取基金历史估值数据

        :param fund_code: 基金代码
        :param days: 获取最近N天的数据
        :return: 估值数据列表
        """
        try:
            sql = """
            SELECT 
                fund_code as code,
                fund_name as name,
                estimate_nav as estimateNav,
                estimate_change as estimateChange,
                estimate_change_amount as estimateChangeAmount,
                estimate_time as estimateTime,
                update_time as updateTime
            FROM fund_estimate
            WHERE fund_code = %s
            AND estimate_time >= DATE_SUB(NOW(), INTERVAL %s DAY)
            ORDER BY estimate_time DESC
            """

            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(sql, (fund_code, days))
                results = cursor.fetchall()

            # 转换时间格式
            for result in results:
                result['estimateTime'] = result['estimateTime'].strftime('%Y-%m-%d %H:%M:%S')
                result['updateTime'] = result['updateTime'].strftime('%Y-%m-%d %H:%M:%S')

            return results

        except Exception as e:
            logger.error(f"❌ 查询历史估值失败: {e}")
            return []

    def batch_save_estimates(self, fund_infos: List[Dict]) -> int:
        """
        批量保存基金估值数据

        :param fund_infos: 基金信息列表
        :return: 成功保存的数量
        """
        success_count = 0
        for fund_info in fund_infos:
            if self.save_estimate(fund_info):
                success_count += 1

        logger.info(f"✅ 批量保存完成: {success_count}/{len(fund_infos)} 个基金")
        return success_count

    def close(self):
        """关闭数据库连接"""
        if self.connection and self.connection.open:
            self.connection.close()
            logger.info("数据库连接已关闭")


def test_fund_estimate_db():
    """测试基金估值数据库功能"""
    from fund_api import FundAPI

    print("=" * 80)
    print("测试基金估值数据库功能")
    print("=" * 80)

    # 初始化
    db = FundEstimateDB()
    api = FundAPI()

    # 测试1: 保存单个基金估值
    print("\n【测试1】保存单个基金估值")
    print("-" * 80)
    fund_info = api.get_fund_realtime_value("000001")
    if fund_info:
        success = db.save_estimate(fund_info)
        print(f"保存结果: {'✅ 成功' if success else '❌ 失败'}")

    # 测试2: 查询最新估值
    print("\n【测试2】查询最新估值")
    print("-" * 80)
    latest = db.get_latest_estimate("000001")
    if latest:
        print(f"基金代码: {latest['code']}")
        print(f"基金名称: {latest['name']}")
        print(f"估算净值: {latest['estimateNav']}")
        print(f"估算涨跌幅: {latest['estimateChange']}%")
        print(f"估算时间: {latest['estimateTime']}")

    # 测试3: 批量保存
    print("\n【测试3】批量保存基金估值")
    print("-" * 80)
    fund_codes = ["000001", "161116"]
    fund_infos = []
    for code in fund_codes:
        info = api.get_fund_realtime_value(code)
        if info:
            fund_infos.append(info)

    count = db.batch_save_estimates(fund_infos)
    print(f"批量保存成功: {count} 个基金")

    # 关闭连接
    db.close()

    print("\n" + "=" * 80)
    print("✅ 测试完成")
    print("=" * 80)


if __name__ == "__main__":
    test_fund_estimate_db()
