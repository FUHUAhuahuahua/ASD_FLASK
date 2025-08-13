from models import db, CaseInfo, Region
from sqlalchemy import func


class CaseService:
    @staticmethod
    def get_all_cases():
        """获取所有个案信息"""
        cases = CaseInfo.query.join(Region).all()
        return [
            {
                'caseId': case.case_id,
                'gender': case.gender,
                'ageMonths': case.age_months,
                'regionName': case.region.name,
                'testDate': case.test_date.strftime('%Y-%m-%d'),
                'result': case.result
            }
            for case in cases
        ]

    @staticmethod
    def get_case_by_id(case_id):
        """通过个案ID获取个案详情"""
        case = CaseInfo.query.filter_by(case_id=case_id).join(Region).first()
        if not case:
            return None
        return {
            'caseId': case.case_id,
            'gender': case.gender,
            'ageMonths': case.age_months,
            'regionName': case.region.name,
            'testDate': case.test_date.strftime('%Y-%m-%d'),
            'result': case.result,
            'details': case.details or ''
        }