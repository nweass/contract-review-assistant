"""
合同审查助手 - 配置管理模块
"""
import os
from pathlib import Path
from functools import lru_cache
from typing import Optional

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class LLMSettings(BaseModel):
    """LLM配置"""
    provider: str = "openai"
    api_key: str = ""
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4"
    temperature: float = 0.1


class AppSettings(BaseModel):
    """应用配置"""
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "INFO"
    max_file_size: int = 50
    allowed_extensions: list = ["pdf", "docx", "doc", "txt"]
    rules_path: str = "./rules"
    knowledge_base_path: str = "./knowledge_base"
    default_department: str = "investment_supervision"
    cors_origins: list = ["http://localhost:5173", "http://localhost:3000"]


class Settings(BaseSettings):
    """全局设置"""
    llm: LLMSettings = Field(default_factory=LLMSettings)
    app: AppSettings = Field(default_factory=AppSettings)
    
    class Config:
        env_prefix = "CONTRACT_REVIEW_"
        env_nested_delimiter = "__"


@lru_cache()
def get_settings() -> Settings:
    """获取全局配置（单例模式）"""
    return Settings()


class ConfigLoader:
    """配置加载器"""
    
    @staticmethod
    def load_yaml(file_path: str) -> dict:
        """加载YAML配置文件"""
        path = Path(file_path)
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return {}
    
    @staticmethod
    def save_yaml(file_path: str, data: dict) -> bool:
        """保存YAML配置文件"""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)
        return True
