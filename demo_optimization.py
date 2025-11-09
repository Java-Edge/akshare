#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
QDII优化效果演示脚本
演示三种场景下的数据保存行为
"""

import pymysql
import database_config
import subprocess
import sys

def run_command(cmd):
    """运行命令并返回输出"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr

def get_data_count():
    """获取数据库中的数据条数"""
    conn = pymysql.connect(**database_config.MYSQL_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM qdii_fund_data WHERE fund_code='513100'")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

def demo_scenario_1():
    """场景1：数据库已有所有数据"""
    print("\n" + "="*70)
    print("📊 场景1：数据库已有所有数据（应该显示：无需保存）")
    print("="*70)

    count = get_data_count()
    print(f"当前数据库中有 {count} 条数据\n")

    if count < 30:
        print("⚠️  数据不足30条，需要先获取完整数据")
        print("运行程序中...\n")
        output = run_command("cd /Users/javaedge/soft/PyCharmProjects/akshare && python qdii-stock-plan.py 2>&1 | grep -E '保存|无需|数据库'")
        print(output)
    else:
        print("运行程序中...\n")
        output = run_command("cd /Users/javaedge/soft/PyCharmProjects/akshare && python qdii-stock-plan.py 2>&1 | grep -E '保存|无需|数据库已包含'")
        print(output)

        if "无需保存" in output:
            print("\n✅ 成功！程序正确识别到数据库已有所有数据，没有重复保存")
        else:
            print("\n❌ 失败！程序应该显示'无需保存'")

def demo_scenario_2():
    """场景2：数据库缺少部分数据"""
    print("\n" + "="*70)
    print("📊 场景2：删除3条数据后（应该显示：正在保存 X 条新数据）")
    print("="*70)

    # 删除最近3条数据
    conn = pymysql.connect(**database_config.MYSQL_CONFIG)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM qdii_fund_data WHERE fund_code='513100' ORDER BY trade_date DESC LIMIT 3")
    conn.commit()
    cursor.close()
    conn.close()

    count = get_data_count()
    print(f"删除后数据库中有 {count} 条数据\n")

    print("运行程序中...\n")
    output = run_command("cd /Users/javaedge/soft/PyCharmProjects/akshare && python qdii-stock-plan.py 2>&1 | grep -E '保存|缺失|合并'")
    print(output)

    if "条新数据" in output or "缺失" in output:
        print("\n✅ 成功！程序检测到缺失数据并尝试补充")
    else:
        print("\n⚠️  注意：可能因网络问题未能获取API数据")

def main():
    print("🎯 QDII基金数据保存优化效果演示")
    print("="*70)
    print("\n本演示将展示以下场景：")
    print("1. 数据库已有所有数据 → 应该显示'无需保存'")
    print("2. 数据库缺少部分数据 → 应该显示'正在保存 X 条新数据'")

    choice = input("\n请选择要演示的场景 (1/2/q退出): ").strip()

    if choice == '1':
        demo_scenario_1()
    elif choice == '2':
        demo_scenario_2()
    elif choice.lower() == 'q':
        print("退出演示")
        return
    else:
        print("无效选择")

    print("\n" + "="*70)
    print("演示完成！")
    print("="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n演示已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 演示过程中发生错误: {e}")
        sys.exit(1)

