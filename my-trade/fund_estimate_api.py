#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
基金估值后端API服务
提供RESTful API接口给前端调用

作者: JavaEdge
日期: 2025-02-01
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import logging
from typing import Dict, Optional
import traceback

from fund_api import FundAPI
from jijin_db import FundEstimateDB

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 启用跨域支持

# 初始化基金API（启用Redis缓存，TTL=30秒）
fund_api = FundAPI(use_redis=True, redis_ttl=30)

# 初始化数据库
try:
    fund_db = FundEstimateDB()
    logger.info("✅ 数据库连接成功")
except Exception as e:
    logger.warning(f"⚠️  数据库连接失败: {e}，将仅使用API模式")
    fund_db = None


def parse_estimate_rate(rate_str: str) -> float:
    """
    解析估算增长率字符串为浮点数

    :param rate_str: 增长率字符串，如 "0.65%" 或 "-0.03%"
    :return: 浮点数，如 0.65 或 -0.03
    """
    try:
        if rate_str == '---' or not rate_str:
            return 0.0
        # 去除%号并转换为浮点数
        return float(rate_str.rstrip('%'))
    except (ValueError, AttributeError):
        return 0.0


def calculate_change_amount(current_value: float, rate: float) -> float:
    """
    计算涨跌额

    :param current_value: 当前净值
    :param rate: 涨跌幅（百分比）
    :return: 涨跌额
    """
    if not current_value or not rate:
        return 0.0
    # 涨跌额 = 当前净值 / (1 + 涨跌幅/100) * 涨跌幅/100
    return round(current_value * rate / (100 + rate), 4)


def convert_to_fund_estimate(fund_info: Dict) -> Dict:
    """
    将fund_info转换为前端需要的FundEstimate格式

    :param fund_info: 基金信息字典
    :return: FundEstimate格式的字典
    """
    # 解析估算增长率
    rate_str = fund_info.get('实时估算增长率', '0%')
    estimate_change = parse_estimate_rate(rate_str)

    # 获取估算净值
    estimate_nav = fund_info.get('实时估算净值', 0.0)
    if estimate_nav is None:
        estimate_nav = 0.0

    # 计算涨跌额
    estimate_change_amount = calculate_change_amount(estimate_nav, estimate_change)

    # 获取当前时间作为估算时间
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return {
        'code': fund_info.get('基金代码', ''),
        'estimateNav': round(float(estimate_nav), 4) if estimate_nav else 0.0,
        'estimateChange': round(estimate_change, 2),
        'estimateChangeAmount': round(estimate_change_amount, 4),
        'estimateTime': current_time,
        'updateTime': fund_info.get('查询时间', current_time)
    }


@app.route('/api/fund/estimate/<fund_code>', methods=['GET'])
def get_fund_estimate(fund_code: str):
    """
    获取单个基金的实时估值

    路径参数:
        fund_code: 基金代码（6位数字）

    查询参数:
        use_cache: 是否使用缓存（默认true）

    返回:
        {
            "success": true,
            "data": {
                "code": "000001",
                "estimateNav": 1.1806,
                "estimateChange": 0.65,
                "estimateChangeAmount": 0.0076,
                "estimateTime": "2026-02-01 22:00:00",
                "updateTime": "2026-02-01 22:00:00"
            },
            "message": "查询成功"
        }
    """
    try:
        logger.info(f"收到查询请求，基金代码: {fund_code}")

        # 验证基金代码格式
        if not fund_code or len(fund_code) != 6 or not fund_code.isdigit():
            return jsonify({
                'success': False,
                'data': None,
                'message': '基金代码格式错误，请输入6位数字'
            }), 400

        # 检查是否使用缓存
        use_cache = request.args.get('use_cache', 'true').lower() == 'true'

        # 如果启用缓存且数据库可用，先尝试从数据库获取
        if use_cache and fund_db:
            cached_data = fund_db.get_latest_estimate(fund_code)
            if cached_data:
                logger.info(f"从缓存获取数据: {fund_code}")
                return jsonify({
                    'success': True,
                    'data': cached_data,
                    'message': '查询成功（来自缓存）',
                    'cached': True
                }), 200

        # 查询基金信息
        fund_info = fund_api.get_fund_realtime_value(fund_code)

        if not fund_info:
            return jsonify({
                'success': False,
                'data': None,
                'message': f'未找到基金代码 {fund_code} 的数据，请确认基金代码是否正确'
            }), 404

        # 转换为前端格式
        estimate_data = convert_to_fund_estimate(fund_info)

        # 保存到数据库
        if fund_db:
            try:
                fund_db.save_estimate(fund_info)
                logger.info(f"已保存到数据库: {fund_code}")
            except Exception as e:
                logger.warning(f"保存到数据库失败: {e}")

        logger.info(f"查询成功: {fund_code} - {fund_info.get('基金名称', 'N/A')}")

        return jsonify({
            'success': True,
            'data': estimate_data,
            'message': '查询成功',
            'cached': False
        }), 200

    except Exception as e:
        logger.error(f"查询基金 {fund_code} 时发生错误: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'data': None,
            'message': f'服务器错误: {str(e)}'
        }), 500


@app.route('/api/fund/estimate/batch', methods=['POST'])
def get_fund_estimates_batch():
    """
    批量获取基金实时估值

    请求体:
        {
            "codes": ["000001", "161116", "110022"]
        }

    返回:
        {
            "success": true,
            "data": [
                {
                    "code": "000001",
                    "estimateNav": 1.1806,
                    ...
                },
                ...
            ],
            "message": "查询成功"
        }
    """
    try:
        data = request.get_json()
        codes = data.get('codes', [])

        if not codes or not isinstance(codes, list):
            return jsonify({
                'success': False,
                'data': None,
                'message': '请提供基金代码列表'
            }), 400

        logger.info(f"收到批量查询请求，基金数量: {len(codes)}")

        results = []
        failed_codes = []

        for code in codes:
            try:
                # 验证基金代码
                if not code or len(code) != 6 or not code.isdigit():
                    failed_codes.append({'code': code, 'reason': '格式错误'})
                    continue

                # 查询基金信息
                fund_info = fund_api.get_fund_realtime_value(code)

                if fund_info:
                    estimate_data = convert_to_fund_estimate(fund_info)
                    results.append(estimate_data)
                else:
                    failed_codes.append({'code': code, 'reason': '未找到数据'})

            except Exception as e:
                logger.error(f"查询基金 {code} 失败: {str(e)}")
                failed_codes.append({'code': code, 'reason': str(e)})

        message = f"查询成功 {len(results)}/{len(codes)} 个基金"
        if failed_codes:
            message += f"，{len(failed_codes)} 个失败"

        logger.info(message)

        return jsonify({
            'success': True,
            'data': results,
            'failed': failed_codes,
            'message': message
        }), 200

    except Exception as e:
        logger.error(f"批量查询时发生错误: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'data': None,
            'message': f'服务器错误: {str(e)}'
        }), 500


@app.route('/api/fund/search', methods=['GET'])
def search_funds():
    """
    搜索基金

    查询参数:
        keyword: 搜索关键词（基金代码或名称）

    返回:
        {
            "success": true,
            "data": [
                {
                    "code": "000001",
                    "name": "华夏成长混合",
                    "estimateNav": 1.1806,
                    "estimateChange": 0.65
                },
                ...
            ],
            "message": "查询成功"
        }
    """
    try:
        keyword = request.args.get('keyword', '')

        if not keyword:
            return jsonify({
                'success': False,
                'data': None,
                'message': '请提供搜索关键词'
            }), 400

        logger.info(f"收到搜索请求，关键词: {keyword}")

        # 搜索基金
        result_df = fund_api.search_funds(keyword)

        if result_df is None or result_df.empty:
            return jsonify({
                'success': False,
                'data': [],
                'message': f'未找到包含 "{keyword}" 的基金'
            }), 404

        # 转换为列表格式
        results = []
        for _, row in result_df.iterrows():
            # 获取估算增长率列
            rate_cols = [col for col in result_df.columns if '估算增长率' in col]
            rate_str = str(row[rate_cols[0]]) if rate_cols else '0%'
            estimate_change = parse_estimate_rate(rate_str)

            # 获取估算净值列
            value_cols = [col for col in result_df.columns if '估算值' in col]
            estimate_nav = 0.0
            if value_cols:
                try:
                    estimate_nav = float(row[value_cols[0]])
                except (ValueError, TypeError):
                    estimate_nav = 0.0

            results.append({
                'code': str(row['基金代码']),
                'name': str(row['基金名称']),
                'estimateNav': round(estimate_nav, 4),
                'estimateChange': round(estimate_change, 2)
            })

        logger.info(f"搜索成功，找到 {len(results)} 个基金")

        return jsonify({
            'success': True,
            'data': results,
            'message': f'找到 {len(results)} 个相关基金'
        }), 200

    except Exception as e:
        logger.error(f"搜索时发生错误: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'data': None,
            'message': f'服务器错误: {str(e)}'
        }), 500


@app.route('/api/fund/history/<fund_code>', methods=['GET'])
def get_fund_history(fund_code: str):
    """
    获取基金历史估值数据

    路径参数:
        fund_code: 基金代码（6位数字）

    查询参数:
        days: 获取最近N天的数据（默认7天）

    返回:
        {
            "success": true,
            "data": [
                {
                    "code": "000001",
                    "estimateNav": 1.1806,
                    "estimateChange": 0.65,
                    "estimateTime": "2026-02-01 14:30:00"
                },
                ...
            ],
            "message": "查询成功"
        }
    """
    try:
        logger.info(f"收到历史数据查询请求，基金代码: {fund_code}")

        # 验证基金代码格式
        if not fund_code or len(fund_code) != 6 or not fund_code.isdigit():
            return jsonify({
                'success': False,
                'data': None,
                'message': '基金代码格式错误，请输入6位数字'
            }), 400

        # 检查数据库是否可用
        if not fund_db:
            return jsonify({
                'success': False,
                'data': None,
                'message': '数据库不可用，无法查询历史数据'
            }), 503

        # 获取天数参数
        try:
            days = int(request.args.get('days', 7))
            if days < 1 or days > 30:
                days = 7
        except ValueError:
            days = 7

        # 查询历史数据
        history_data = fund_db.get_history_estimates(fund_code, days)

        if not history_data:
            return jsonify({
                'success': False,
                'data': [],
                'message': f'未找到基金 {fund_code} 的历史数据'
            }), 404

        logger.info(f"查询成功，返回 {len(history_data)} 条历史记录")

        return jsonify({
            'success': True,
            'data': history_data,
            'message': f'查询成功，共 {len(history_data)} 条记录'
        }), 200

    except Exception as e:
        logger.error(f"查询历史数据时发生错误: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'data': None,
            'message': f'服务器错误: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    健康检查接口

    返回:
        {
            "status": "ok",
            "timestamp": "2026-02-01 22:00:00",
            "redis_enabled": true,
            "redis_stats": {...},
            "database_enabled": true
        }
    """
    health_info = {
        'status': 'ok',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'redis_enabled': False,
        'database_enabled': fund_db is not None
    }

    # 检查Redis状态
    if hasattr(fund_api, 'redis_cache') and fund_api.redis_cache:
        health_info['redis_enabled'] = fund_api.redis_cache.enabled
        if fund_api.redis_cache.enabled:
            health_info['redis_stats'] = fund_api.redis_cache.get_stats()

    return jsonify(health_info), 200


@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """
    清空Redis缓存

    请求体:
        {
            "prefix": "fund_estimate"  // 可选，不提供则清空所有基金估值缓存
        }

    返回:
        {
            "success": true,
            "message": "清空缓存成功",
            "count": 10
        }
    """
    try:
        if not hasattr(fund_api, 'redis_cache') or not fund_api.redis_cache or not fund_api.redis_cache.enabled:
            return jsonify({
                'success': False,
                'message': 'Redis缓存未启用'
            }), 503

        data = request.get_json() or {}
        prefix = data.get('prefix', 'fund_estimate')

        count = fund_api.redis_cache.clear_prefix(prefix)

        logger.info(f"清空Redis缓存: {prefix} ({count}个键)")

        return jsonify({
            'success': True,
            'message': f'清空缓存成功',
            'count': count
        }), 200

    except Exception as e:
        logger.error(f"清空缓存失败: {e}")
        return jsonify({
            'success': False,
            'message': f'清空缓存失败: {str(e)}'
        }), 500


@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({
        'success': False,
        'data': None,
        'message': '请求的资源不存在'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'success': False,
        'data': None,
        'message': '服务器内部错误'
    }), 500


if __name__ == '__main__':
    logger.info("=" * 80)
    logger.info("基金估值API服务启动中...")
    logger.info("=" * 80)
    logger.info("API端点:")
    logger.info("  GET  /api/fund/estimate/<fund_code>  - 查询单个基金估值")
    logger.info("  POST /api/fund/estimate/batch        - 批量查询基金估值")
    logger.info("  GET  /api/fund/search?keyword=xxx    - 搜索基金")
    logger.info("  GET  /api/fund/history/<fund_code>   - 查询历史估值数据")
    logger.info("  GET  /api/health                     - 健康检查")
    logger.info("  POST /api/cache/clear                - 清空Redis缓存")
    logger.info("=" * 80)
    logger.info(f"数据库状态: {'✅ 已连接' if fund_db else '❌ 未连接（仅API模式）'}")

    # 显示Redis缓存状态
    if hasattr(fund_api, 'redis_cache') and fund_api.redis_cache and fund_api.redis_cache.enabled:
        logger.info(f"Redis缓存: ✅ 已启用 (TTL: {fund_api.redis_cache.default_ttl}秒)")
    else:
        logger.info(f"Redis缓存: ❌ 未启用")

    logger.info("=" * 80)

    # 启动服务
    app.run(
        host='0.0.0.0',
        port=8083,
        debug=True
    )
