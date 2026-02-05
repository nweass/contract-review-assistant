"""
审查规则引擎 - 可配置的规则管理
"""
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

import yaml
from loguru import logger

from .config import ConfigLoader


class ReviewRule:
    """审查规则类"""
    
    def __init__(self, rule_data: dict):
        self.id = rule_data.get('id', '')
        self.name = rule_data.get('name', '')
        self.description = rule_data.get('description', '')
        self.enabled = rule_data.get('enabled', True)
        self.keywords = rule_data.get('keywords', [])
        self.check_items = rule_data.get('check_items', [])
        self.threshold = rule_data.get('threshold', 0.8)
        self.risk_level = rule_data.get('risk_level', 'medium')
        self.recommendation = rule_data.get('recommendation', '')
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'enabled': self.enabled,
            'keywords': self.keywords,
            'check_items': self.check_items,
            'threshold': self.threshold,
            'risk_level': self.risk_level,
            'recommendation': self.recommendation,
        }


class RuleEngine:
    """规则引擎"""
    
    def __init__(self, rules_path: Optional[str] = None):
        settings = get_settings()
        self.rules_path = rules_path or settings.app.rules_path
        self._rules: Dict[str, List[ReviewRule]] = {}
        self._load_all_rules()
    
    def _load_all_rules(self):
        """加载所有规则文件"""
        rules_dir = Path(self.rules_path)
        
        if not rules_dir.exists():
            logger.warning(f"Rules directory not found: {self.rules_path}")
            # 创建默认规则文件
            self._create_default_rules()
            return
        
        for rule_file in rules_dir.glob("*.yaml"):
            try:
                rules_data = ConfigLoader.load_yaml(str(rule_file))
                department = rules_data.get('department', 'general')
                rules = [ReviewRule(r) for r in rules_data.get('rules', [])]
                self._rules[department] = rules
                logger.info(f"Loaded {len(rules)} rules for {department}")
            except Exception as e:
                logger.error(f"Failed to load rules from {rule_file}: {e}")
    
    def _create_default_rules(self):
        """创建默认规则"""
        default_rules = {
            'investment_supervision': [
                {
                    'id': 'INV001',
                    'name': '投资范围审查',
                    'description': '检查投资范围是否符合监管要求',
                    'enabled': True,
                    'keywords': ['投资范围', '投资标的', '投资品种'],
                    'risk_level': 'high',
                    'recommendation': '建议明确投资范围的具体标的和比例限制',
                },
                {
                    'id': 'INV002',
                    'name': '投资比例限制',
                    'description': '验证投资比例是否在监管限制范围内',
                    'enabled': True,
                    'keywords': ['投资比例', '单一股票', '单一发行人'],
                    'check_items': ['单一股票投资比例', '单一发行人债券比例'],
                    'risk_level': 'high',
                    'recommendation': '确保各投资比例符合最新监管规定',
                },
            ],
            'risk_compliance': [
                {
                    'id': 'RC001',
                    'name': '合同文件一致性',
                    'description': '检查正文列示文件名与签署页是否一致',
                    'enabled': True,
                    'keywords': ['文件名称', '签署页', '附件'],
                    'risk_level': 'medium',
                    'recommendation': '核对正文和签署页的文件名称是否完全一致',
                },
                {
                    'id': 'RC002',
                    'name': '托管人职责审查',
                    'description': '审查托管人职责条款完整性',
                    'enabled': True,
                    'keywords': ['托管人职责', '保管职责', '监督职责'],
                    'risk_level': 'high',
                    'recommendation': '确保职责条款覆盖所有必要的托管职能',
                },
            ],
            'valuation_service': [
                {
                    'id': 'VS001',
                    'name': '估值核算方法',
                    'description': '审查估值核算方法及频率',
                    'enabled': True,
                    'keywords': ['估值方法', '核算方法', '估值频率'],
                    'risk_level': 'medium',
                    'recommendation': '明确估值方法和频率，确保符合监管要求',
                },
            ],
            'settlement_service': [
                {
                    'id': 'SS001',
                    'name': '清算交收方式',
                    'description': '审查清算交收方式与频率',
                    'enabled': True,
                    'keywords': ['清算', '交收', '交割'],
                    'risk_level': 'medium',
                    'recommendation': '明确清算交收的具体流程和时间要求',
                },
            ],
        }
        
        for dept, rules in default_rules.items():
            rule_file = Path(self.rules_path) / f"{dept}_rules.yaml"
            rule_file.parent.mkdir(parents=True, exist_ok=True)
            
            config_data = {
                'department': dept,
                'version': '1.0.0',
                'updated_at': datetime.now().isoformat(),
                'rules': rules,
            }
            
            ConfigLoader.save_yaml(str(rule_file), config_data)
            self._rules[dept] = [ReviewRule(r) for r in rules]
            logger.info(f"Created default rules for {dept}")
    
    def get_rules(self, department: str) -> List[ReviewRule]:
        """获取指定部门的规则"""
        return self._rules.get(department, [])
    
    def get_enabled_rules(self, department: str) -> List[ReviewRule]:
        """获取指定部门已启用的规则"""
        return [r for r in self._rules.get(department, []) if r.enabled]
    
    def update_rule(self, department: str, rule_id: str, updates: dict) -> bool:
        """更新规则"""
        rules = self._rules.get(department, [])
        
        for rule in rules:
            if rule.id == rule_id:
                for key, value in updates.items():
                    if hasattr(rule, key):
                        setattr(rule, key, value)
                
                # 更新规则文件
                self._save_rules_to_file(department)
                logger.info(f"Updated rule {rule_id} for {department}")
                return True
        
        return False
    
    def toggle_rule(self, department: str, rule_id: str, enabled: bool) -> bool:
        """启用/禁用规则"""
        return self.update_rule(department, rule_id, {'enabled': enabled})
    
    def add_rule(self, department: str, rule_data: dict) -> bool:
        """添加新规则"""
        if department not in self._rules:
            self._rules[department] = []
        
        rule = ReviewRule(rule_data)
        self._rules[department].append(rule)
        self._save_rules_to_file(department)
        logger.info(f"Added new rule {rule.id} for {department}")
        return True
    
    def _save_rules_to_file(self, department: str):
        """保存规则到文件"""
        rules = self._rules.get(department, [])
        rule_file = Path(self.rules_path) / f"{department}_rules.yaml"
        
        config_data = {
            'department': department,
            'version': '1.0.0',
            'updated_at': datetime.now().isoformat(),
            'rules': [r.to_dict() for r in rules],
        }
        
        ConfigLoader.save_yaml(str(rule_file), config_data)
    
    def list_departments(self) -> List[str]:
        """列出所有部门"""
        return list(self._rules.keys())


# 全局规则引擎实例
_rule_engine: Optional[RuleEngine] = None


def get_rule_engine(rules_path: Optional[str] = None) -> RuleEngine:
    """获取规则引擎实例"""
    global _rule_engine
    if _rule_engine is None:
        _rule_engine = RuleEngine(rules_path)
    return _rule_engine
