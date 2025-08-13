from flask import Blueprint, jsonify
from models import Region, CaseInfo
from sqlalchemy import func
from services.stats_service import StatsService

map_bp = Blueprint('map', __name__, url_prefix='/api/map')


@map_bp.route('/data', methods=['GET'])
def get_map_data():
    """获取地图所需数据"""
    # 获取各地区的经纬度
    regions = Region.query.all()

    # 获取各地区检测数和阳性数
    total_by_region = StatsService.get_region_distribution()
    positive_by_region = dict(CaseInfo.query.join(Region)
                              .filter(CaseInfo.result == '阳性')
                              .group_by(Region.name)
                              .with_entities(Region.name, func.count(CaseInfo.id))
                              .all())

    # 构建地图数据
    map_data = []
    for region in regions:
        count = total_by_region.get(region.name, 0)
        positive = positive_by_region.get(region.name, 0)
        positive_rate = round((positive / count) * 100, 2) if count > 0 else 0

        map_data.append({
            'name': region.name,
            'lnglat': [region.lng, region.lat],
            'count': count,
            'positive': positive,
            'positiveRate': positive_rate
        })

    return jsonify(map_data)