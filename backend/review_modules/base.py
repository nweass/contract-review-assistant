"""
审查模块基类
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime

from .llm_engine import get_llm, REVIEW_PROMPT_TEMPLATE
from .rule_engine import get_rule_engine, ReviewRule


class ReviewFinding:
    """审查发现"""
    
    def __init__(
        self,
        item: str,
        status: str,  # pass, warning, fail
        finding: str,
        risk_level: str = "medium",  # low, medium, high
        recommendation: str = "",
        evidence: str = "",
    ):
        self.item = item
        self.status = status
        self.finding = finding
        self.risk_level = risk_level
        self.recommendation = recommendation
        self.evidence = evidence
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        return {
            "item": self.item,
            "status": self.status,
            "finding": self.finding,
            "risk_level": self.risk_level,
            "recommendation": self.recommendation,
            "evidence": self.evidence,
            "timestamp": self.timestamp,
        }


class ReviewResult:
    """审查结果"""
    
    def __init__(
        self,
        department: str,
        product_name: str = "",
        product_type: str = "",
    ):
        self.department = department
        self.product_name = product_name
        self.product_type = product_type
        self.findings: List[ReviewFinding] = []
        self.summary = {
            "total": 0,
            "passed": 0,
            "warnings": 0,
            "errors": 0,
        }
        self.metadata = {
            "review_time": datetime.now().isoformat(),
            "model": "",
            "version": "1.0.0",
        }
    
    def add_finding(self, finding: ReviewFinding):
        self.findings.append(finding)
        self._update_summary()
    
    def _update_summary(self):
        """更新统计"""
        self.summary["total"] = len(self.findings)
        self.summary["passed"] = sum(1 for f in self.findings if f.status == "pass")
        self.summary["warnings"] = sum(1 for f in self.findings if f.status == "warning")
        self.summary["errors"] = sum(1 for f in self.findings if f.status == "fail")
    
    def to_dict(self) -> dict:
        return {
            "department": self.department,
            "product_name": self.product_name,
            "product_type": self.product_type,
            "findings": [f.to_dict() for f in self.findings],
            "summary": self.summary,
            "metadata": self.metadata,
        }


class BaseReviewModule(ABC):
    """审查模块基类"""
    
    department: str = "base"
    department_name: str = "基础审查"
    
    def __init__(self):
        self.llm = get_llm()
        self.rule_engine = get_rule_engine()
    
    @abstractmethod
    def get_review_prompt(self, contract_content: str, rules: List[ReviewRule]) -> str:
        """获取审查Prompt"""
        pass
    
    @abstractmethod
    def parse_review_result(self, llm_output: str) -> ReviewResult:
        """解析LLM输出为审查结果"""
        pass
    
    def review(
        self,
        contract_content: str,
        product_name: str = "",
        product_type: str = "",
        **kwargs
    ) -> ReviewResult:
        """执行审查"""
        result = ReviewResult(self.department, product_name, product_type)
        
        # 获取规则
        rules = self.rule_engine.get_enabled_rules(self.department)
        
        if not rules:
            # 无规则时使用默认审查
            result.add_finding(ReviewFinding(
                item="通用审查",
                status="warning",
                finding="未找到该部门的审查规则，已执行基础审查",
                risk_level="low",
            ))
            return self._basic_review(contract_content, result)
        
        # 构建Prompt
        review_prompt = self.get_review_prompt(contract_content, rules)
        
        # 调用LLM
        try:
            llm_output = self.llm.generate(
                prompt=review_prompt,
                system_prompt="你是一位专业的托管合同审查专家，请严格按照JSON格式输出审查结果。",
            )
            
            # 解析结果
            result = self.parse_review_result(llm_output)
            result.metadata["model"] = self.llm.model
            
        except Exception as e:
            result.add_finding(ReviewFinding(
                item="审查执行",
                status="fail",
                finding=f"审查过程出错: {str(e)}",
                risk_level="high",
                recommendation="请检查系统配置或稍后重试",
            ))
        
        return result
    
    def _basic_review(self, contract_content: str, result: ReviewResult) -> ReviewResult:
        """基础审查（无规则时）"""
        # 简单的关键词检查
        keywords = ["投资", "托管", "风险", "费用"]
        
        for keyword in keywords:
            if keyword in contract_content:
                result.add_finding(ReviewFinding(
                    item=f"关键词'{keyword}'检查",
                    status="pass",
                    finding=f"合同中包含'{keyword}'相关内容",
                    risk_level="low",
                ))
            else:
                result.add_finding(ReviewFinding(
                    item=f"关键词'{keyword}'检查",
                    status="warning",
                    finding=f"合同中未找到'{keyword}'相关内容",
                    risk_level="medium",
                ))
        
        return result
