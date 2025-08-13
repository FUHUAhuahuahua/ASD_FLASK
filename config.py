import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI',
                                        'mysql+pymysql://root:thedangerinmyheart@localhost:3306/asd_screening_system')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False  # 保持JSON字段顺序

    # 添加secret key（关键修复）
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-123456')  # 开发环境临时密钥，生产环境必须更换