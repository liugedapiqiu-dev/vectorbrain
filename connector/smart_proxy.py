#!/usr/bin/env python3
"""
智能模型路由代理 - 自动在云端和本地模型之间切换

功能：
- 优先使用云端模型
- 云端超时自动降级到本地
- 无缝切换，用户无感知
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
import logging

# 配置
CLOUD_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
LOCAL_API_URL = "http://127.0.0.1:11434/v1/chat/completions"
CLOUD_MODEL = "qwen3.5-plus"
LOCAL_MODEL = "qwen2.5:14b"
CLOUD_TIMEOUT = 3.0
LOCAL_TIMEOUT = 120.0

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - 🛡️ SmartProxy - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Smart Proxy")

@app.post("/v1/chat/completions")
async def proxy_chat(request: Request):
    """代理聊天请求"""
    try:
        payload = await request.json()
        auth_header = request.headers.get("Authorization", "")
        
        # 1. 尝试请求云端模型
        cloud_payload = payload.copy()
        cloud_payload["model"] = CLOUD_MODEL
        headers = {"Authorization": auth_header, "Content-Type": "application/json"}
        
        try:
            logger.info(f"🌐 尝试连接云端 [{CLOUD_MODEL}]...")
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    CLOUD_API_URL,
                    json=cloud_payload,
                    headers=headers,
                    timeout=CLOUD_TIMEOUT
                )
                response.raise_for_status()
                logger.info("✅ 云端请求成功！")
                return JSONResponse(content=response.json(), status_code=response.status_code)
        
        except (httpx.TimeoutException, httpx.ConnectError) as e:
            logger.warning(f"⚠️ 云端无响应，触发降级机制...")
        
        # 2. 降级到本地模型
        local_payload = payload.copy()
        local_payload["model"] = LOCAL_MODEL
        
        try:
            logger.info(f"🏠 启动本地备用模型 [{LOCAL_MODEL}]...")
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    LOCAL_API_URL,
                    json=local_payload,
                    timeout=LOCAL_TIMEOUT
                )
                response.raise_for_status()
                logger.info("✅ 本地模型接管成功！")
                return JSONResponse(content=response.json(), status_code=response.status_code)
        
        except Exception as e:
            logger.critical(f"🚨 本地模型也失败了：{e}")
            raise HTTPException(status_code=500, detail="Both models failed")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 未知错误：{e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "Smart Proxy",
        "cloud_model": CLOUD_MODEL,
        "local_model": LOCAL_MODEL
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("=" * 60)
    logger.info("🛡️ 智能模型路由代理启动")
    logger.info(f"🌐 监听地址：http://127.0.0.1:8000")
    logger.info(f"☁️ 云端模型：{CLOUD_MODEL}")
    logger.info(f"🏠 本地模型：{LOCAL_MODEL}")
    logger.info("=" * 60)
    uvicorn.run(app, host="127.0.0.1", port=8000)
