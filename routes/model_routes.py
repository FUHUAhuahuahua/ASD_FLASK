from flask import Blueprint, jsonify
from models import Model, db
from sqlalchemy.exc import SQLAlchemyError

model_bp = Blueprint('model', __name__, url_prefix='/api/models')

@model_bp.route('', methods=['GET'])
def get_all_models():
    try:
        # 查询所有模型版本并按名称排序
        models = Model.query.order_by(Model.name).all()
        return jsonify([{
            'id': model.id,
            'name': model.name
        } for model in models])
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500