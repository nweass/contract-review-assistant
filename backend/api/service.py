"""
审查服务 - 统一的审查入口
"""
from typing import List, Dict, Optional, Union
from pathlib import Path

from .core.document_parser import DocumentParserFactory
from .core.rule_engine import get_rule_engine
from .review_modules.investment import InvestmentSupervisionReview
from .review_modules.compliance import RiskComplianceReview
from .review_modules.valuation import ValuationServiceReview
from .review_modules.settlement import SettlementServiceReview


class ReviewService:
    """审查服务"""
    
    # 支持的部门映射
    DEPARTMENTS = {
        "investment_supervision": InvestmentSupervisionReview,
        "risk_compliance": RiskComplianceReview,
        "valuation_service": ValuationServiceReview,
        "settlement_service": SettlementServiceReview,
    }
    
    DEPARTMENT_NAMES = {
        "investment_supervision": "投资监督部",
        "risk_compliance": "风险合规部",
        "valuation_service": "估值服务部",
        "settlement_service": "结算服务部",
    }
    
    def __init__(self):
        self.rule_engine = get_rule_engine()
        self._modules = {}
    
    def _get_module(self, department: str):
        """获取审查模块"""
        if department not in self._modules:
            if department in self.DEPARTMENTS:
                self._modules[department] = self.DEPARTMENTS[department]()
            else:
                raise ValueError(f"Unknown department: {department}")
        return self._modules[department]
    
    def list_departments(self) -> List[Dict]:
        """列出所有支持的部门"""
        return [
            {
                "id": dept_id,
                "name": name,
                "enabled": bool(self.rule_engine.get_rules(dept_id)),
            }
            for dept_id, name in self.DEPARTMENT_NAMES.items()
        ]
    
    def review(
        self,
        file_path: Optional[str] = None,
        content: Optional[str] = None,
        department: str = "investment_supervision",
        product_name: str = "",
        product_type: str = "",
    ) -> Dict:
        """审查合同"""
        # 获取合同内容
        if content is None and file_path:
            content = DocumentParserFactory.parse_document(file_path)
        elif not content:
            raise ValueError("Must provide file_path or content")
        
        # 获取审查模块
        module = self._get_module(department)
        
        # 执行审查
        result = module.review(
            contract_content=content,
            product_name=product_name,
            product_type=product_type,
        )
        
        return result.to_dict()
    
    def batch_review(
        self,
        file_paths: List[str],
        department: str = "investment_supervision",
    ) -> List[Dict]:
        """批量审查"""
        results = []
        for file_path in file_paths:
            try:
                result = self.review(
                    file_path=file_path,
                    department=department,
                )
                result["file_path"] = file_path
                results.append(result)
            except Exception as e:
                results.append({
                    "file_path": file_path,
                    "error": str(e),
                    "status": "failed",
                })
        return results
    
    def review_all_departments(
        self,
        file_path: Optional[str] = None,
        content: Optional[str] = None,
    ) -> Dict[str, Dict]:
        """全部门审查"""
        results = {}
        
        for dept_id in self.DEPARTMENTS.keys():
            try:
                result = self.review(
                    file_path=file_path,
                    content=content,
                    department=dept_id,
                )
                results[dept_id] = {
                    "department_name": self.DEPARTMENT_NAMES[dept_id],
                    "result": result,
                }
            except Exception as e:
                results[dept_id] = {
                    "department_name": self.DEPARTMENT_NAMES[dept_id],
                    "error": str(e),
                }
        
        return results
    
    def get_rules(self, department: str) -> List[Dict]:
        """获取审查规则"""
        rules = self.rule_engine.get_rules(department)
        return [r.to_dict() for r in rules]
    
    def update_rule(
        self,
        department: str,
        rule_id: str,
        updates: Dict,
    ) -> Dict:
        """更新规则"""
        success = self.rule_engine.update_rule(department, rule_id, updates)
        return {
            "success": success,
            "department": department,
            "rule_id": rule_id,
        }
    
    def toggle_rule(
        self,
        department: str,
        rule_id: str,
        enabled: bool,
    ) -> Dict:
        """启用/禁用规则"""
        success = self.rule_engine.toggle_rule(department, rule_id, enabled)
        return {
            "success": success,
            "department": department,
            "rule_id": rule_id,
            "enabled": enabled,
        }


# 全局服务实例
_review_service: Optional[ReviewService] = None


def get_review_service() -> ReviewService:
    """获取审查服务实例"""
    global _review_service
    if _review_service is None:
        _review_service = ReviewService()
    return _review_service
