from pathlib import Path
import re
from datetime import datetime

def parse_timestamp_from_name(name: str):
    match = re.search(r"multi_sessions_(\d{8})_(\d{6})", name)
    if match:
        date_str, time_str = match.groups()
        try:
            return datetime.strptime(date_str + time_str, "%Y%m%d%H%M%S")
        except ValueError:
            pass
    return None

def select_multi_sessions_dir(base_path="~/data_collection_11.14/data_collector_opt"):
    base = Path(base_path).expanduser()
    dirs = [p for p in base.glob("multi_sessions*") if p.is_dir()]
    if not dirs:
        raise FileNotFoundError("未找到任何 'multi_sessions*' 目录。")

    def sort_key(p):
        dt = parse_timestamp_from_name(p.name)
        return (dt or datetime.min, p.name)
    
    sorted_dirs = sorted(dirs, key=sort_key, reverse=True)

    print("\n📁 可用的多会话记录（最新在前）：")
    print("─" * 50)
    for i, d in enumerate(sorted_dirs, 1):
        dt = parse_timestamp_from_name(d.name)
        time_label = dt.strftime("%Y-%m-%d %H:%M:%S") if dt else "???"
        print(f"[{i:2}] {time_label}  →  {d.name}")
    print("─" * 50)

    while True:
        try:
            choice = input("\n➤ 请输入多会话编号（直接回车 = 使用最新会话）：").strip()
            if not choice:
                selected_root = sorted_dirs[0]
                print(f"→ 使用最新会话根目录：{selected_root.name}")
                return selected_root
            idx = int(choice)
            if 1 <= idx <= len(sorted_dirs):
                selected_root = sorted_dirs[idx - 1]
                print(f"→ 已选择：{selected_root.name}")
                return selected_root
            else:
                print(f"⚠️  编号无效，请输入 1–{len(sorted_dirs)} 之间的数字。")
        except ValueError:
            print("⚠️  请输入有效数字，或直接回车选择最新会话。")

def select_session_subdir(multi_session_root: Path):
    """在 multi_sessions_*/ 下选择 session_XXX 子目录"""
    session_dirs = sorted(
        [p for p in multi_session_root.glob("session_*") if p.is_dir()],
        key=lambda p: p.name  # session_001 < session_002 < ... < session_010
    )
    
    if not session_dirs:
        raise FileNotFoundError(f"在 '{multi_session_root}' 下未找到任何 'session_*' 子目录。")

    print(f"\n📂 当前多会话：{multi_session_root.name}")
    print("📁 可用的子会话（按编号升序排列）：")
    print("─" * 45)
    for i, d in enumerate(session_dirs, 1):
        print(f"[{i:2}] {d.name}")
    print("─" * 45)

    while True:
        try:
            choice = input("\n➤ 请输入子会话编号（直接回车 = 选择【最新】会话）：").strip()
            if not choice:
                # ✅ NOW DEFAULTS TO LATEST (last in sorted list)
                selected = session_dirs[-1]
                print(f"→ 使用最新子会话：{selected.name}")
                return selected
            idx = int(choice)
            if 1 <= idx <= len(session_dirs):
                selected = session_dirs[idx - 1]
                print(f"→ 已选择子会话：{selected.name}")
                return selected
            else:
                print(f"⚠️  编号无效，请输入 1–{len(session_dirs)} 之间的数字。")
        except ValueError:
            print("⚠️  请输入有效数字，或直接回车选择最新会话。")