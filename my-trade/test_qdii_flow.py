#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
测试QDII基金数据获取和保存流程
"""

import pymysql
import database_config

def test_data_flow():
    """测试数据流程"""
    conn = pymysql.connect(**database_config.MYSQL_CONFIG)
    cursor = conn.cursor()

    print("=" * 60)
    print("测试场景1: 数据库已有所有数据")
    print("=" * 60)

    # 查看当前数据
    cursor.execute("SELECT COUNT(*) FROM qdii_fund_data WHERE fund_code='513100'")
    count = cursor.fetchone()[0]
    print(f"✅ 数据库中有 {count} 条数据")

    if count >= 30:
        print("✅ 数据充足，运行程序应该显示：'✅ 无需保存，数据库已是最新'\n")
    else:
        print(f"⚠️  数据不足30条，运行程序会尝试从API获取缺失的数据\n")

    print("=" * 60)
    print("测试场景2: 模拟删除最新数据")
    print("=" * 60)

    # 删除最近3条数据
    cursor.execute("SELECT trade_date FROM qdii_fund_data WHERE fund_code='513100' ORDER BY trade_date DESC LIMIT 3")
    deleted_dates = cursor.fetchall()

    if deleted_dates:
        cursor.execute("DELETE FROM qdii_fund_data WHERE fund_code='513100' ORDER BY trade_date DESC LIMIT 3")
        conn.commit()
        print(f"✅ 已删除最近3条数据（日期: {[str(d[0]) for d in deleted_dates]}）")

        cursor.execute("SELECT COUNT(*) FROM qdii_fund_data WHERE fund_code='513100'")
        new_count = cursor.fetchone()[0]
        print(f"✅ 现在数据库中有 {new_count} 条数据")
        print("✅ 运行程序应该会：")
        print("   1. 检测到缺失3个交易日")
        print("   2. 从API获取这3天的数据")
        print("   3. 显示：'💾 正在保存 X 条新数据到数据库...'")
        print("\n💡 现在运行 python qdii-stock-plan.py 来测试\n")
    else:
        print("⚠️  没有数据可删除")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    test_data_flow()

