# server/manage.py
"""
AdoruWorld 管理工具

用法:
    python manage.py

选择功能:
    1. 启动服务器
    2. 导入种子数据
    3. 导出全部数据
    4. 导入全部数据
"""

import subprocess
from pathlib import Path

SCRIPTS = {
    "1": ("🚀  启动服务器", ["python", "-m", "scripts.run"]),
    "2": ("🌱  导入种子数据", ["python", "-m", "scripts.seed_data"]),
    "3": ("📦  导出全部数据", ["python", "-m", "scripts.export_all"]),
    "4": ("📥  导入全部数据", ["python", "-m", "scripts.import_all"]),
    "5": ("🔐  创建/重置管理员", ["python", "-m", "scripts.create_admin"]),
}


def show_menu():
    print("\n" + "=" * 50)
    print("             AdoruWorld 管理工具")
    print("=" * 50)
    for key, (desc, _) in SCRIPTS.items():
        print(f"  {key}. {desc}")
    print("  0.  退出")
    print("=" * 50)


def main():
    while True:
        show_menu()
        choice = input("\n请选择 [0-4]: ").strip()

        if choice == "0":
            print("👋  再见~")
            break

        if choice not in SCRIPTS:
            print("❌  无效选项，请重新输入")
            continue

        desc, cmd = SCRIPTS[choice]

        if choice == "4":
            path = input("请输入导入文件路径: ").strip()
            cmd = ["python", "-m", "scripts.import_all", path]

        print(f"\n{desc} ...\n")
        result = subprocess.run(cmd, cwd=Path(__file__).parent, check=False)
        if result.returncode != 0:
            print(f"\n⚠️  命令退出码: {result.returncode}")
        input("\n按 Enter 继续...")


if __name__ == "__main__":
    main()
