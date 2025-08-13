from flask import Blueprint, request, jsonify, render_template
from flask_login import login_user, logout_user, login_required, current_user
from services.user_service import UserService

user_bp = Blueprint('user', __name__, url_prefix='/api/user')


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录接口"""
    if request.method == 'GET':
        # 显示登录页面
        return render_template('login.html')

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400

    user = UserService.verify_user(username, password)
    if not user:
        return jsonify({'error': '用户名或密码错误'}), 401

    # 登录用户
    login_user(user)
    return jsonify({
        'success': True,
        'message': '登录成功',
        'user': UserService.get_user_info(user.id)
    })


@user_bp.route('/logout', methods=['POST'])


def logout():
    logout_user()
    return jsonify({'success': True, 'message': '登出成功'})


@user_bp.route('/info', methods=['GET'])
@login_required
def get_user_info():
    """获取当前登录用户信息"""
    return jsonify(UserService.get_user_info(current_user.id))
