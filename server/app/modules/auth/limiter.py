"""内存限流器：登录防爆破、验证码发送频率、验证尝试次数

设计说明：
- 单进程内存 dict，重启即清零（对个人站足够；多实例部署需换 Redis）
- 每个动作一个独立桶，按 key（用户名/邮箱）隔离
"""
import time

# key -> (失败次数/上次时间戳)
_attempts: dict[str, list] = {}

LOGIN_MAX_FAILS = 5          # 登录连续失败上限
LOGIN_LOCK_SECONDS = 15 * 60  # 锁定 15 分钟
SEND_CODE_INTERVAL = 60       # 同一邮箱两次发码最小间隔（秒）
VERIFY_MAX_ATTEMPTS = 5       # 验证码尝试上限


def _now() -> float:
    return time.monotonic()


def is_locked(key: str, max_fails: int, lock_seconds: int) -> bool:
    record = _attempts.get(key)
    if not record:
        return False
    fails, last_ts = record
    if fails >= max_fails and (_now() - last_ts) < lock_seconds:
        return True
    # 锁定期已过，自动重置
    if fails >= max_fails:
        _attempts.pop(key, None)
    return False


def record_fail(key: str) -> None:
    record = _attempts.get(key)
    if record:
        record[0] += 1
        record[1] = _now()
    else:
        _attempts[key] = [1, _now()]


def reset(key: str) -> None:
    """成功后清除失败计数"""
    _attempts.pop(key, None)


def check_send_interval(key: str, interval: int = SEND_CODE_INTERVAL) -> bool:
    """True=允许发送；间隔内返回 False"""
    record = _attempts.get(f"send:{key}")
    if record and (_now() - record[1]) < interval:
        return False
    _attempts[f"send:{key}"] = [0, _now()]
    return True
