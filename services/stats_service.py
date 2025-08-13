from models import db, CaseInfo, Region
from sqlalchemy import func
from datetime import datetime


class StatsService:
    @staticmethod
    def get_summary_stats():
        """获取统计摘要信息"""
        total_tests = CaseInfo.query.count()
        positive_count = CaseInfo.query.filter_by(result='阳性').count()
        suspected_count = CaseInfo.query.filter_by(result='疑似').count()  # 新增行
        positive_rate = round((positive_count / total_tests) * 100, 2) if total_tests > 0 else 0

        # 模拟数据上传成功率（实际项目中应根据真实数据计算）
        upload_success_rate = 98.5

        return {
            'totalTests': total_tests,
            'positiveCount': positive_count,
            'suspectedCount': suspected_count,  # 确保这个字段存在
            'positiveRate': positive_rate
        }
    @staticmethod
    def get_monthly_trend():
        """获取月度检测趋势"""
        # 按月份分组统计
        result = db.session.query(
            func.date_format(CaseInfo.test_date, '%m月').label('month'),
            func.count(CaseInfo.id).label('count')
        ).group_by(func.date_format(CaseInfo.test_date, '%Y-%m')).order_by(
            func.date_format(CaseInfo.test_date, '%Y-%m')).all()

        return [{'month': item.month, 'count': item.count} for item in result]

    @staticmethod
    def get_region_distribution():
        """获取各地区检测数量分布"""
        result = db.session.query(
            Region.name,
            func.count(CaseInfo.id).label('count')
        ).join(CaseInfo).group_by(Region.name).all()

        return {item.name: item.count for item in result}

    @staticmethod
    def get_positive_rate_by_region():
        """获取各地区阳性率"""
        # 先获取各地区总检测数
        total_by_region = dict(db.session.query(
            Region.name,
            func.count(CaseInfo.id)
        ).join(CaseInfo).group_by(Region.name).all())

        # 获取各地区阳性数
        positive_by_region = dict(db.session.query(
            Region.name,
            func.count(CaseInfo.id)
        ).join(CaseInfo).filter(CaseInfo.result == '阳性').group_by(Region.name).all())

        # 计算阳性率
        positive_rate = {}
        for region, total in total_by_region.items():
            positive = positive_by_region.get(region, 0)
            positive_rate[region] = round((positive / total) * 100, 2) if total > 0 else 0

        return positive_rate