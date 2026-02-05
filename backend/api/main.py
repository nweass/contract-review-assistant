"""
合同审查助手 - FastAPI主应用
"""
import os
import tempfile
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.service import get_review_service
from core.config import get_settings
from core.document_parser import DocumentParserFactory


# ==================== Pydantic Models ====================

class ReviewRequest(BaseModel):
    """审查请求"""
    file_path: Optional[str] = None
    content: Optional[str] = None
    department: str = "investment_supervision"
    product_name: Optional[str] = ""
    product_type: Optional[str] = ""


class BatchReviewRequest(BaseModel):
    """批量审查请求"""
    file_paths: List[str]
    department: str = "investment_supervision"


class RuleUpdateRequest(BaseModel):
    """规则更新请求"""
    updates: dict


class ReviewResponse(BaseModel):
    """审查响应"""
    code: int = 200
    message: str = "success"
    data: dict


class DepartmentResponse(BaseModel):
    """部门响应"""
    id: str
    name: str
    enabled: bool


# ==================== FastAPI App ====================

settings = get_settings()

app = FastAPI(
    title="托管合同智能审查系统",
    description="基于大语言模型的托管合同智能审查API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.app.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== API Endpoints ====================

@app.get("/")
async def root():
    """API根路径"""
    return {
        "name": "托管合同智能审查系统",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "contract-review-assistant"}


@app.get("/departments", response_model=List[DepartmentResponse])
async def list_departments():
    """获取支持的审查部门列表"""
    service = get_review_service()
    return service.list_departments()


@app.post("/review", response_model=ReviewResponse)
async def review_contract(request: ReviewRequest):
    """
    审查单个合同
    
    - **file_path**: 合同文件路径
    - **content**: 合同文本内容（与file_path二选一）
    - **department**: 审查部门
    - **product_name**: 产品名称
    - **product_type**: 产品类型
    """
    service = get_review_service()
    
    try:
        result = service.review(
            file_path=request.file_path,
            content=request.content,
            department=request.department,
            product_name=request.product_name or "",
            product_type=request.product_type or "",
        )
        
        return ReviewResponse(
            code=200,
            message="success",
            data=result,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload", response_model=ReviewResponse)
async def upload_and_review(
    file: UploadFile = File(...),
    department: str = Form("investment_supervision"),
):
    """
    上传文件并审查
    
    - **file**: 合同文件（PDF/Word/TXT）
    - **department**: 审查部门
    """
    # 检查文件类型
    ext = Path(file.filename).suffix.lower()
    if ext not in DocumentParserFactory.supported_formats():
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式: {ext}. 支持: {DocumentParserFactory.supported_formats()}",
        )
    
    # 保存临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        service = get_review_service()
        result = service.review(
            file_path=tmp_path,
            department=department,
        )
        
        return ReviewResponse(
            code=200,
            message="success",
            data=result,
        )
    finally:
        # 清理临时文件
        try:
            os.unlink(tmp_path)
        except:
            pass


@app.post("/review/all", response_model=ReviewResponse)
async def review_all_departments(
    file: UploadFile = File(...),
):
    """
    全部门审查（上传文件）
    
    对合同执行所有四个部门的审查
    """
    ext = Path(file.filename).suffix.lower()
    if ext not in DocumentParserFactory.supported_formats():
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式: {ext}",
        )
    
    # 保存临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        service = get_review_service()
        results = service.review_all_departments(file_path=tmp_path)
        
        return ReviewResponse(
            code=200,
            message="success",
            data={
                "results": results,
                "file_name": file.filename,
            },
        )
    finally:
        try:
            os.unlink(tmp_path)
        except:
            pass


@app.post("/batch", response_model=ReviewResponse)
async def batch_review(request: BatchReviewRequest):
    """批量审查"""
    service = get_review_service()
    
    results = service.batch_review(
        file_paths=request.file_paths,
        department=request.department,
    )
    
    return ReviewResponse(
        code=200,
        message="success",
        data={"results": results},
    )


@app.get("/rules/{department}")
async def get_department_rules(department: str):
    """获取部门审查规则"""
    service = get_review_service()
    rules = service.get_rules(department)
    return {
        "department": department,
        "rules": rules,
    }


@app.put("/rules/{department}/{rule_id}")
async def update_rule(
    department: str,
    rule_id: str,
    request: RuleUpdateRequest,
):
    """更新审查规则"""
    service = get_review_service()
    
    result = service.update_rule(
        department=department,
        rule_id=rule_id,
        updates=request.updates,
    )
    
    return result


@app.patch("/rules/{department}/{rule_id}")
async def toggle_rule(
    department: str,
    rule_id: str,
    enabled: bool = Query(..., description="启用或禁用规则"),
):
    """启用/禁用审查规则"""
    service = get_review_service()
    
    result = service.toggle_rule(
        department=department,
        rule_id=rule_id,
        enabled=enabled,
    )
    
    return result


@app.get("/supported-formats")
async def supported_formats():
    """获取支持的文件格式"""
    return {
        "formats": DocumentParserFactory.supported_formats(),
    }


# ==================== 启动命令 ====================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.app.host,
        port=settings.app.port,
        reload=True,
    )
