from app import create_app
from models import db, User

# 创建应用并获取上下文
app = create_app()
with app.app_context():
    # 先检查用户是否已存在（避免重复创建）
    existing_test = User.query.filter_by(username="test").first()
    if not existing_test:
        # 创建测试用户（原代码保留）
        user = User(username="test")
        user.set_password("123456")  # 加密密码
        user.role = "admin"  # 设置角色
        user.name = "测试管理员"

        db.session.add(user)
        print("测试用户创建成功：用户名=test，密码=123456")


    # 创建管理员用户
    existing_admin = User.query.filter_by(username="admin").first()
    if not existing_admin:
        admin = User(username="admin")
        admin.set_password("123456")  # 管理员密码
        admin.role = "admin"
        admin.name = "系统管理员"
        admin.hospital = "系统管理中心"  # 管理员所属机构z
        db.session.add(admin)
        print("管理员创建成功：用户名=admin，密码=123456")


    # 创建医生用户1
    existing_doctor1 = User.query.filter_by(username="doctor_zhang").first()
    if not existing_doctor1:
        doctor1 = User(username="doctor_zhang")
        doctor1.set_password("123456")  # 医生密码
        doctor1.role = "doctor"
        doctor1.name = "张医生"
        doctor1.hospital = "拉萨市第一人民医院"

        db.session.add(doctor1)
        print("医生创建成功：用户名=doctor_zhang，密码=123456")


    # 创建医生用户2
    existing_doctor2 = User.query.filter_by(username="doctor_li").first()
    if not existing_doctor2:
        doctor2 = User(username="doctor_li")
        doctor2.set_password("Li@123")  # 医生密码
        doctor2.role = "doctor"
        doctor2.name = "李医生"
        doctor2.hospital = "日喀则市人民医院"

        db.session.add(doctor2)
        print("医生创建成功：用户名=doctor_li，密码=Li@123")


    # 提交所有用户到数据库
    db.session.commit()