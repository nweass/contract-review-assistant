"""
投资监督部审查模块
"""
import json
import re
from typing import List

from .base import BaseReviewModule, ReviewResult, ReviewFinding
from .rule_engine import ReviewRule


class InvestmentSupervisionReview(BaseReviewModule):
    """投资监督部审查模块"""
    
    department = "investment_supervision"
    department_name = "投资监督部"
    
    def get_review_prompt(self, contract_content: str, rules: List[ReviewRule]) -> str:
        """生成投资监督审查Prompt"""
        rules_info = "\n".join([
            f"- {r.name}: {r.description}" for r in rules
        ])
        
        prompt = f"""
作为投资监督部合同审查专家，请审查以下托管合同的投资相关条款。

## 审查要点
{rules_info}

## 合同内容
{contract_content[:8000]}  # 限制长度

## 需要重点检查
1. 投资范围是否明确
2. 投资比例是否符合监管限制
3. 投资限制条款是否完整
4. 是否存在违规投资风险

请输出JSON格式的审查结果：
```json
{{
  "product_name": "产品名称（从合同中提取）",
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
            # 提取JSON
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
            else:
                # 未能解析JSON，添加错误信息
                result.add_finding(ReviewFinding(
                    item="结果解析",
                    status="warning",
                    finding="未能解析LLM输出，请人工检查",
                    risk_level="medium",
                    recommendation="联系技术支持",
                ))
        
        except json.JSONDecodeError as e:
            result.add_finding(ReviewFinding(
                item="JSON解析",
                status="fail",
                finding=f"JSON解析错误: {str(e)}",
                risk_level="high",
                recommendation="检查LLM输出格式",
            ))
        
        return result
