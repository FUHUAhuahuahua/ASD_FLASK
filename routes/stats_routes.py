from flask import Blueprint, jsonify
from services.stats_service import StatsService

stats_bp = Blueprint('stats', __name__, url_prefix='/api/stats')

@stats_bp.route('/summary', methods=['GET'])
def get_summary():
    """获取统计摘要"""
    data = StatsService.get_summary_stats()
    return jsonify(data)

@stats_bp.route('/month-trend', methods=['GET'])
def get_month_trend():
    """获取月度趋势"""
    data = StatsService.get_monthly_trend()
    return jsonify(data)

@stats_bp.route('/region-distribution', methods=['GET'])
def get_region_distribution():
    """获取地区分布"""
    data = StatsService.get_region_distribution()
    return jsonify(data)

@stats_bp.route('/positive-rate', methods=['GET'])
def get_positive_rate():
    """获取各地区阳性率"""
    data = StatsService.get_positive_rate_by_region()
    return jsonify(data)