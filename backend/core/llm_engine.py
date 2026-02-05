"""
LLM引擎 - 统一的大语言模型接口
"""
import os
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from loguru import logger

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate

from .config import get_settings


class LLMBase(ABC):
    """LLM抽象基类"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        pass
    
    @abstractmethod
    def embed(self, text: str) -> List[float]:
        pass


class OpenAILLM(LLMBase):
    """OpenAI LLM实现"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        settings = get_settings()
        
        self.api_key = api_key or settings.llm.api_key
        self.model = model or settings.llm.model
        self.temperature = settings.llm.temperature
        
        # 初始化LLM
        self.llm = ChatOpenAI(
            api_key=self.api_key,
            model=self.model,
            temperature=self.temperature
        )
        
        # 初始化Embedding
        self.embeddings = OpenAIEmbeddings(
            api_key=self.api_key,
            model="text-embedding-3-small"
        )
        logger.info(f"Initialized OpenAI LLM with model: {self.model}")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """生成文本"""
        messages = []
        
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        
        messages.append(HumanMessage(content=prompt))
        
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise
    
    def embed(self, text: str) -> List[float]:
        """生成嵌入向量"""
        try:
            return self.embeddings.embed_query(text)
        except Exception as e:
            logger.error(f"Embedding failed: {e}")
            raise


class LLMFactory:
    """LLM工厂类"""
    
    _instances: Dict[str, LLMBase] = {}
    
    @classmethod
    def get_llm(cls, provider: Optional[str] = None) -> LLMBase:
        """获取LLM实例"""
        settings = get_settings()
        provider = provider or settings.llm.provider
        
        if provider not in cls._instances:
            if provider == "openai":
                cls._instances[provider] = OpenAILLM()
            else:
                raise ValueError(f"Unsupported LLM provider: {provider}")
        
        return cls._instances[provider]
    
    @classmethod
    def reset(cls):
        """重置实例"""
        cls._instances.clear()


def get_llm() -> LLMBase:
    """获取默认LLM实例"""
    return LLMFactory.get_llm()


# 常用Prompt模板
REVIEW_PROMPT_TEMPLATE = """
你是一位专业的托管合同审查专家。请根据以下要求审查合同：

## 审查部门
{department}

## 审查要点
{review_points}

## 合同内容
{contract_content}

## 输出要求
1. 逐条分析每个审查要点
2. 标注是否符合要求（符合/不符合/未提及）
3. 识别潜在风险点
4. 用JSON格式输出结果

## JSON输出格式
```json
{{
  "findings": [
    {{
      "item": "审查项目名称",
      "status": "pass/warning/fail",
      "finding": "具体发现",
      "risk_level": "low/medium/high",
      "recommendation": "改进建议"
    }}
  ],
  "summary": "总体审查结论"
}}
```
"""
