from fastapi import APIRouter
from datetime import datetime, timezone
import time

router = APIRouter(prefix="/system", tags=["system"])

LAUNCH_TIME = datetime.now(timezone.utc)
START_TIMESTAMP = time.time()


@router.get("/info")
async def get_system_info():
    return {
        "launch_date": LAUNCH_TIME.isoformat(),  # 服务启动时间
    }
