# 托管业务AI合同审查助手
# Contract Review Assistant for Custody Business

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

**基于大语言模型的托管合同智能审查系统**

[功能特性](#-功能特性) • [快速开始](#-快速开始) • [API文档](#-api文档) • [前端演示](#-前端演示)

</div>

---

## 📋 项目概述

本项目是一个**托管合同智能审查系统**，通过AI技术实现公募基金和年金合同的自动化要素提取与多维度风险审查，支持4个托管二级部的差异化审查需求。

### 🎯 核心功能

| 模块 | 审查内容 |
|------|----------|
| **投资监督部** | 投资范围、投资比例、投资限制合规性 |
| **风险合规部** | 权利义务、托管人职责、反洗钱条款、版本检查 |
| **估值服务部** | 估值核算方法、对账频率、报告频率 |
| **结算服务部** | 账户管理、清算交收、资产保管 |

### ✨ 功能特性

- 🤖 **AI驱动**：基于大语言模型的智能合同分析
- 📝 **规则可配置**：审查规则支持动态更新，无需修改代码
- 🔄 **多格式支持**：支持PDF、Word、TXT等格式合同文件
- 📊 **多维度审查**：覆盖4个业务部门的差异化审查需求
- 🌐 **Web界面**：提供现代化的前端演示界面
- 📈 **API接口**：RESTful API，易于集成到现有系统

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+ (仅前端开发需要)
- 大模型API密钥 (OpenAI/Azure/智谱AI等)

### 1. 克隆项目

```bash
git clone https://github.com/your-org/contract-review-assistant.git
cd contract-review-assistant
```

### 2. 后端安装

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r backend/requirements.txt
```

### 3. 配置环境变量

```bash
# 复制配置模板
cp backend/.env.example backend/.env

# 编辑配置
# 主要配置项：
# - LLM_API_KEY: 大模型API密钥
# - LLM_BASE_URL: API地址
# - LLM_MODEL: 模型名称
# - VECTOR_DB_PATH: 向量数据库路径
```

### 4. 启动后端服务

```bash
cd backend
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### 5. 前端启动（可选）

```bash
cd frontend
npm install
npm run dev
```

访问 `http://localhost:5173` 即可使用前端界面。

---

## 📁 项目结构

```
contract-review-assistant/
├── backend/
│   ├── api/                    # FastAPI接口层
│   │   ├── main.py            # 应用入口
│   │   ├── routes/            # 路由定义
│   │   └── schemas/           # Pydantic模型
│   ├── core/                   # 核心引擎
│   │   ├── document_parser.py # 文档解析
│   │   ├── element_extractor.py # 要素提取
│   │   └── llm_engine.py      # LLM引擎
│   ├── review_modules/         # 审查模块
│   │   ├── investment.py      # 投资监督
│   │   ├── compliance.py      # 风险合规
│   │   ├── valuation.py       # 估值服务
│   │   └── settlement.py      # 结算服务
│   ├── knowledge_base/         # 知识库
│   │   └── regulations/       # 监管政策
│   ├── rules/                  # 可配置规则
│   │   ├── investment_rules.yaml
│   │   ├── compliance_rules.yaml
│   │   ├── valuation_rules.yaml
│   │   └── settlement_rules.yaml
│   ├── requirements.txt       # Python依赖
│   └── .env.example          # 配置模板
├── frontend/                   # 前端应用
│   ├── src/
│   │   ├── components/       # Vue组件
│   │   ├── pages/           # 页面
│   │   └── styles/          # 样式
│   └── package.json
├── docs/                       # 文档
├── scripts/                    # 脚本工具
└── README.md
```

---

## 📖 API文档

### 基础信息

- **Base URL**: `http://localhost:8000/api/v1`
- **文档**: `http://localhost:8000/docs`

### 主要接口

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/review` | 审查单个合同 |
| POST | `/review/batch` | 批量审查 |
| GET | `/departments` | 获取支持的审查部门 |
| GET | `/rules/{department}` | 获取审查规则 |
| PUT | `/rules/{department}` | 更新审查规则 |
| POST | `/upload` | 上传合同文件 |

### 请求示例

```bash
# 审查合同
curl -X POST "http://localhost:8000/api/v1/review" \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "/path/to/contract.pdf",
    "department": "investment_supervision"
  }'
```

### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "product_name": "XX公募基金",
    "product_type": "public_fund",
    "review_items": [
      {
        "item": "投资范围",
        "status": "pass",
        "finding": "符合监管要求",
        "risk_level": "low"
      }
    ],
    "summary": {
      "total": 10,
      "passed": 8,
      "warnings": 2,
      "errors": 0
    }
  }
}
```

---

## 🔧 配置说明

### 审查规则配置

规则文件位于 `backend/rules/` 目录，支持YAML格式动态更新：

```yaml
# 示例：投资监督规则
department: investment_supervision
version: 1.0.0
updated_at: 2025-02-05

rules:
  - id: INV001
    name: 投资范围审查
    description: 检查投资范围是否符合监管要求
    enabled: true
    keywords:
      - "投资范围"
      - "投资标的"
    threshold: 0.8
    
  - id: INV002
    name: 投资比例限制
    description: 验证投资比例是否在限制范围内
    enabled: true
    check_items:
      - "单一股票投资比例"
      - "单一发行人债券比例"
      - "流动性资产比例"
```

### LLM模型配置

```yaml
# backend/.env
LLM_PROVIDER=openai  # 可选：openai/azure/zhipu
LLM_API_KEY=your-api-key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.1
```

---

## 🧪 测试

```bash
# 运行后端测试
cd backend
pytest tests/ -v

# 测试特定模块
pytest tests/test_investment_review.py -v
```

---

## 📦 部署

### Docker部署（推荐）

```bash
# 构建镜像
docker build -t contract-review-assistant .

# 运行容器
docker run -p 8000:8000 -p 5173:5173 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/rules:/app/backend/rules \
  contract-review-assistant
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./rules:/app/backend/rules
    environment:
      - LLM_API_KEY=${LLM_API_KEY}

  frontend:
    build: ./frontend
    ports:
      - "5173:80"
```

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 发起 Pull Request

---

<div align="center">

**Built with ❤️ for Custody Business**

</div>
