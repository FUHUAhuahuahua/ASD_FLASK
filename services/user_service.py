from models import db, User
from datetime import datetime


class UserService:
    @staticmethod
    def get_user_by_username(username):
        """通过用户名获取用户"""
        return User.query.filter_by(username=username).first()

    @staticmethod
    def verify_user(username, password):
        """验证用户登录"""
        user = UserService.get_user_by_username(username)
        if user and user.is_active and user.check_password(password):
            # 更新最后登录时间
            user.last_login_time = datetime.now()
            db.session.commit()
            return user
        return None

    @staticmethod
    def get_user_info(user_id):
        """获取用户信息（不含敏感数据）"""
        user = User.query.get(user_id)
        if not user:
            return None
        return {
            'id': user.id,
            'username': user.username,
            'name': user.name or user.username,
            'role': user.role,
            'hospital': user.hospital or '',
            'lastLoginTime': user.last_login_time.strftime('%Y-%m-%d %H:%M:%S') if user.last_login_time else None
        }