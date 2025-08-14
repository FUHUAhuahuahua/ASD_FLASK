from app import create_app
from models import db, CaseInfo, Region
from datetime import datetime, timedelta
import random

# 创建应用并获取上下文
app = create_app()
with app.app_context():
    # 确保成都和贵阳地区存在
    chengdu = Region.query.filter_by(name="成都").first()
    if not chengdu:
        chengdu = Region(
            name="成都",
            lng=104.0665,  # 成都经度
            lat=30.5723    # 成都纬度
        )
        db.session.add(chengdu)
        print("地区创建成功：成都")
    
    guiyang = Region.query.filter_by(name="贵阳").first()
    if not guiyang:
        guiyang = Region(
            name="贵阳",
            lng=106.7134,  # 贵阳经度
            lat=26.5784    # 贵阳纬度
        )
        db.session.add(guiyang)
        print("地区创建成功：贵阳")
    
    # 生成拼音姓名的辅助函数
    def generate_pinyin_name():
        surnames = ["Zhang", "Wang", "Li", "Zhao", "Liu", "Chen", "Yang", "Huang", "Zhou", "Wu"]
        first_names = ["Wei", "Jie", "Ming", "Jun", "Hong", "Tao", "Bin", "Chao", "Lei", "Yang"]
        return f"{random.choice(surnames)} {random.choice(first_names)}"
    
    # 生成随机日期的辅助函数
    def random_date(start, end):
        delta = end - start
        days = random.randint(0, delta.days)
        return start + timedelta(days=days)
    
    # 基础Case ID
    base_case_id = "08141013"
    operation = "模型更新ASD_v0.13"
    
    # 成都案例日期范围（7月1日-8月12日）
    chengdu_start = datetime(2023, 7, 1)
    chengdu_end = datetime(2023, 8, 12)
    
    # 生成20个成都案例
    for i in range(20):
        case_id = f"{base_case_id}_{i+1:03d}"  # 格式：08141013_001 到 08141013_020
        existing_case = CaseInfo.query.filter_by(case_id=case_id).first()
        
        if not existing_case:
            name = generate_pinyin_name()
            age = random.randint(6, 24)
            test_date = random_date(chengdu_start, chengdu_end)
            probability = random.randint(5, 95)  # 5%-95%的概率范围
            result = f"{probability}% 概率患有ASD"
            
            case = CaseInfo(
                case_id=case_id,
                gender="男",
                age_months=age,
                region_id=chengdu.id,
                test_date=test_date,
                result=result,
                device_id="DEVICE_ASD_001",  # 假设设备ID
                details=f"姓名: {name}; 操作: {operation}"
            )
            
            db.session.add(case)
            print(f"成都案例创建成功：case_id={case_id}, 姓名={name}, 年龄={age}月")
    
    # 贵阳案例日期范围（8月13日-8月14日）
    guiyang_start = datetime(2023, 8, 13)
    guiyang_end = datetime(2023, 8, 14)
    
    # 生成2个贵阳案例
    for i in range(20, 22):  # 续接编号：021-022
        case_id = f"{base_case_id}_{i+1:03d}"  # 格式：08141013_021 到 08141013_022
        existing_case = CaseInfo.query.filter_by(case_id=case_id).first()
        
        if not existing_case:
            name = generate_pinyin_name()
            age = random.randint(6, 24)
            test_date = random_date(guiyang_start, guiyang_end)
            probability = random.randint(5, 95)
            result = f"{probability}% 概率患有ASD"
            
            case = CaseInfo(
                case_id=case_id,
                gender="男",
                age_months=age,
                region_id=guiyang.id,
                test_date=test_date,
                result=result,
                device_id="DEVICE_ASD_002",  # 假设设备ID
                details=f"姓名: {name}; 操作: {operation}"
            )
            
            db.session.add(case)
            print(f"贵阳案例创建成功：case_id={case_id}, 姓名={name}, 年龄={age}月")
    
    # 提交所有数据
    db.session.commit()
    print("所有案例数据创建完成")