from app.main import app
import uvicorn
import sys
from pathlib import Path
import subprocess
from app.config import DATABASE_URL

server_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(server_dir))


def start_sqlite_web():
    try:
        db_path = DATABASE_URL.replace("sqlite+aiosqlite:///", "")
        db_file = Path(db_path)

        if not db_file.exists():
            print("⚠️  数据库文件尚未生成")
            return

        subprocess.Popen(
            [sys.executable, "-m", "sqlite_web",
                str(db_file), "--port", "8081", "--host", "0.0.0.0"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print("✅ SQLite Web: http://127.0.0.1:8081")
    except Exception as e:
        print("⚠️  SQLite Web 启动失败:", e)


if __name__ == "__main__":
    start_sqlite_web()
    print("已成功启动服务器...")
    print("本地:   http://127.0.0.1:8000")
    print("局域网: http://0.0.0.0:8000")
    print("Docs:   http://127.0.0.1:8000/docs")
    print("Redoc:  http://127.0.0.1:8000/redoc")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
