from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class Region(db.Model):
    __tablename__ = 'region'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    lng = db.Column(db.Float, nullable=False)  # 经度
    lat = db.Column(db.Float, nullable=False)  # 纬度
    create_time = db.Column(db.DateTime, default=datetime.now)

    # 关系
    cases = db.relationship('CaseInfo', backref='region', lazy=True)


class CaseInfo(db.Model):
    __tablename__ = 'case_info'

    id = db.Column(db.BigInteger, primary_key=True)
    case_id = db.Column(db.String(50), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age_months = db.Column(db.Integer, nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    test_date = db.Column(db.Date, nullable=False)
    result = db.Column(db.String(20), nullable=False)
    device_id = db.Column(db.String(50), nullable=False)
    details = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)



class Device(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    region = db.Column(db.String(100))
    location = db.Column(db.String(200))
    status = db.Column(db.String(20))  # '在线' 或 '离线'
    version = db.Column(db.String(50))
    total = db.Column(db.Integer, default=0)  # 累计采集数
    today = db.Column(db.Integer, default=0)  # 今日采集数
    last_upload = db.Column(db.DateTime)  # 最后上传时间
    available_versions = db.Column(db.JSON)  # 可用版本列表

class Model(db.Model):
    __tablename__ = 'model'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # 版本名称


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin/doctor
    name = db.Column(db.String(50))  # 真实姓名
    hospital = db.Column(db.String(100))  # 所属医院
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def set_password(self, password):
        """设置密码哈希"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)