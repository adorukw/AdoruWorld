import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATABASE_URL: str = os.getenv(
    "DATABASE_URL", f"sqlite+aiosqlite:///{BASE_DIR}/adoruworld.db"
)

SITE_START_DATE: str = os.getenv("SITE_START_DATE", "2025-01-01")

API_PREFIX: str = "/api/v1"

PROJECT_NAME: str = "AdoruKWorld Server"
VERSION: str = "1.0.0"
DESCRIPTION: str = "AdoruKWorld personal site backend API"

# 上传文件 URL 前缀
#
# 为什么需要这个？
# 前端页面通过 nginx 反向代理访问，前端存储的图片路径（如
# /uploads/media/image/xxx.jpg）直接给 <img src> 使用时，
# 浏览器会请求 http://domain/uploads/...
# 但为了与前端路由 /adoru-world/ 保持路径层级一致，nginx 代理
# location 配置需统一前缀更清晰。
#
# 加上此前缀后，存储路径变为 /adoru-world/uploads/...，
# 浏览器请求 http://domain/adoru-world/uploads/...
# → nginx 的 location /adoru-world/uploads/ 匹配
# → rewrite 去掉 /adoru-world 前缀
# → proxy_pass 到后端实际文件
#
# 如果 nginx 的 uploads location 不需要前缀，设为空字符串 "" 即可
UPLOAD_URL_PREFIX: str = "/adoru-world"
