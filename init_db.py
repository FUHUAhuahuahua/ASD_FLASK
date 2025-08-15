from app import create_app
from models import db, CaseInfo, Region, Model  # 新增 Model 导入
from datetime import datetime, timedelta
import random

# 创建应用并获取上下文
app = create_app()
with app.app_context():
      # 初始化模型版本数据
    versions = ["v0.11", "v0.12", "v0.13", "v0.14"]
    for version in versions:
        existing = Model.query.filter_by(name=version).first()
        if not existing:
            model = Model(name=version)
            db.session.add(model)
            print(f"模型版本创建: {version}")
    
    # 提交所有数据
    db.session.commit()
    print("所有数据创建完成")