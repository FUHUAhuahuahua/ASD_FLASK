from flask import Blueprint, jsonify
from models import Device  # 假设存在 Device 模型
from sqlalchemy.exc import SQLAlchemyError

device_bp = Blueprint('device', __name__, url_prefix='/api/devices')

# 获取所有设备列表
@device_bp.route('', methods=['GET'])
def get_devices():
    try:
        devices = Device.query.all()
        # 转换为前端需要的格式
        result = [{
            'id': device.id,
            'region': device.region,
            'location': device.location,
            'status': device.status,
            'version': device.version,
            'total': device.total,
            'today': device.today,
            'lastUpload': device.last_upload
        } for device in devices]
        return jsonify(result)
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

# 获取单个设备详情
@device_bp.route('/<device_id>', methods=['GET'])
def get_device_detail(device_id):
    try:
        device = Device.query.get_or_404(device_id)
        return jsonify({
            'id': device.id,
            'region': device.region,
            'version': device.version,
            'availableVersions': device.available_versions  # 假设存在该字段
        })
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500