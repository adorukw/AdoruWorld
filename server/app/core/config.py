import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def _load_env_file() -> None:
    """极简 .env 加载器：KEY=VALUE 逐行读入，已存在的环境变量不覆盖"""
    env_file = BASE_DIR / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip()
        if key and key not in os.environ:
            os.environ[key] = value


_load_env_file()

DATABASE_URL: str = os.getenv(
    "DATABASE_URL", f"sqlite+aiosqlite:///{BASE_DIR}/adoruworld.db"
)

# ============================================================
# 认证配置（JWT）
# ============================================================
SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-only-insecure-key")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# 初始管理员密码（仅 scripts/create_admin.py 使用，用后即弃）
INITIAL_ADMIN_PASSWORD: str = os.getenv("INITIAL_ADMIN_PASSWORD", "")

# ============================================================
# 邮件发送（注册验证码）
# console 模式打印到后端日志（开发零依赖）；smtp 模式真实发信
# QQ 邮箱：SMTP_HOST=smtp.qq.com PORT=465 USER=邮箱 PASSWORD=授权码
# ============================================================
MAIL_MODE: str = os.getenv("MAIL_MODE", "console")
SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.qq.com")
SMTP_PORT: int = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER: str = os.getenv("SMTP_USER", "")
SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM: str = os.getenv("SMTP_FROM", "") or os.getenv("SMTP_USER", "")

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
