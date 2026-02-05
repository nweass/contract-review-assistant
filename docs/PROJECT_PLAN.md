# 托管业务AI合同审查助手 - 开发方案

## 📋 项目概述

**项目名称**：托管合同智能审查系统
**目标**：通过AI技术实现托管公募基金和年金合同的自动化要素提取与多维度风险审查

---

## 🎯 核心功能模块

### 1. 合同要素提取引擎
- **输入识别**：产品名称、产品类型、合同类别
- **要素提取**：结构化+非结构化数据混合处理
- **时效要求**：准实时

### 2. 多部门视角审查（4大模块）

#### 📊 投资监督部
- 投资范围审查
- 投资比例限制
- 投资限制合规性
- 对照现行监管政策

#### ⚖️ 风险合规部
- 合同文件名称一致性（正文 vs 签署页）
- 当事人权利义务
- 托管人职责条款
- 反洗钱相关条款
- 违约责任条款
- 引用文件版本检查（是否为最新版）

#### 💰 估值服务部
- 估值核算方法及频率
- 对账处理方法及频率
- 报告出具方法及频率

#### 🔄 结算服务部
- 账户管理要求
- 清算交收方式与频率
- 实物资产保管方式
- 核对方式

---

## 🔧 技术架构

```
├── contract-review-core/          # 核心引擎
│   ├── document_parser.py         # 文档解析（PDF/Word）
│   ├── element_extractor.py       # 要素提取
│   ├── vector_store.py            # 向量知识库
│   └── rule_engine.py             # 规则引擎
│
├── review_modules/                 # 审查模块
│   ├── investment_supervision.py  # 投资监督审查
│   ├── risk_compliance.py         # 风险合规审查
│   ├── valuation_service.py       # 估值服务审查
│   └── settlement_service.py      # 结算服务审查
│
├── knowledge_base/                 # 知识库
│   ├── regulations/               # 监管政策库
│   ├── templates/                 # 合同模板库
│   └── rules/                     # 审查规则库
│
├── api/                            # API层
│   └── fastapi_app.py
│
├── cli/                            # CLI工具
│   └── review_cli.py
│
└── tests/                          # 测试用例
```

---

## 🚀 开发路线图

### Phase 1：基础架构（第1-2周）
- [ ] 项目初始化与环境配置
- [ ] 文档解析引擎（支持PDF/Word）
- [ ] 合同要素提取模块
- [ ] 基础向量数据库搭建

### Phase 2：审查模块开发（第3-5周）
- [ ] 投资监督审查模块
- [ ] 风险合规审查模块
- [ ] 估值服务审查模块
- [ ] 结算服务审查模块

### Phase 3：知识库与规则（第6-7周）
- [ ] 监管政策知识库
- [ ] 合同模板库
- [ ] 审查规则引擎
- [ ] 版本比对功能

### Phase 4：集成与优化（第8周）
- [ ] FastAPI接口开发
- [ ] CLI工具封装
- [ ] 性能优化
- [ ] 测试与部署

---

## 📦 依赖技术栈

```yaml
# 核心依赖
python: ">=3.10"
langchain: ">=0.2.0"
langchain-openai: ">=0.1.0"
unstructured: ">=0.14.0"        # 文档解析
pymupdf: ">=1.24.0"             # PDF处理
python-docx: ">=1.1.0"          # Word处理
chromadb: ">=0.5.0"             # 向量数据库
pydantic: ">=2.6.0"             # 数据校验

# API服务
fastapi: ">=0.110.0"
uvicorn: ">=0.27.0"

# 工具库
python-dotenv: ">=1.0.0"
loguru: ">=0.7.0"
rich: ">=13.7.0"
```

---

## 📝 使用方式

### CLI方式
```bash
# 审查单个合同
python -m cli.review_cli --file 合同.pdf --output report.md

# 批量审查
python -m cli.review_cli --batch /path/to/contracts/
```

### API方式
```bash
# 启动服务
uvicorn api.fastapi_app:app --host 0.0.0.0 --port 8000

# 调用示例
curl -X POST "http://localhost:8000/review" \
  -F "file=@合同.pdf" \
  -F "department=investment_supervision"
```

### 审查报告输出
```markdown
# 合同审查报告

## 基本信息
- 产品名称：XXX
- 产品类型：公募基金
- 审查部门：投资监督部

## 审查结果
### ✅ 通过项
- 投资范围符合监管要求
- ...

### ⚠️ 风险提示
- [高] 投资比例超出监管限制
- [中] 部分条款表述不明确
```

---

## 🎯 下一步行动

1. **确认需求细节**
   - 具体支持哪些合同类型？（目前已知：公募基金、年金）
   - 是否需要支持增量审查还是全量审查？
   - 报告输出格式偏好？

2. **准备数据**
   - 提供脱敏的合同样本（2-3份不同类型）
   - 监管政策文件
   - 现有审查清单/检查表

3. **开发环境确认**
   - LLM模型选择（本地部署/云端API）
   - GPU资源需求
   - 部署环境要求

---

*方案版本：v1.0*
*生成时间：2025-02-05*
