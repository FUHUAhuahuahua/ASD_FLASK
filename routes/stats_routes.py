from flask import Blueprint, jsonify
from services.stats_service import StatsService
# 补充导入必要的模型和数据库对象
from models import db, CaseInfo  # 关键：导入db和CaseInfo
from sqlalchemy import func

stats_bp = Blueprint('stats', __name__, url_prefix='/api/stats')

# 现有路由保持不变...
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

# 新增：实现 /api/stats/detailed 接口
@stats_bp.route('/detailed', methods=['GET'])
def get_detailed_stats():
    """获取详细统计数据（满足前端 loadStatsData 函数需求）"""
    try:
        # 1. 计算平均年龄（使用正确的字段名 age_months）
        avg_age_result = db.session.query(func.avg(CaseInfo.age_months)).first()
        # 修改平均年龄计算部分
        avg_age = round(float(avg_age_result[0]), 1) if avg_age_result[0] is not None else 0.0

        # 2. 统计性别分布
        male_count = CaseInfo.query.filter_by(gender='男').count()
        female_count = CaseInfo.query.filter_by(gender='女').count()

        # 3. 获取月度检测数（复用现有服务方法）
        monthly_trend = StatsService.get_monthly_trend()
        monthly_tests = [item['count'] for item in monthly_trend]

        # 4. 获取地区列表和对应的阳性率（用于图表）
        region_positive_rates = StatsService.get_positive_rate_by_region()
        regions = list(region_positive_rates.keys())  # 以阳性率的地区顺序为准
        positive_rates = list(region_positive_rates.values())

        # 5. 复用摘要统计数据
        summary = StatsService.get_summary_stats()

        # 组装返回数据（匹配前端需要的字段）
        return jsonify({
            'totalTests': summary['totalTests'],
            'positiveCount': summary['positiveCount'],
            'suspectedCount': summary['suspectedCount'],
            'averageAge': avg_age,
            'maleCount': male_count,
            'femaleCount': female_count,
            'monthlyTests': monthly_tests,
            'regions': regions,
            'positiveRates': positive_rates
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500