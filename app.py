from flask import Flask, render_template, redirect, url_for, request, jsonify  # 补充导入 request 和 jsonify
from flask_cors import CORS
from flask_login import LoginManager, login_required, current_user
from config import Config
from models import db
from routes.case_routes import case_bp
from routes.stats_routes import stats_bp
from routes.map_routes import map_bp
from routes.user_routes import user_bp
from routes.device_routes import device_bp
from routes.rag_routes import rag_bp

login_manager = LoginManager()
login_manager.login_view = 'user.login'  # 登录视图


@login_manager.user_loader
def load_user(user_id):
    """加载用户回调函数"""
    from models import User
    return db.session.get(User, int(user_id))



# 全局登录验证装饰器
def login_required_decorator(app):
    @app.before_request
    def check_login():
        # 排除登录相关路径、API登录接口、静态文件
        excluded_paths = [
            '/api/user/login',
            '/login',  # 新增：确保登录页面本身不被拦截
            '/static'
        ]
        # 检查当前路径是否需要排除
        if any(request.path.startswith(path) for path in excluded_paths):
            return None
        # 未登录处理
        if not current_user.is_authenticated:
            if request.path.startswith('/api/'):
                return jsonify({'error': '请先登录'}), 401
            else:
                return redirect(url_for('user.login'))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化扩展
    db.init_app(app)
    CORS(app)
    login_manager.init_app(app)  # 初始化登录管理器

    # 注册蓝图（新增用户蓝图）
    app.register_blueprint(case_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(map_bp)
    app.register_blueprint(device_bp)
    app.register_blueprint(rag_bp)
    app.register_blueprint(user_bp)  # 注册用户路由

    # 添加根路由
    @app.route('/')
    @login_required
    def index():
        return render_template('head.html')

    # 创建数据库表
    with app.app_context():
        db.create_all()

    # 应用登录验证
    from flask import request, jsonify
    login_required_decorator(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)  # 添加host和port参数