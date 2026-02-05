"""
风险合规部审查模块
"""
import json
import re
from typing import List

from .base import BaseReviewModule, ReviewResult, ReviewFinding
from .rule_engine import ReviewRule


class RiskComplianceReview(BaseReviewModule):
    """风险合规部审查模块"""
    
    department = "risk_compliance"
    department_name = "风险合规部"
    
    def get_review_prompt(self, contract_content: str, rules: List[ReviewRule]) -> str:
        """生成风险合规审查Prompt"""
        rules_info = "\n".join([
            f"- {r.name}: {r.description}" for r in rules
        ])
        
        prompt = f"""
作为风险合规部合同审查专家，请审查以下托管合同的合规相关条款。

## 审查要点
{rules_info}

## 需要重点检查
1. 合同文件名称与签署页一致性
2. 当事人权利义务条款完整性
3. 托管人职责条款
4. 反洗钱相关条款
5. 违约责任条款
6. 引用文件版本检查

## 合同内容
{contract_content[:8000]}

请输出JSON格式的审查结果：
```json
{{
  "product_name": "产品名称",
  "product_type": "产品类型",
  "findings": [
    {{
      "item": "具体审查项目",
      "status": "pass/warning/fail",
      "finding": "具体发现",
      "risk_level": "low/medium/high",
      "recommendation": "改进建议",
      "evidence": "合同原文引用"
    }}
  ]
}}
```
"""
        return prompt
    
    def parse_review_result(self, llm_output: str) -> ReviewResult:
        """解析LLM输出"""
        result = ReviewResult(self.department)
        
        try:
            json_match = re.search(r'```json\s*([\s\S]*?)\s*```', llm_output)
            if not json_match:
                json_match = re.search(r'\{[\s\S]*\}', llm_output)
            
            if json_match:
                data = json.loads(json_match.group(1))
                
                result.product_name = data.get('product_name', '')
                result.product_type = data.get('product_type', '')
                
                for item in data.get('findings', []):
                    finding = ReviewFinding(
                        item=item.get('item', ''),
                        status=item.get('status', 'warning'),
                        finding=item.get('finding', ''),
                        risk_level=item.get('risk_level', 'medium'),
                        recommendation=item.get('recommendation', ''),
                        evidence=item.get('evidence', ''),
                    )
                    result.add_finding(finding)
        
        except Exception as e:
            result.add_finding(ReviewFinding(
                item="结果解析",
                status="warning",
                finding=f"解析错误: {str(e)}",
                risk_level="medium",
            ))
        
        return result
