from models import db, CaseInfo, Region
from sqlalchemy import func
from datetime import datetime
import re 



class StatsService:
    @staticmethod
    def get_summary_stats():
        """获取统计摘要信息（修改版）"""
        # 1. 查询所有个案的result字段
        all_results = CaseInfo.query.with_entities(CaseInfo.result).all()
        
        # 2. 初始化计数器
        total_tests = len(all_results)
        positive_count = 0  # >80%
        suspected_count = 0  # 40%-80%
        negative_count = 0   # <40%
        
        # 3. 正则表达式：提取result中的数字（支持整数和小数）
        pattern = re.compile(r'(\d+\.?\d*)%')
        
        # 4. 遍历结果并分类计数
        for result in all_results:
            result_str = result[0]  # result是元组，取第一个元素
            match = pattern.search(result_str)
            if match:
                try:
                    percentage = float(match.group(1))  # 提取数字并转为浮点数
                    if percentage > 80:
                        positive_count += 1
                    elif 40 <= percentage <= 80:
                        suspected_count += 1
                    else:
                        negative_count += 1
                except ValueError:
                    # 处理数字转换失败的异常（如格式错误）
                    continue
        
        # 5. 计算阳性率（仅基于有效分类的数据）
        valid_count = positive_count + suspected_count + negative_count
        positive_rate = round((positive_count / valid_count) * 100, 2) if valid_count > 0 else 0

        return {
            'totalTests': total_tests,
            'positiveCount': positive_count,  # 阳性（>80%）
            'suspectedCount': suspected_count,  # 疑似（40%-80%）
            'negativeCount': negative_count,    # 新增：阴性（<40%）
            'positiveRate': positive_rate
        }
    @staticmethod
    def get_monthly_trend():
        """获取月度检测趋势"""
        # 按年-月分组统计（确保SELECT和GROUP BY使用相同格式）
        result = db.session.query(
            func.date_format(CaseInfo.test_date, '%Y-%m').label('year_month'),  # 统一格式
            func.count(CaseInfo.id).label('count')
        ).group_by(func.date_format(CaseInfo.test_date, '%Y-%m')).order_by(
            func.date_format(CaseInfo.test_date, '%Y-%m')).all()

    # 转换为前端需要的"XX月"格式
        return [
            {'month': item.year_month.split('-')[1] + '月', 'count': item.count} 
            for item in result
        ]
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