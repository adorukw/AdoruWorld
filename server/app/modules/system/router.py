import time
from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(prefix="/system", tags=["system"])

LAUNCH_TIME = datetime.now(timezone.utc)
START_TIMESTAMP = time.time()


@router.get("/info")
async def get_system_info():
    return {
        "launch_date": LAUNCH_TIME.isoformat(),  # 服务启动时间
    }
