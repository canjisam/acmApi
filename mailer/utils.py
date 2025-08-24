import json
from datetime import datetime, timedelta
from typing import List, Dict


def load_contests(path: str) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def filter_upcoming(contests: List[Dict], within_days: int = 3) -> List[Dict]:
    """Return contests within the next `within_days` days from now."""
    now = datetime.now()
    end = now + timedelta(days=within_days)
    out = []
    for c in contests:
        try:
            st = datetime.strptime(c["start_time"], "%Y-%m-%d %H:%M:%S")
        except Exception:
            continue
        if now <= st <= end:
            out.append({**c, "start_dt": st})
    out.sort(key=lambda x: x["start_dt"])
    return out


def filter_next_24h(contests: List[Dict]) -> List[Dict]:
    now = datetime.now()
    end = now + timedelta(hours=24)
    out = []
    for c in contests:
        try:
            st = datetime.strptime(c["start_time"], "%Y-%m-%d %H:%M:%S")
        except Exception:
            continue
        if now <= st <= end:
            out.append({**c, "start_dt": st})
    out.sort(key=lambda x: x["start_dt"])
    return out


def format_contest(c: Dict) -> str:
    st = c.get("start_dt") or datetime.strptime(c.get("start_time"), "%Y-%m-%d %H:%M:%S")
    lines = [
        f"平台: {c.get('platform', '')}",
        f"名称: {c.get('name', '')}",
        f"开始时间: {st.strftime('%Y-%m-%d %H:%M:%S')}",
        f"时长: {c.get('duration', '')}",
        f"链接: {c.get('url', '')}",
    ]
    return "\n".join(lines)


def build_email_text(contests: List[Dict]) -> str:
    if not contests:
        return "未来24小时内没有检测到新的比赛。"
    parts = ["以下为未来24小时内的比赛日程：\n"]
    for i, c in enumerate(contests, 1):
        parts.append(f"{i}. {c.get('name')} ({c.get('platform')})")
        parts.append(f"   开始: {c.get('start_dt').strftime('%Y-%m-%d %H:%M:%S')}")
        parts.append(f"   时长: {c.get('duration')}")
        parts.append(f"   链接: {c.get('url')}")
        parts.append("")
    return "\n".join(parts)
