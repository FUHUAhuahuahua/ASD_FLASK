from flask import Blueprint, jsonify
from services.case_service import CaseService

case_bp = Blueprint('case', __name__, url_prefix='/api/cases')

@case_bp.route('', methods=['GET'])
def get_all_cases():
    """获取所有个案列表"""
    cases = CaseService.get_all_cases()
    return jsonify(cases)

@case_bp.route('/<case_id>', methods=['GET'])
def get_case_detail(case_id):
    """获取个案详情"""
    case = CaseService.get_case_by_id(case_id)
    if not case:
        return jsonify({'error': '个案不存在'}), 404
    return jsonify(case)